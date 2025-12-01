import argparse
import logging

from pit_companion.app import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="Pit Companion")
    parser.add_argument(
        "-c", "--config", default="config/config.yaml", help="Path to config file"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    controller = create_app(args.config)
    controller.run_forever()
