from __future__ import annotations

import enum
import datetime
from typing import Literal, Annotated

import pydantic


class Permissions(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    READ_WRITE = "READ_WRITE"


class File(pydantic.BaseModel):
    type: Literal["file"] = "file"
    name: str
    created_by: str
    created_at: datetime.datetime
    updated_by: str | None = None
    updated_at: datetime.datetime | None = None
    nbytes: int
    permissions: Permissions


class Directory(pydantic.BaseModel):
    type: Literal["directory"] = "directory"
    name: str
    created_by: str
    created_at: datetime.datetime
    updated_by: str | None = None
    updated_at: datetime.datetime | None = None
    contents: list[File]


class Directories(pydantic.BaseModel):
    directories: list[Directory]
    type: str = "directories"


if pydantic.__version__.startswith("2."):
    label = "pydantic v2"

    def encode(obj):
        return obj.model_dump_json(exclude_defaults=True)

    def decode(msg):
        return Directories.model_validate_json(msg)

else:
    label = "pydantic v1"

    def encode(obj):
        return obj.json(exclude_defaults=True)

    def decode(msg):
        return Directories.parse_raw(msg)
