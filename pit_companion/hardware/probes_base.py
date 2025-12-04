from abc import ABC, abstractmethod
from typing import Dict


class ProbeReader(ABC):
    """Abstract base class for anything that can read probe temperatures."""

    @abstractmethod
    def read_all(self) -> Dict[str, float]:
        """
        Return a mapping of probe_name -> temperature in °C.
        Example: {"pit": 118.3, "meat": 56.7}
        """
        raise NotImplementedError