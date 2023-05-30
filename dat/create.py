import os
# from dat.format.wiki import format_wiki
from dat.format.dat import format_dat
from dat.metadata import file_metadata
# from dat.sign import sign_message

BUFFER_SIZE = 1024 * 1024


def create_dat(path_names):
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

    # if format == "wiki":
    #     message = format_wiki(info, name)
    # elif format == "dat":
    message = format_dat(info, name)
    
    print(message)

    # signed = sign_message(message, format)

    # print(info)
    # print(signed)
