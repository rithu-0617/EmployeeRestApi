"""
Student model.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone


@dataclass
class Student:
    id: str
    first_name: str
    last_name: str
    email: str
    course: str
    enrollment_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_active: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Student:
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
