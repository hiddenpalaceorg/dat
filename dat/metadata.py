import hashlib
import zlib
import os
import platform
import logging
import magic
from datetime import datetime
from pathlib import Path
from dat.exceptions import DatException
from dat.version import PACKAGE_VERSION, PROTOCOL_VERSION, git_hash

BUFFER_SIZE = 1024 * 1024

logger = logging.getLogger(__name__)


def file_metadata(path_names):
    output = []

    for path_name in path_names:
        path = Path(path_name)
        root = os.path.dirname(path)

        if path.is_dir():
            paths = []

            for (dir, _, files) in os.walk(path):
                for file_name in files:
                    paths.append(os.path.join(dir, file_name))

        elif path.is_file():
            paths = [path_name]

        else:
            raise DatException(f"Invalid file: {path_name}")

        for path_name in sorted(paths):
            relative_path = os.path.normpath(os.path.relpath(path_name, root))

            logger.info(f"Processing {relative_path}...")
            info = {
                "file": relative_path,
                "size": os.path.getsize(path_name),
                "hashes": hashes(path_name),
                "type": file_type(path_name),
                "datetimes": dates(path_name),
            }
            output.append(info)

    return output


def hashes(filename):
    hashes = {}
    digests = {}

    crc32 = 0

    for algorithm in ("md5", "sha1", "sha256"):
        hashes[algorithm] = getattr(hashlib, algorithm)()

    with open(filename, "rb") as file:
        while chunk := file.read(BUFFER_SIZE):
            for hash in hashes.values():
                hash.update(chunk)

            crc32 = zlib.crc32(chunk, crc32)

    for algorithm, hash in hashes.items():
        digests[algorithm] = hash.hexdigest()

    digests["crc32"] = f"{crc32:x}"

    return digests


def dates(filename):
    mtime = os.path.getmtime(filename)

    if platform.system() == "Windows":
        ctime = os.path.getctime(filename)
    else:
        try:
            ctime = os.stat(filename).st_birthtime
        except AttributeError:
            ctime = None

    return {
        "created": format_timestamp(ctime),
        "modified": format_timestamp(mtime),
    }


def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def file_type(filename):
    description = magic.from_file(filename)

    return description.partition(":")[0]
