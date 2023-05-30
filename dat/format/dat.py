import xml.etree.ElementTree as ET


def format_dat(metadata, name):
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
    
    # print(ET.tostring(game, encoding="unicode"))
    # print('-')
    
    # s = ET.tostring(game, encoding="unicode")
    
    # parse_dat(s)
    # x  = ET.fromstring(s)
    
    # print(ET.tostring(x, encoding="unicode"))
    # print('-')
    
    # raise 0
    
    return ET.tostring(datafile, encoding="unicode")


def parse_dat(dat):
    from lxml import etree
    parser = etree.XMLParser(remove_blank_text=True)
    elem = etree.XML(dat, parser=parser)
    print(etree.tostring(elem))

