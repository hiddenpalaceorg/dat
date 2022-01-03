from importlib import metadata
import subprocess


PACKAGE_VERSION = metadata.version("dat")
PROTOCOL_VERSION = 1


def git_hash():
    output = subprocess.check_output(["git", "rev-parse", "HEAD"])
    return output.decode("ascii").strip()


def version_string():
    return f"dat {PACKAGE_VERSION} ({PROTOCOL_VERSION}, {git_hash()})"
