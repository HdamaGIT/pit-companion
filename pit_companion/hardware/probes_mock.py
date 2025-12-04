# pit_companion/hardware/probes_mock.py

import math
import random
from datetime import datetime, timedelta
from typing import Dict

from .probes_base import ProbeReader


class MockProbeReader(ProbeReader):
    """
    Simulates probe readings so you can develop the UI without hardware.
    - Pit temp: oscillates gently around a target (e.g. 110°C)
    - Meat temp: slowly rises towards a done temp (e.g. 95°C)
    """

    def __init__(
        self,
        pit_target: float = 110.0,
        meat_start: float = 8.0,
        meat_done: float = 95.0,
    ) -> None:
        self.pit_target = pit_target
        self.meat_start = meat_start
        self.meat_done = meat_done
        self.start_time = datetime.utcnow()

    def _minutes_since_start(self) -> float:
        return (datetime.utcnow() - self.start_time).total_seconds() / 60.0

    def read_all(self) -> Dict[str, float]:
        t_min = self._minutes_since_start()

        # Pit: base around target with slow sinusoidal swing + small noise
        pit = (
            self.pit_target
            + 5.0 * math.sin(t_min / 5.0)
            + random.uniform(-0.7, 0.7)
        )

        # Meat: simple "cooking" curve – fast at first, then flattening
        progress = 1 - math.exp(-t_min / 60.0)  # asymptotic 0→1 over ~1h
        meat = self.meat_start + (self.meat_done - self.meat_start) * progress
        meat += random.uniform(-0.4, 0.4)  # small noise
        meat = max(self.meat_start, min(self.meat_done + 5, meat))

        return {
            "pit": pit,
            "meat": meat,
        }
