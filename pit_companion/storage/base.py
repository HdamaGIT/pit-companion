from abc import ABC, abstractmethod
from pit_companion.core.models import Snapshot


class StorageBackend(ABC):
    @abstractmethod
    def save_snapshot(self, snapshot: Snapshot) -> None:
        ...
