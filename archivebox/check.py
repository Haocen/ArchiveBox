#!/usr/bin/env python3

from argparse import ArgumentParser
from os import listdir
from os.path import exists, join

from config import ARCHIVE_DIR, OUTPUT_DIR
from index import (parse_json_links_index)


def check_index() -> None:
    if not exists(join(OUTPUT_DIR, 'index.json')):
        exit('index.json is missing; nothing to do')

    links = parse_json_links_index(OUTPUT_DIR)

    links_missing_archive_dir = []
    archive_dirs_missing_link = listdir(ARCHIVE_DIR)

    for l in links:
        if l['timestamp'] in archive_dirs_missing_link:
            archive_dirs_missing_link.remove(l['timestamp'])
            data_dir = join(ARCHIVE_DIR, l['timestamp'])
            if len(listdir(data_dir)) == 0:
                links_missing_archive_dir.append(l)
        else:
            links_missing_archive_dir.append(l)

    print('Found {}/{} urls without archive folder:'.format(len(links_missing_archive_dir), len(links)))

    for l in links_missing_archive_dir:
        print(' {url} is missing folder {folder}'.format(url=l['url'], folder=l['timestamp']))

    print('Found {} folders missing from index:'.format(len(archive_dirs_missing_link)))

    for d in archive_dirs_missing_link:
        print(' {folder} does not exist in index'.format(folder=d))


if __name__ == '__main__':
    p = ArgumentParser('Index checking tool')
    
    check_index()