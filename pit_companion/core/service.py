# pit_companion/core/service.py

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, List, Tuple

from pit_companion.hardware.probes_base import ProbeReader


@dataclass
class Reading:
    timestamp: datetime
    values: Dict[str, float]


class TemperatureService:
    """
    Small in-process service that:
    - Polls a ProbeReader
    - Stores a rolling history of readings
    - Provides convenience methods for UI code
    """

    def __init__(
        self,
        reader: ProbeReader,
        max_points: int = 6 * 60,  # e.g. last 6h if reading every minute
    ) -> None:
        self.reader = reader
        self.history: Deque[Reading] = deque(maxlen=max_points)

    def poll_once(self) -> Reading:
        """Take one reading and store it."""
        values = self.reader.read_all()
        reading = Reading(timestamp=datetime.utcnow(), values=values)
        self.history.append(reading)
        return reading

    def get_latest(self) -> Reading | None:
        return self.history[-1] if self.history else None

    def get_series(self, probe_name: str) -> List[Tuple[datetime, float]]:
        """Return list of (timestamp, value) for a given probe."""
        return [
            (r.timestamp, r.values.get(probe_name))
            for r in self.history
            if probe_name in r.values
        ]
