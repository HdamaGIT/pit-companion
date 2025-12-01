from datetime import datetime
from time import sleep
from typing import Protocol, List

from pit_companion.core.models import Snapshot, ProbeReading
from pit_companion.config import Config, ProbeConfig


class ProbeReader(Protocol):
    def read_probe(self, probe: ProbeConfig) -> float:
        """Return temperature in °C for given probe, or raise on failure."""


class StorageBackend(Protocol):
    def save_snapshot(self, snapshot: Snapshot) -> None:
        ...


class Publisher(Protocol):
    def publish_snapshot(self, snapshot: Snapshot) -> None:
        ...


class PitController:
    def __init__(
        self,
        cfg: Config,
        reader: ProbeReader,
        storage: StorageBackend,
        publishers: List[Publisher] | None = None,
    ) -> None:
        self.cfg = cfg
        self.reader = reader
        self.storage = storage
        self.publishers = publishers or []

    def run_forever(self) -> None:
        """Main loop: read -> store -> publish."""
        interval = self.cfg.app.poll_interval_seconds
        while True:
            snapshot = self._take_snapshot()
            self.storage.save_snapshot(snapshot)
            for pub in self.publishers:
                pub.publish_snapshot(snapshot)
            sleep(interval)

    def _take_snapshot(self) -> Snapshot:
        ts = datetime.utcnow()
        readings = {}
        for probe_cfg in self.cfg.probes:
            value_c = self.reader.read_probe(probe_cfg)
            readings[probe_cfg.id] = ProbeReading(
                timestamp=ts,
                probe_id=probe_cfg.id,
                value_c=value_c,
            )
        return Snapshot(timestamp=ts, readings=readings)
