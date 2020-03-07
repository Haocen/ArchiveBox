#!/usr/bin/env python3

import re
from argparse import ArgumentParser
from os.path import exists, join
from shutil import rmtree
from typing import (List, Pattern)

from config import ARCHIVE_DIR, OUTPUT_DIR
from index import (parse_json_links_index, write_links_index)


def cleanup_index(exact_link: str, regexes: List[str], proceed: bool, delete: bool) -> None:
    if not exists(join(OUTPUT_DIR, 'index.json')):
        exit('index.json is missing; nothing to do')

    compiled = [re.compile(r) for r in regexes]
    links = parse_json_links_index(OUTPUT_DIR)
    filtered = []
    remaining = []

    for l in links:
        url = l['url']
        for r in compiled:
            if r.search(url):
                filtered.append((l, r))
                break
        else:
            if url == exact_link:
                filtered.append((l, exact_link))
            else:
                remaining.append(l)

    if not filtered:
        exit('Search did not match any entries.')

    print('Filtered out {}/{} urls:'.format(len(filtered), len(links)))

    for link, regex_or_exact_link in filtered:
        url = link['url']
        print(' {url} via {match}'.format(
            url=url,
            match=regex_or_exact_link.pattern if isinstance(regex_or_exact_link, Pattern) else regex_or_exact_link
        ))

    if not proceed:
        answer = input('Remove {} entries from index? [y/n] '.format(
            len(filtered)))
        proceed = answer.strip().lower() in ('y', 'yes')

    if not proceed:
        exit('Aborted')

    write_links_index(OUTPUT_DIR, remaining, finished=True)


    if delete:
        for link, _ in filtered:
            data_dir = join(ARCHIVE_DIR, link['timestamp'])
            if exists(data_dir):
                rmtree(data_dir)


if __name__ == '__main__':
    p = ArgumentParser('Index purging tool')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        'link',
        nargs='?',
        type=str,
        help='URL matching exactly with this link will be removed from the index.'
    )
    g.add_argument(
        '--regex',
        '-r',
        action='append',
        default=[],
        help='Regular expression matching URLs to purge',
    )
    p.add_argument(
        '--delete',
        '-d',
        action='store_true',
        default=False,
        help='Delete webpage files from archive',
    )
    p.add_argument(
        '--yes',
        '-y',
        action='store_true',
        default=False,
        help='Do not prompt for confirmation',
    )

    args = p.parse_args()
    if args.regex or args.link:
        cleanup_index(exact_link=args.link, regexes=args.regex, proceed=args.yes, delete=args.delete)
    else:
        p.print_help()
