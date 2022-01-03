import xml.etree.ElementTree as ET


def format_xml(metadata, name):
    game = ET.Element("game", name=name)

    for file in metadata:
        props = {
            "name": file["file"],
            "size": str(file["size"]),
            "crc": file["hashes"]["crc32"],
            "md5": file["hashes"]["md5"],
            "sha1": file["hashes"]["sha1"],
            "sha256": file["hashes"]["sha256"],
        }
        ET.SubElement(game, "rom", **props)

    ET.indent(game, space="\t", level=0)
    return ET.tostring(game, encoding="unicode")
