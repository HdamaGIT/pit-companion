from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class ProbeReading:
    """Single temperature reading from one probe."""
    timestamp: datetime
    probe_id: str
    value_c: float


@dataclass
class Snapshot:
    """Snapshot of all probes at a given time."""
    timestamp: datetime
    readings: Dict[str, ProbeReading]
