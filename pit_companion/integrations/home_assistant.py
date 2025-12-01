from typing import Optional

import paho.mqtt.client as mqtt

from pit_companion.config import HomeAssistantConfig
from pit_companion.core.models import Snapshot


class HomeAssistantMQTTPublisher:
    def __init__(self, cfg: HomeAssistantConfig) -> None:
        self.cfg = cfg
        if not cfg.enabled or cfg.mqtt is None:
            self._client: Optional[mqtt.Client] = None
            return

        self._client = mqtt.Client()
        self._client.connect(cfg.mqtt.host, cfg.mqtt.port)

    def publish_snapshot(self, snapshot: Snapshot) -> None:
        if not self.cfg.enabled or self._client is None or self.cfg.mqtt is None:
            return

        prefix = self.cfg.mqtt.topic_prefix.rstrip("/")
        for probe_id, reading in snapshot.readings.items():
            topic = f"{prefix}/{probe_id}"
            payload = str(reading.value_c)
            self._client.publish(topic, payload, retain=True)
