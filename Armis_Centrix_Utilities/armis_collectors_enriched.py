#!/usr/bin/env python3
import os
import csv
import logging
import requests
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ====== CONFIG ======
TENANT = os.getenv("ARMIS_TENANT", "verizon1")
SECRET_KEY = os.getenv("ARMIS_SECRET_KEY", "<PUT_SECRET_KEY_HERE>")
VERIFY_TLS = False                 # set True if you want SSL verification
REQUEST_TIMEOUT = 30
CSV_FILE = "armis_collectors_enriched.csv"

# Proxy (set to {} to disable)
PROXIES = {
    "http":  os.getenv("HTTP_PROXY",  "http://vzproxy.verizon.com:9290"),
    "https": os.getenv("HTTPS_PROXY", "http://vzproxy.verizon.com:9290"),
}

BASE = f"https://{TENANT}.armis.com/api/v1"
TOKEN_URL = f"{BASE}/access_token/"
COLLECTORS_URL = f"{BASE}/collectors/"

# ====== LOGGING ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("armis_collectors_enriched.log", encoding="utf-8")
    ],
)
log = logging.getLogger("armis_collectors")

# ====== HTTP SESSION ======
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


def get_access_token(session: requests.Session) -> str:
    if not SECRET_KEY or SECRET_KEY.startswith("<PUT_"):
        raise RuntimeError("Missing ARMIS_SECRET_KEY (env var or edit the script)."
        )
    r = session.post(TOKEN_URL, data={"secret_key": SECRET_KEY}, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    token = r.json().get("access_token")
    if not token:
        raise RuntimeError(f"No access_token in response: {r.text[:200]}")
    return token


def list_collectors(session: requests.Session, token: str):
    headers = {"Authorization": token, "Accept": "application/json"}
    r = session.get(COLLECTORS_URL, headers=headers, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json().get("collectors", [])


def get_collector_detail(session: requests.Session, token: str, collector_id):
    headers = {"Authorization": token, "Accept": "application/json"}
    url = f"{COLLECTORS_URL}{collector_id}/"
    r = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.json()


def up_down(status: str, last_seen: str, threshold_minutes: int = 15):
    """Returns (health_text, icon)."""
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


FIELDS = [
    "id", "name", "type", "status", "lastSeen",
    "ipAddress", "macAddress", "subnet", "defaultGateway",
    "clusterId", "collectorNumber",
    "health", "health_icon"]
    

def write_csv(rows):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    log.info("Wrote %s (%d rows)", CSV_FILE, len(rows))


def main():
    try:
        session = build_session()
        token = get_access_token(session)

        # 1) list all collectors (summary)
        base_list = list_collectors(session, token)
        log.info("Collectors (summary): %d", len(base_list))

        # 2) enrich with per-collector details
        enriched = []
        for c in base_list:
            cid = c.get("id")
            try:
                detail = get_collector_detail(session, token, cid)
            except Exception as e:
                log.warning("Failed detail for %s: %s", cid, e)
                detail = {}

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
