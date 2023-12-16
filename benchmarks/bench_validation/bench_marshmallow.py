from typing import Any, Callable, Optional

import enum
import datetime
import marshmallow
import orjson

from marshmallow_dataclass import dataclass
from marshmallow.types import StrSequenceOrSet


class BaseOrjsonSchema(marshmallow.Schema):
    def dumpb(
        self,
        obj: Any,
        *,
        many: bool | None = None,
        default: Callable[[Any], Any] | None = None,
        option: int | None = None,
    ) -> bytes:
        serialized = self.dump(obj, many=many)
        return orjson.dumps(serialized, default=default, option=option)

    def dumps(
        self,
        obj: Any,
        *,
        many: bool | None = None,
        default: Callable[[Any], Any] | None = None,
        option: int | None = None,
    ) -> str:
        return self.dumpb(obj, many=many, default=default, option=option).decode()

    def loads(
        self,
        json_data: str,
        *,
        many: bool | None = None,
        partial: bool | StrSequenceOrSet | None = None,
        unknown: str | None = None,
        **kwargs,
    ) -> Any:
        data = orjson.loads(json_data)
        return self.load(data, many=many, partial=partial, unknown=unknown)


class Permissions(str, enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    READ_WRITE = "READ_WRITE"

    def __missing__(self, key):
        return None


@dataclass(base_schema=BaseOrjsonSchema)
class File:
    name: str
    created_by: str
    created_at: datetime.datetime
    nbytes: int
    permissions: Permissions
    updated_by: Optional[str] = None
    updated_at: Optional[datetime.datetime] = None
    type: str = "file"


@dataclass(base_schema=BaseOrjsonSchema)
@dataclass
class Directory:
    name: str
    created_by: str
    created_at: datetime.datetime
    contents: list[File]
    updated_by: Optional[str] = None
    updated_at: Optional[datetime.datetime] = None
    type: str = "directory"


@dataclass(base_schema=BaseOrjsonSchema)
@dataclass
class Directories:
    directories: list[Directory]
    type: str = "directories"


def encode(obj):
    return Directories.Schema().dumps(obj)


def decode(msg):
    return Directories.Schema().loads(json_data=msg)


label = "marshmallow"
