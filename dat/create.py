import os
from dat.format.wiki import format_wiki
from dat.format.xml import format_xml
from dat.metadata import file_metadata
from dat.sign import sign_message

BUFFER_SIZE = 1024 * 1024


def create_dat(path_names, format):
    info = file_metadata(path_names)

    if len(path_names) == 1:
        path = path_names[0]
        relative_path = os.path.relpath(path, os.path.dirname(path))

        partition = relative_path.rpartition(".")
        if partition[0]:
            name = partition[0]
        else:
            name = partition[-1]
    else:
        name = ""

    if format == "wiki":
        message = format_wiki(info, name)
    elif format == "xml":
        message = format_xml(info, name)

    signed = sign_message(message, format)
    print(signed)
