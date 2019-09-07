"""
Source-related functionality for simiotics_s3 tool
"""

from typing import Any, Iterator, List, Optional

from simiotics.client import Simiotics
import simiotics.registry.data_pb2 as data_pb2

def list_data_sources(
        simiotics_client: Simiotics,
        offset: int,
        num_items: int
    ) -> List[data_pb2.Source]:
    """
    Lists source in a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    offset
        Offset from which list should start
    num_items
        Number of items to list

    Returns: Source object
    """
    request = data_pb2.ListSourcesRequest(
        version=simiotics_client.client_version,
        offset=offset,
        num_items=num_items,
    )
    response = simiotics_client.data_registry.ListSources(request)

    return response.sources

def update_data_source(
        simiotics_client: Simiotics,
        source_id: str,
        message: str,
    ) -> data_pb2.Source:
    """
    Gets a source from a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source you would like to register
    message
        Update message signifying the nature of the marked update

    Returns: Source object
    """
    request = data_pb2.UpdateSourceRequest(
        version=simiotics_client.client_version,
        id=source_id,
        notes=message,
    )
    response = simiotics_client.data_registry.UpdateSource(request)

    return response.source

def get_data_source(
        simiotics_client: Simiotics,
        source_id: str,
    ) -> data_pb2.Source:
    """
    Gets a source from a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source you would like to register

    Returns: Source object
    """
    request = data_pb2.GetSourceRequest(
        version=simiotics_client.client_version,
        id=source_id,
    )
    response = simiotics_client.data_registry.GetSource(request)

    return response.source

def create_data_source(
        simiotics_client: Simiotics,
        source_id: str,
        s3_root: str,
    ) -> data_pb2.Source:
    """
    Registers an S3 data source against a Simiotics data registry

    Args:
    simiotics_client
        Simiotics client -- see the simiotics.client module
    source_id
        String identifying the source you would like to register
    s3_root
        Root under which all source samples may be found

    Returns: Source object
    """
    source = data_pb2.Source(
        id=source_id,
        source_type=data_pb2.Source.SourceType.SOURCE_S3,
        data_access_spec=s3_root,
    )

    request = data_pb2.RegisterSourceRequest(
        version=simiotics_client.client_version,
        source=source,
    )
    response = simiotics_client.data_registry.RegisterSource(request)

    return response.source
