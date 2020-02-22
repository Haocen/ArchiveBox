#!/usr/bin/env python3

from argparse import ArgumentParser
from os.path import exists, join

from config import ARCHIVE_DIR, OUTPUT_DIR
from index import (parse_json_links_index, write_html_links_index)


def generate_index() -> None:
    if not exists(join(OUTPUT_DIR, 'index.json')):
        exit('index.json is missing; nothing to do')

    links = parse_json_links_index(OUTPUT_DIR)
    write_html_links_index(OUTPUT_DIR, links, True)


if __name__ == '__main__':
    p = ArgumentParser('HTML index generating tool')

    generate_index()
