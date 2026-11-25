from dataclasses import dataclass
from datetime import date
from re import fullmatch

from src.object_catalog.errors import DuplicateError, InvalidItemError
from src.object_catalog.utils import time_format


@dataclass
class MediaItem:
    id: str
    name: str
    category: str
    date: date
    source: str

    @staticmethod
    def str_validate(value: str, field_name: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidItemError(f"{field_name} must be a non-empty string")

    @staticmethod
    def int_validate(value: int, field_name: str) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidItemError(f"{field_name} must be an integer")

    def __post_init__(self):
        self.str_validate(value=self.id, field_name="ID")
        self.str_validate(value=self.name, field_name="Name")
        self.str_validate(value=self.category, field_name="Category")
        self.str_validate(value=self.source, field_name="Source")

        if not isinstance(self.date, date):
            raise InvalidItemError("Date must be a datetime.date instance")

    def __str__(self) -> str:
        return f"| ID: {self.id} | Name: {self.name} | Category: {self.category} | Source: {self.source} | Date: {self.date} |"


@dataclass
class VideoItem(MediaItem):
    duration_seconds: int
    resolution: str

    def __post_init__(self):
        super().__post_init__()

        self.int_validate(value=self.duration_seconds, field_name="Duration")

        if self.duration_seconds < 0:
            raise InvalidItemError("Duration must be a not negative integer")

        if not isinstance(self.resolution, str) or fullmatch(r"[1-9][0-9]*[xX][1-9][0-9]*", self.resolution) is None:
            raise InvalidItemError("Resolution must be a string like \"[WIDTH]x[HEIGHT]\"")

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} Duration: {time_format(self.duration_seconds)} | Resolution: {self.resolution} |"


@dataclass
class AudioItem(MediaItem):
    duration_seconds: int
    artist: str | None = None
    album: str | None = None


    def __post_init__(self):
        super().__post_init__()

        self.int_validate(value=self.duration_seconds, field_name="Duration")

        if self.duration_seconds < 0:
            raise InvalidItemError("Duration must be a not negative integer")

        if self.artist is not None:
            self.str_validate(value=self.artist, field_name="Artist")

        if self.album is not None:
            self.str_validate(value=self.album, field_name="Album")

    def  __str__(self) -> str:
        base_str = super().__str__()
        parts = [base_str, f" Duration: {time_format(self.duration_seconds)} |"]

        if self.artist is not None:
            parts.append(f" Artist: {self.artist} |")

        if self.album is not None:
            parts.append(f" Album: {self.album} |")

        return "".join(parts)


@dataclass
class MediaCatalog:
    data: dict[str, MediaItem]
    categories: dict[str, list[str]]
    names: dict[str, list[str]]

    def __len__(self) -> int:
        return len(self.data)
    
    def __iter__(self):
        return iter(self.data.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.data

    def add(self, item: MediaItem) -> None:
        if not isinstance(item, MediaItem):
            raise InvalidItemError("Trying to insert not a MediaObject in catalog")

        if self.__contains__(item.id):
            raise DuplicateError(f"Trying to insert object with existing id \"{item.id}\" in catalog")

        self.data[item.id] = item
            

