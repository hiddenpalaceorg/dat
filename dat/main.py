import argparse
import logging

from dat.exceptions import DatException

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser(description="")
    # subparsers = parser.add_subparsers(
    #     title="subcommands", dest="command", metavar="COMMAND"
    # )

    # subparser = subparsers.add_parser("create", help="Create a dat")
    parser.add_argument("file", nargs="+", help="files to process")
    # subparser.add_argument("--format", "-f", choices=["wiki", "dat"], default="dat")

    # subparser = subparsers.add_parser("verify", help="Verify a message")
    # subparser.add_argument("file", help="file to verify")

    # subparser = subparsers.add_parser(
    #     "generate-keys", help="Generate a key pair for signing dats"
    # )
    # subparser.add_argument(
    #     "--user", "-u", required=True, help="User name of the signer"
    # )

    args = parser.parse_args()

    try:
        if True or args.command == "create":
            from dat.create import create_dat

            # create_dat(args.file, args.format)
            create_dat(args.file)

        elif args.command == "verify":
            from dat.verify import verify_file

            verify_file(args.file)

        elif args.command == "generate-keys":
            from dat.keys import generate_keys

            generate_keys(args.user)

        else:
            parser.print_help()

    except DatException as e:
        logger.error(f"\nError:\n{e}")
