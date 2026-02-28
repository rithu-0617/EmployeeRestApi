"""
Abstract base repository – defines the contract every data-store must fulfil.
Swap the JSON implementation for SQLAlchemy / MongoDB later without touching API code.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Interface for CRUD operations."""

    @abstractmethod
    def get_all(self) -> list[T]:
        ...

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        ...

    @abstractmethod
    def create(self, entity: T) -> T:
        ...

    @abstractmethod
    def update(self, entity_id: str, entity: T) -> Optional[T]:
        ...

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        ...
