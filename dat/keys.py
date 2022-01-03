from genericpath import exists
import os
import logging
from pathlib import Path
from datetime import datetime
from collections import namedtuple

from nacl.signing import SigningKey
import yaml
from dat.base64_encoder import UnpaddedBase64Encoder
from dat.exceptions import DatException

from dat.version import version_string

logger = logging.getLogger(__name__)


def generate_keys(user_name):
    path = key_path()

    if os.path.exists(path):
        raise DatException(
            f"Keys are already generated: {path} already exists. If you are SURE you want to generate a new pair, delete that file and run this command again.\n\nWARNING: this will obliterate your secret key forever if you don't have a backup."
        )

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as yaml_file:
        key = SigningKey.generate()

        secret = UnpaddedBase64Encoder.encode(bytes(key)).decode()
        public = key.verify_key.encode(encoder=UnpaddedBase64Encoder).decode()
        contents = {
            "user_name": user_name,
            "created": datetime.now().isoformat(),
            "version": version_string(),
            "secret": secret,
            "public": public,
        }

        yaml_file.write(yaml.dump(contents))

        logger.info(f"Successfully generated {path}")


KeyInfo = namedtuple("KeyInfo", ["key", "user_name"])


def load_secret_key():
    contents = load_yaml()

    key = SigningKey(seed=contents["secret"].encode(), encoder=UnpaddedBase64Encoder)

    return KeyInfo(key=key, user_name=contents["user_name"])


def user_name():
    contents = load_yaml()

    return contents["user_name"]


def load_yaml():
    path = key_path()

    if not os.path.isfile(path):
        raise DatException(
            f"Key file at {path} not found. Please generate by running\n\n    dat generate-keys --user YOUR_USER_NAME"
        )

    with open(path) as yaml_file:
        contents = yaml.safe_load(yaml_file.read())

        return contents


def key_path():
    return Path.home() / ".dat" / "key.yaml"
