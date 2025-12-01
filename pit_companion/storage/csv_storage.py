import csv
from pathlib import Path
from pit_companion.core.models import Snapshot
from pit_companion.storage.base import StorageBackend


class CSVStorage(StorageBackend):
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "probe_id", "value_c"])

    def save_snapshot(self, snapshot: Snapshot) -> None:
        with self.path.open("a", newline="") as f:
            writer = csv.writer(f)
            for reading in snapshot.readings.values():
                writer.writerow(
                    [reading.timestamp.isoformat(), reading.probe_id, reading.value_c]
                )
