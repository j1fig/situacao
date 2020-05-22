import datetime
import os

from bs4 import BeautifulSoup
import pdftotext
import requests

import parse
import settings


def _report_filename(date):
    return os.path.join(settings.CACHE_DIR, date.isoformat() + ".pdf")


def _crawl():
    r = requests.get(settings.URL)
    s = BeautifulSoup(r.content, "html.parser")
    anchors = [
        a for a in s.find_all("a") if a.text.startswith(settings.LINK_TEXT_PREFIX)
    ]
    reports = {}
    for a in anchors:
        day, month, year = [int(t) for t in a.text.split(" | ")[-1].split("/")]
        if year == 2:
            year = 2020  # fixes 29th of April.
        url = a.get("href")
        date = datetime.date(year, month, day)
        if date < max(
            settings.FIRST_REPORT_WITH_MUNICIPAL_DATA, settings.FIRST_SUPPORTED_REPORT
        ):
            # there have been multiple versions prior to the 24th of March
            # but we really only care from that onwards as there is more data
            # granularity in those.
            continue
        reports[date] = url
    return reports


def _maybe_fetch(reports):
    fetched = 0
    for d, url in reports.items():
        report_path = _report_filename(d)
        if os.path.exists(report_path):
            continue
        with open(report_path, "wb") as f:
            r = requests.get(url)
            f.write(r.content)
            fetched += 1
    return fetched


def _extract_text(reports):
    text = {}
    for d in reports:
        p = _report_filename(d)
        with open(p, "rb") as f:
            pdf = pdftotext.PDF(f, raw=True)
            try:
                text[d] = pdf[2]
            except Exception:
                continue
    return text


def command_concelho(args):
    reports = _crawl()
    print(f"found {len(reports)} interesting reports.")
    fetched = _maybe_fetch(reports)
    if fetched:
        print(f"fetched {fetched} missing reports.")
    text = _extract_text(reports)
    dataset = parse.from_text(text)
    for d, c in dataset["Cascais"].items():
        print(f"{d.isoformat()}: {c}")


def add_concelho(sub_parser):
    concelho_parser = sub_parser.add_parser(
        "concelho",
        help="interact with municipality data. (only from 2020-04-09 onwards)",
    )
    console_parser.set_defaults(command=command_concelho)
    console_parser.add_argument(
        "name", help="Municipality name.",
    )
