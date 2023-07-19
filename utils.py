from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileDescription:
    """Description of a file.

    Attributes:
        name (str): the name of the file
        size_bytes (int): the size of the file in bytes
        modification_time (float): the modification time of the file
    """

    name: str
    size_bytes: int
    modification_time: float

    @property
    def modification_time_str(self) -> str:
        """Get modification time as string in format: YYYY-MM-DD HH:MM:SS.

        Returns:
            str: modification time as string
        """
        return datetime.datetime.fromtimestamp(self.modification_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )


def get_list_of_files(data_path: Path) -> list[FileDescription]:
    """Get list of files in data path.

    Args:
        data_path (Path): path to data directory

    Returns:
        list[FileDescription]: list of files in data directory
    """
    files: list[FileDescription] = []
    file: Path
    for file in data_path.iterdir():
        if not file.is_file():
            # print("fake file")
            continue
        files.append(
            FileDescription(
                name=file.name,
                size_bytes=file.stat().st_size,
                modification_time=file.stat().st_mtime,
            )
        )

    return files
