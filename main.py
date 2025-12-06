import argparse
import logging
from core.engine import AgentEngine


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )


def parse_args():
    parser = argparse.ArgumentParser(description="AgenticAI Builder CLI")
    parser.add_argument(
        "-c", "--config",
        required=True,
        help="Path to YAML configuration file"
    )
    return parser.parse_args()


def main():
    configure_logging()
    args = parse_args()

    try:
        engine = AgentEngine(config_path=args.config)
        engine.run()
    except Exception as e:
        logging.error(f"❌ AgenticAI Builder failed: {e}")


if __name__ == "__main__":
    main()
