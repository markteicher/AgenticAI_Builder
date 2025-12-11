#!/usr/bin/env python3
import os
import csv
import logging
from datetime import datetime, timezone, timedelta
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========= CONFIG =========
TENANT = os.getenv("ARMIS_TENANT", "verizon1")
SECRET_KEY = os.getenv("ARMIS_SECRET_KEY", "<PUT_SECRET_KEY_HERE>")

VERIFY_TLS = False           # your environment preference
REQUEST_TIMEOUT = 30
TOKEN_REFRESH_MARGIN = 120   # seconds before expiry to refresh token
CSV_FILE = "armis_collectors_enriched.csv"

# Proxies (set {} to disable)
PROXIES = {
    "http":  os.getenv("HTTP_PROXY",  "http://vzproxy.verizon.com:9290"),
    "https": os.getenv("HTTPS_PROXY", "http://vzproxy.verizon.com:9290"),
}

BASE = f"https://{TENANT}.armis.com/api/v1"
TOKEN_URL = f"{BASE}/access_token/"
COLLECTORS_URL = f"{BASE}/collectors/"

# ========= LOGGING =========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("armis_collectors_enriched.log", encoding="utf-8")],
)
log = logging.getLogger("armis")

# ========= HTTP SESSION (retries + proxy) =========
def build_session() -> requests.Session:
    s = requests.Session()
    s.verify = VERIFY_TLS
    s.proxies = PROXIES or {}
    retry = Retry(
        total=5, connect=5, read=5, status=5,
        backoff_factor=1.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "POST"})
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://",  HTTPAdapter(max_retries=retry))
    return s

# ========= TOKEN MANAGEMENT =========
ACCESS_TOKEN: str | None = None
TOKEN_EXPIRES_AT: datetime | None = None

def _parse_expiration(expiration_utc: str) -> datetime:
    return datetime.fromisoformat(expiration_utc.replace("Z", "+00:00"))

def _get_new_token(session: requests.Session) -> None:
    global ACCESS_TOKEN, TOKEN_EXPIRES_AT
    if not SECRET_KEY or SECRET_KEY.startswith("<PUT_"):
        raise RuntimeError("Missing ARMIS_SECRET_KEY (set env var or edit the script).")

    log.info("Requesting new access token…")
    r = session.post(TOKEN_URL, data={"secret_key": SECRET_KEY}, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()

    data = r.json()
    token = (data.get("data") or {}).get("access_token")
    exp   = (data.get("data") or {}).get("expiration_utc")
    if not token:
        raise RuntimeError(f"No access_token in response: {r.text[:200]}")
    if not exp:
        TOKEN_EXPIRES_AT = datetime.now(timezone.utc) + timedelta(minutes=15)
    else:
        TOKEN_EXPIRES_AT = _parse_expiration(exp)

    ACCESS_TOKEN = token
    log.info("Token acquired; expires at %s", TOKEN_EXPIRES_AT.isoformat())

def _token_expiring_soon() -> bool:
    if not TOKEN_EXPIRES_AT:
        return True
    margin = timedelta(seconds=TOKEN_REFRESH_MARGIN)
    return datetime.now(timezone.utc) + margin >= TOKEN_EXPIRES_AT

def ensure_token(session: requests.Session) -> str:
    global ACCESS_TOKEN
    if ACCESS_TOKEN is None or _token_expiring_soon():
        _get_new_token(session)
    return ACCESS_TOKEN

# ========= API HELPERS =========
def api_get(session: requests.Session, url: str, timeout: int = REQUEST_TIMEOUT) -> requests.Response:
    token = ensure_token(session)

    headers_plain  = {"Authorization": token,             "Accept": "application/json"}
    headers_bearer = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    r = session.get(url, headers=headers_plain, timeout=timeout)
    if r.status_code == 401:
        r2 = session.get(url, headers=headers_bearer, timeout=timeout)
        if r2.status_code == 401 and _token_expiring_soon():
            _get_new_token(session)
            token2 = ACCESS_TOKEN
            headers_plain2  = {"Authorization": token2,             "Accept": "application/json"}
            headers_bearer2 = {"Authorization": f"Bearer {token2}", "Accept": "application/json"}
            r = session.get(url, headers=headers_plain2, timeout=timeout)
            if r.status_code == 401:
                r = session.get(url, headers=headers_bearer2, timeout=timeout)
                return r
            return r
        return r2
    return r

# ========= COLLECTORS =========
def list_collectors(session: requests.Session):
    r = api_get(session, COLLECTORS_URL)
    r.raise_for_status()
    body = r.json()
    return body.get("collectors", body.get("results", []))

def get_collector_detail(session: requests.Session, collector_id: str):
    url = f"{COLLECTORS_URL}{collector_id}/"
    r = api_get(session, url)
    r.raise_for_status()
    return r.json()

# ========= HEALTH =========
def up_down(status: str | None, last_seen: str | None, threshold_minutes: int = 15) -> tuple[str, str]:
    if not status or status.lower() != "active":
        return "DOWN", "❌"
    try:
        dt = datetime.fromisoformat((last_seen or "").replace("Z", "+00:00"))
        age_min = (datetime.now(timezone.utc) - dt).total_seconds() / 60
        if age_min > threshold_minutes:
            return f"DOWN (last seen {int(age_min)} min ago)", "❌"
        return "UP", "✅"
    except Exception:
        return "UNKNOWN", "❓"

# ========= CSV =========
FIELDS = [
    "id", "name", "type", "status", "lastSeen",
    "ipAddress", "macAddress", "subnet", "defaultGateway",
    "clusterId", "collectorNumber",
    "health", "health_icon"
]

def write_csv(rows: list[dict]):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    log.info("Wrote %s (%d rows)", CSV_FILE, len(rows))

# ========= MAIN =========
def main():
    try:
        session = build_session()
        ensure_token(session)

        base = list_collectors(session)
        log.info("Collectors found: %d", len(base))

        enriched = []
        for c in base:
            cid = c.get("id")
            detail = {}
            try:
                detail = get_collector_detail(session, cid)
            except requests.HTTPError as e:
                log.warning("Detail fetch failed for id=%s: %s", cid, e)

            merged = {**c, **detail}
            health, icon = up_down(merged.get("status"), merged.get("lastSeen"))
            merged["health"] = health
            merged["health_icon"] = icon
            enriched.append(merged)

        write_csv(enriched)

        up_count = sum(1 for r in enriched if r.get("health") == "UP")
        down_count = sum(1 for r in enriched if str(r.get("health", "")).startswith("DOWN"))
        print(f"✅ Collectors: {len(enriched)} | Online: {up_count} | Offline: {down_count}")
        print(f"CSV: {CSV_FILE}")

    except requests.RequestException as e:
        log.exception("Network/API error")
        print(f"❌ Request failed: {e}")
    except Exception as e:
        log.exception("Runtime error")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
