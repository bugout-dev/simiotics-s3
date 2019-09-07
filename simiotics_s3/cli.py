"""
Command line interface for the simiotics_s3 tool
"""

import argparse

from simiotics.client import client_from_env
from simiotics.registry.data_pb2 import *

from . import data, sources

def parse_sources_list(args: argparse.Namespace) -> None:
    """
    Handler for the "sources list" command
    """
    simiotics_client = client_from_env()
    registered_sources = sources.list_data_sources(simiotics_client, args.offset, args.num_items)
    print('*** Sources ***')
    for i, source in enumerate(registered_sources):
        print('*** Source {} ***'.format(args.offset + i))
        print(source)

def parse_sources_get(args: argparse.Namespace) -> None:
    """
    Handler for the "sources get" command
    """
    simiotics_client = client_from_env()
    registered_source = sources.get_data_source(simiotics_client, args.id)
    print('*** Source ***')
    print(registered_source)

def parse_sources_update(args: argparse.Namespace) -> None:
    """
    Handler for the "sources update" command
    """
    simiotics_client = client_from_env()
    registered_source = sources.update_data_source(simiotics_client, args.id, args.message)
    print('*** Source ***')
    print(registered_source)

def parse_sources_create(args: argparse.Namespace) -> None:
    """
    Handler for the "sources create" command
    """
    simiotics_client = client_from_env()
    registered_source = sources.create_data_source(simiotics_client, args.id, args.s3_path)
    print('*** Source registered ***')
    print(registered_source)

def parse_data_describe(args: argparse.Namespace) -> None:
    """
    Handler for the "data describe" command
    """
    simiotics_client = client_from_env()
    data_descriptions = data.describe_data(simiotics_client, args.source, args.ids)
    print('*** Data descriptions ***')
    for i, description in enumerate(data_descriptions):
        print('*** Sample {} ***'.format(i))
        print(description)

def parse_data_download(args: argparse.Namespace) -> None:
    """
    Handler for the "data download" command
    """
    simiotics_client = client_from_env()
    paths = data.download_data(simiotics_client, args.source, args.ids, args.dir)
    for path in paths:
        print(path)

def parse_data_register(args: argparse.Namespace) -> None:
    """
    Handler for the "data register" command
    """
    simiotics_client = client_from_env()
    responses = data.register_data(simiotics_client, args.source, args.files)
    print('*** Data registration ***')
    for i, response in enumerate(responses):
        print('*** Sample {} ***'.format(i))
        print(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Define and interact with Simiotics S3 data registries')
    subparsers = parser.add_subparsers(
        title='Actions',
        help='Define sources, and add and retrieve data from those sources',
    )

    sources_subcommand = subparsers.add_parser('sources')
    sources_subparser = sources_subcommand.add_subparsers(
        title='Data sources',
        help='Register, list, signal updates, and get descriptions of sources of data'
    )

    sources_create = sources_subparser.add_parser('create', help='Create a source')
    sources_create.add_argument(
        '-i',
        '--id',
        required=True,
        help='An identifier for the source -- this must be unique over all registered sources',
    )
    sources_create.add_argument(
        '-p',
        '--s3-path',
        required=True,
        help='S3 path under which individual samples are stored',
    )
    sources_create.set_defaults(func=parse_sources_create)

    sources_get = sources_subparser.add_parser('get', help='Get a previously created source')
    sources_get.add_argument(
        '-i',
        '--id',
        required=True,
        help='An identifier for the source -- this must be unique over all registered sources',
    )
    sources_get.set_defaults(func=parse_sources_get)

    sources_update = sources_subparser.add_parser('update', help='Mark an update to a source')
    sources_update.add_argument(
        '-i',
        '--id',
        required=True,
        help='An identifier for the source -- this must be unique over all registered sources',
    )
    sources_update.add_argument(
        '-m',
        '--message',
        help='Update message -- specifies the nature of the update',
    )
    sources_update.set_defaults(func=parse_sources_update)

    sources_list = sources_subparser.add_parser('list', help='List previously created sources')
    sources_list.add_argument(
        '-o',
        '--offset',
        type=int,
        default=0,
        help='Offset from which listing should start',
    )
    sources_list.add_argument(
        '-n',
        '--num-items',
        type=int,
        default=10,
        help='Number of items to list',
    )
    sources_list.set_defaults(func=parse_sources_list)

    data_subcommand = subparsers.add_parser('data')
    data_subparser = data_subcommand.add_subparsers(
        title='Data samples',
        help='Register data against a Simiotics source and download datasets from that source'
    )

    data_describe = data_subparser.add_parser('describe', help='Describe the data in a data source')
    data_describe.add_argument(
        '-s',
        '--source',
        required=True,
        help='ID of the source'
    )
    data_describe.add_argument(
        '-i',
        '--ids',
        nargs='*',
        help='Optional IDs for data samples that you would like to restrict to in the description'
    )
    data_describe.set_defaults(func=parse_data_describe)

    data_download = data_subparser.add_parser('download', help='Describe the data in a data source')
    data_download.add_argument(
        '-s',
        '--source',
        required=True,
        help='ID of the source'
    )
    data_download.add_argument(
        '-i',
        '--ids',
        nargs='*',
        help='Optional IDs for data samples that you would like to restrict to in the description',
    )
    data_download.add_argument(
        '-d',
        '--dir',
        default='./',
        help='Directory into which data should be downloaded (defaults to current directory)',
    )
    data_download.set_defaults(func=parse_data_download)

    data_register = data_subparser.add_parser('register', help='Register data against a source')
    data_register.add_argument(
        '-s',
        '--source',
        required=True,
        help='ID of the source',
    )
    data_register.add_argument(
        'files',
        nargs='+',
        help='Paths describing local files to be uploaded',
    )
    data_register.set_defaults(func=parse_data_register)

    args = parser.parse_args()
    args.func(args)
