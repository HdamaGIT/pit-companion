from pit_companion.config import ProbeConfig
# Later: import spidev, MAX31856, etc.


class MockProbeReader:
    """Dev-only reader that returns fake temps (e.g., for GitHub CI, local dev)."""

    def __init__(self, base_temp: float = 110.0):
        self.base_temp = base_temp

    def read_probe(self, probe: ProbeConfig) -> float:
        # TODO: replace with real hardware logic
        # add some tiny variation so it doesn't look static
        return self.base_temp
