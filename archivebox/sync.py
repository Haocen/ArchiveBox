#!/usr/bin/env python3

from argparse import ArgumentParser
from os import listdir
from os.path import exists, join
from shutil import rmtree
from datetime import datetime

from config import ARCHIVE_DIR, OUTPUT_DIR
from index import (parse_json_links_index, parse_json_link_index,
                   load_links_index, write_links_index)
from links import validate_links


def sync_index() -> None:
    if not exists(join(OUTPUT_DIR, 'index.json')):
        exit('index.json is missing; nothing to do')

    links = parse_json_links_index(OUTPUT_DIR)

    all_archived_urls = []
    links_missing_archive_dir = []
    archive_dirs_missing_link = listdir(ARCHIVE_DIR)

    for idx, link in enumerate(links):
        all_archived_urls.append(link['url'])

        if link['timestamp'] in archive_dirs_missing_link:
            archive_dirs_missing_link.remove(link['timestamp'])
            data_dir = join(ARCHIVE_DIR, link['timestamp'])
            if len(listdir(data_dir)) == 0:
                links_missing_archive_dir.append((idx, link))
                rmtree(data_dir)
        else:
            links_missing_archive_dir.append((idx, link))

    print('Found {}/{} urls without archive folder or archive folder is empty:'.format(len(links_missing_archive_dir), len(links)))

    for idx, link in links_missing_archive_dir:
        print('Resetting {url} to not yet archived'.format(url=link['url']))
        links[idx] = {
            'tags': link.get('tags'),
            'sources': link.get('sources') or [],
            'url': link.get('url') or '',
            'title': link.get('title'),
            'timestamp': link.get('timestamp') or str(datetime.now().timestamp())
        }

    write_links_index(OUTPUT_DIR, links, finished=True)

    print('Found {} folders missing from index:'.format(len(archive_dirs_missing_link)))

    for d in archive_dirs_missing_link:
        data_dir = join(ARCHIVE_DIR, d)
        if len(listdir(data_dir)) == 0:
            print('Folder {folder} is empty, deleting'.format(folder=d))
            rmtree(data_dir)
        else:
            link = parse_json_link_index(data_dir)
            if link.get('url') != None and link['url'] in all_archived_urls:
                print('Folder {folder} contain duplicated archive of {url}, deleting'.format(folder=d, url=link['url']))
                rmtree(data_dir)
            elif link.get('url') != None:
                print('Folder {folder} contain archive of {url} but missing from index, adding'.format(folder=d, url=link['url']))
                links.append(link)
                validate_links(links)
                write_links_index(out_dir=OUTPUT_DIR, links=links, finished=True)
            else:
                print('Cannot detect {folder} content, skipping'.format(folder=d))


if __name__ == '__main__':
    p = ArgumentParser('Index syncing tool')

    sync_index()
