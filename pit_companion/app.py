from pit_companion.config import load_config
from pit_companion.core.controller import PitController
from pit_companion.hardware.probes_base import MockProbeReader
from pit_companion.storage.csv_storage import CSVStorage
from pit_companion.integrations.home_assistant import HomeAssistantMQTTPublisher


def create_app(config_path: str = "config/config.yaml") -> PitController:
    cfg = load_config(config_path)

    reader = MockProbeReader()
    storage = CSVStorage(cfg.storage.csv.path if cfg.storage.csv else "readings.csv")
    ha_publisher = HomeAssistantMQTTPublisher(cfg.home_assistant)

    controller = PitController(
        cfg=cfg,
        reader=reader,
        storage=storage,
        publishers=[ha_publisher],
    )
    return controller
