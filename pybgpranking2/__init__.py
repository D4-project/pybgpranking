#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys

from .api import PyBGPRanking

from urllib.parse import urljoin
from pyipasnhistory import IPASNHistory
from datetime import date, timedelta


def main():
    parser = argparse.ArgumentParser(description='Run a query against BGP Ranking')
    parser.add_argument('--url', type=str, help='URL of the instance.')
    parser.add_argument('--date', default=date.today().isoformat(), help='Date of the dataset required')

    sub_parsers = parser.add_subparsers(title='Available commands', dest='command')

    index_query = sub_parsers.add_parser('index')
    index_query.add_argument('--limit', default=100, help='Max number of ASN to get')
    index_query.add_argument('--family', default='v4', help='v4 or v6')
    index_query.set_defaults(which='index')

    simple_query = sub_parsers.add_parser('simple')
    group = simple_query.add_mutually_exclusive_group(required=True)
    group.add_argument('--asn', help='ASN to lookup')
    group.add_argument('--ip', help='IP to lookup')
    simple_query.set_defaults(which='simple')

    status_query = sub_parsers.add_parser('status')

    group = status_query.add_mutually_exclusive_group(required=True)
    group.add_argument('--redis_up', action='store_true', help='Check if redis is up.')

    args = parser.parse_args()

    if args.url:
        bgpranking = PyBGPRanking(args.url)
        ipasn = IPASNHistory(urljoin(args.url, 'ipasn_history'))
    else:
        bgpranking = PyBGPRanking()
        ipasn = IPASNHistory()

    if not bgpranking.is_up:
        print(f'Unable to reach {bgpranking.root_url}. Is the server up?')
        sys.exit(1)

    if args.command == 'simple':
        if args.ip:
            response = ipasn.query(args.ip)
            print(json.dumps(response, indent=2))
            if 'response' in response and response['response']:
                asn = response['response'][list(response['response'].keys())[0]]['asn']
        else:
            asn = args.asn

        response = bgpranking.query(asn, date=(date.today() - timedelta(1)).isoformat())
    elif args.command == 'index':
        response = bgpranking.asns_global_ranking(address_family=args.family, limit=args.limit, date=args.date)
    elif args.command == 'status':
        if args.redis_up:
            response = bgpranking.redis_up()

    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main()
