import json
import logging
from pathlib import Path
from datetime import datetime


class OutputLogger:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self._create_session_logfile()

    def _create_session_logfile(self) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"agent_output_{timestamp}.jsonl"
        path = self.output_dir / filename
        logging.info(f"📄 Output log initialized: {path}")
        return path

    def save(self, record: dict):
        try:
            with self.session_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            logging.debug(f"Saved record to log: {record.get('task', 'unnamed')}")
        except Exception as e:
            logging.error(f"❌ Failed to write output record: {e}")
            raise
