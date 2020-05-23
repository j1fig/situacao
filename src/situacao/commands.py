from yaspin import yaspin

from . import minsaude
from . import parse
from . import pdf
from . import settings
from . import util


def command_concelho(args):
    sp = yaspin()
    sp.color = 'blue'
    sp.start()
    sp.text = "checking min-saude.pt..."
    reports = minsaude.crawl()
    sp.write(f"> found {len(reports)} interesting reports.")
    sp.text = "downloading missing reports..."
    fetched = minsaude.maybe_fetch(reports)
    if fetched:
        sp.write(f"> fetched {fetched} missing reports.")
    sp.text = "parsing PDF reports..."
    text = pdf.extract_text(reports)
    dataset = parse.from_text(text)
    m = args.name
    if m not in dataset:
        sp.red.fail("✘")
        util.abort(f"unknown municipality: {m}. tip: run `situacao concelho --list` for a full list of available municipalities.")
    for d, c in dataset[m].items():
        sp.write(f"{d.isoformat()}: {c}")
    sp.text = 'success!'
    sp.green.ok("✔")


def add_concelho(sub_parser):
    concelho_parser = sub_parser.add_parser(
        "concelho",
        help="interact with municipality data. (only from 2020-04-09 onwards)",
    )
    concelho_parser.set_defaults(command=command_concelho)
    concelho_parser.add_argument(
        "name", help="Municipality name.",
    )
