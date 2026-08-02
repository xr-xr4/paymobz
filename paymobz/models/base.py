from __future__ import annotations

from typing import Any, Dict


class BaseModel:
    def __init__(self, **kwargs):
        annotations = {}

        for cls in reversed(self.__class__.__mro__):
            annotations.update(getattr(cls, "__annotations__", {}))

        for field in annotations:
            if field in kwargs:
                value = kwargs[field]
            else:
                value = getattr(self.__class__, field, None)

                if isinstance(value, dict):
                    value = value.copy()
                elif isinstance(value, list):
                    value = value.copy()

            setattr(self, field, value)

    def to_dict(self, *, exclude_none: bool = True) -> Dict[str, Any]:
        data = self.__dict__.copy()

        if exclude_none:
            data = {k: v for k, v in data.items() if v is not None}

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def model_dump(self, *, exclude_none: bool = True):
        return self.to_dict(exclude_none=exclude_none)

    @classmethod
    def model_validate(cls, data: Dict[str, Any]):
        return cls.from_dict(data)

    def __repr__(self):
        values = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"