"""
Data-related functionality for simiotics_s3 tool
"""
import os
from typing import Iterator, List, Optional, Tuple
import uuid

import boto3
from simiotics.client import Simiotics
import simiotics.registry.data_pb2 as data_pb2

from . import sources

def describe_data(
        simiotics_client: Simiotics,
        source_id: str,
        data_ids: Optional[List[str]],
    ) -> Iterator[data_pb2.Datum]:
    """
    Describe data registered under a source in a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source under which the data is registered
    data_ids
        Optional IDs for the data samples you would like to restrict the description to

    Returns: Iterator over the data descriptions
    """
    request = data_pb2.GetDataRequest(
        version=simiotics_client.client_version,
        source_id=source_id,
    )
    if data_ids is not None:
        request.ids.extend(data_ids)

    responses = simiotics_client.data_registry.GetData(request)

    return (response.datum for response in responses)

def download_data(
        simiotics_client: Simiotics,
        source_id: str,
        data_ids: Optional[List[str]],
        target_dir: str,
    ) -> Iterator[str]:
    """
    Describe data registered under a source in a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source under which the data is registered
    data_ids
        Optional IDs for the data samples you would like to restrict the description to
    target_dir
        Directory into which data should be downloaded

    Returns: Iterator over the data descriptions
    """
    request = data_pb2.GetDataRequest(
        version=simiotics_client.client_version,
        source_id=source_id,
    )
    if data_ids is not None:
        request.ids.extend(data_ids)

    responses = simiotics_client.data_registry.GetData(request)

    s3_client = boto3.client('s3')

    paths = []
    for response in responses:
        datum = response.datum

        object_path = datum.content[len('s3://'):].split('/')
        bucket = object_path[0]
        key = '/'.join(object_path[1:])

        target_filename = object_path[-1]
        target_filepath = os.path.join(target_dir, target_filename)
        try:
            s3_client.download_file(bucket, key, target_filepath)
            paths.append(target_filepath)
        except Exception as err:
            print(str(err))

    return paths

def register_data(
        simiotics_client: Simiotics,
        source_id: str,
        files: List[str],
        tags: List[Tuple[str, str]]
    ) -> Iterator[data_pb2.RegisterDataResponse]:
    """
    Register files under a source in a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source under which the data is registered
    files
        Paths to files that should be registered
    tags
        List of key-value ordered pairs representing the tags that should be associated to each
        of the files when registered against the data registry

    Returns: Iterator over the responses to the registration requests
    """
    source = sources.get_data_source(simiotics_client, source_id)
    source_root = source.data_access_spec
    s3_prefix = 's3://'
    if source_root[:len(s3_prefix)] == s3_prefix:
        source_root = source_root[len(s3_prefix):]
    split_root = source_root.split('/')
    bucket = split_root[0]
    root_from_bucket = ''
    if len(split_root) > 1:
        root_from_bucket = '/'.join(split_root[1:])

    s3_client = boto3.client('s3')

    def request_iterator():
        for data_file in files:
            datum_id = str(uuid.uuid4())
            key = os.path.join(root_from_bucket, datum_id)
            successful = False
            try:
                s3_client.upload_file(
                    data_file,
                    bucket,
                    key,
                    ExtraArgs={
                        'Metadata': {
                            'filename': data_file,
                        },
                    },
                )
                successful = True
            except Exception as err:
                print(str(err))

            if successful:
                tags['filename'] = data_file
                datum = data_pb2.Datum(
                    id=datum_id,
                    source=source,
                    content='s3://{}/{}'.format(bucket, key),
                    tags=tags,
                )
                request = data_pb2.RegisterDataRequest(
                    version=simiotics_client.client_version,
                    datum=datum,
                )
                yield request

    responses = simiotics_client.data_registry.RegisterData(request_iterator())

    return responses
