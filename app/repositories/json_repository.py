"""
JSON-file backed repository.
Drop-in replacement: implement BaseRepository with SQLAlchemy to switch to a real DB.
"""
import json
import os
import threading
from typing import Optional, TypeVar, Type

from app.repositories.base_repository import BaseRepository

T = TypeVar("T")


class JsonRepository(BaseRepository[T]):
    """Thread-safe JSON-file data store."""

    def __init__(self, filepath: str, model_cls: Type[T]) -> None:
        self._filepath = filepath
        self._model_cls = model_cls
        self._lock = threading.Lock()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            self._write([])

    # ---- internal helpers ----
    def _read(self) -> list[dict]:
        with open(self._filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: list[dict]) -> None:
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _to_model(self, data: dict) -> T:
        return self._model_cls.from_dict(data)  # type: ignore[attr-defined]

    def _to_dict(self, entity: T) -> dict:
        return entity.to_dict(include_hash=True) if hasattr(entity, "password_hash") else entity.to_dict()  # type: ignore[attr-defined]

    # ---- public CRUD ----
    def get_all(self) -> list[T]:
        with self._lock:
            return [self._to_model(d) for d in self._read()]

    def get_by_id(self, entity_id: str) -> Optional[T]:
        with self._lock:
            for item in self._read():
                if item.get("id") == entity_id:
                    return self._to_model(item)
        return None

    def get_by_field(self, field: str, value: str) -> Optional[T]:
        """Lookup by any field (e.g., username)."""
        with self._lock:
            for item in self._read():
                if item.get(field) == value:
                    return self._to_model(item)
        return None

    def create(self, entity: T) -> T:
        with self._lock:
            data = self._read()
            data.append(self._to_dict(entity))
            self._write(data)
        return entity

    def update(self, entity_id: str, entity: T) -> Optional[T]:
        with self._lock:
            data = self._read()
            for i, item in enumerate(data):
                if item.get("id") == entity_id:
                    data[i] = self._to_dict(entity)
                    self._write(data)
                    return entity
        return None

    def delete(self, entity_id: str) -> bool:
        with self._lock:
            data = self._read()
            new_data = [d for d in data if d.get("id") != entity_id]
            if len(new_data) == len(data):
                return False
            self._write(new_data)
            return True
