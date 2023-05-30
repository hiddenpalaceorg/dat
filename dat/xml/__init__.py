import xml.etree.ElementTree as ET


def create_dat(metadata, name):
    datafile = ET.Element("datafile")
    
    game = ET.SubElement(datafile, "game", name=name)

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

    ET.indent(datafile, level=0)
    # print(ET.tostring(datafile, encoding="unicode"))
    return ET.tostring(datafile, encoding="unicode")