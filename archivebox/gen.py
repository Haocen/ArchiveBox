#!/usr/bin/env python3

from argparse import ArgumentParser
from os.path import exists, join

from config import ARCHIVE_DIR, OUTPUT_DIR
from index import (parse_json_links_index, write_html_links_index)
from logs import (
    log_indexing_started,
    log_indexing_finished
)


def generate_index() -> None:
    if not exists(join(OUTPUT_DIR, 'index.json')):
        exit('index.json is missing; nothing to do')

    links = parse_json_links_index(OUTPUT_DIR)
    
    log_indexing_started(OUTPUT_DIR, 'index.html')
    write_html_links_index(OUTPUT_DIR, links, finished=True)
    log_indexing_finished(OUTPUT_DIR, 'index.html')


if __name__ == '__main__':
    p = ArgumentParser('HTML index generating tool')

    generate_index()
