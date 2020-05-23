from . import minsaude
from . import parse
from . import pdf
from . import settings
from . import util


def command_concelho(args):
    reports = minsaude.crawl()
    print(f"found {len(reports)} interesting reports.")
    fetched = minsaude.maybe_fetch(reports)
    if fetched:
        print(f"fetched {fetched} missing reports.")
    text = pdf.extract_text(reports)
    dataset = parse.from_text(text)
    m = args.name
    if m not in dataset:
        util.abort(f"unknown municipality: {m}. tip: run `situacao concelho --list` for a full list of available municipalities.")
    for d, c in dataset[m].items():
        print(f"{d.isoformat()}: {c}")


def add_concelho(sub_parser):
    concelho_parser = sub_parser.add_parser(
        "concelho",
        help="interact with municipality data. (only from 2020-04-09 onwards)",
    )
    concelho_parser.set_defaults(command=command_concelho)
    concelho_parser.add_argument(
        "name", help="Municipality name.",
    )
