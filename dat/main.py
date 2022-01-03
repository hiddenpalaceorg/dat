import argparse

from dat.exceptions import DatException


def main():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(
        title="subcommands", dest="command", metavar="COMMAND"
    )

    subparser = subparsers.add_parser("create", help="Create a dat")
    subparser.add_argument("file", nargs="+", help="files to process")
    subparser.add_argument("--format", "-f", choices=["wiki", "xml"], default="wiki")

    subparser = subparsers.add_parser(
        "generate-keys", help="Generate a key pair for signing dats"
    )
    subparser.add_argument(
        "--user", "-u", required=True, help="User name of the signer"
    )

    args = parser.parse_args()

    try:
        if args.command == "create":
            from dat.create import create_dat

            create_dat(args.file, args.format)

        elif args.command == "generate-keys":
            from dat.keys import generate_keys

            generate_keys(args.user)

        else:
            parser.print_help()

    except DatException as e:
        print(f"\nError:\n{e}")
