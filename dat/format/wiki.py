import os
from dat.format.xml import format_xml
from dat.version import version_string
from dat.keys import user_name


def format_wiki(info, name):
    xml = format_xml(info, name)

    output = []

    output.append("{{dat")
    output.append("|entries=")

    for index, entry in enumerate(info):
        path = entry["file"]
        indent = len(path.split(os.path.sep))

        args = {
            "i": str(index + 1),
            "icon": "file",
            "indent": str(indent),
            "filename": path,
            "type": entry["type"],
            "size": entry["size"],
            "crc32": entry["hashes"]["crc32"],
            "md5": entry["hashes"]["md5"],
            "sha1": entry["hashes"]["sha1"],
            "sha256": entry["hashes"]["sha256"],
        }
        args = "|".join([f"{key}={value}" for (key, value) in args.items()])

        output.append(f" {{{{datentry|{args}}}}}")

    output.append(f"|xml=<nowiki>{xml}</nowiki>")
    output.append(f"|version={version_string()}")
    output.append(f"|generatedby={user_name()}")

    output.append("}}")

    return "\n".join(output)
