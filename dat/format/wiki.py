import os
from datetime import datetime
from dat.format.xml import format_xml
from dat.version import version_string
from dat.keys import user_name


def format_wiki(info, name):
    xml = format_xml(info, name)
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    output = []

    output.append("{{Dat")
    output.append("|entries=")

    for index, entry in enumerate(info):
        path = entry["file"]
        indent = len(path.split(os.path.sep)) - 1

        args = {
            "i": str(index + 1),
            "indent": str(indent),
            "filename": path,
            "type": entry["type"],
            "size": entry["size"],
            "modified": entry["datetimes"]["modified"],
            "created": entry["datetimes"]["created"],
            "crc32": entry["hashes"]["crc32"],
            "md5": entry["hashes"]["md5"],
            "sha1": entry["hashes"]["sha1"],
            "sha256": entry["hashes"]["sha256"],
        }
        args = "|".join([f"{key}={value}" for (key, value) in args.items()])

        output.append(f" {{{{DatEntry|{args}}}}}")

    output.append(f"|xml=<nowiki>{xml}</nowiki>")
    output.append(f"|version={version_string()}")
    output.append(f"|generated_by={user_name()}")
    output.append(f"|generated_at={created}")

    output.append("}}")

    return "\n".join(output)
