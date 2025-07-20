#!/usr/bin/env python3

"""
ncbi_db.py

This module provides functions to interact with NCBI's Entrez API,
including setting up user credentials, retrieving database information,
and displaying available databases with their descriptions.

Now it is easy to query NCBI’s Entrez eInfo to list all available databases
and print a brief description for each.
"""

import time
import sys

from typing import Any, Union

from Bio import Entrez
from Bio.Entrez.Parser import (
    DictionaryElement,
    IntegerElement,
    ListElement,
    NoneElement,
    NotXMLError,
)


def set_entrez_account(email: str, api: str = None) -> None:
    """
    Set the Entrez email and API key for NCBI queries.

    Args:
        email (str): Email address to identify the user.
        api (str, optional): NCBI API key for higher rate limits.
    """
    Entrez.email = email
    if api:
        Entrez.api_key = api


def get_ncbi_dbs(
    email: str,
    api: str = None,
) -> DictionaryElement | ListElement | Any | IntegerElement | NoneElement | None:
    """
    Query NCBI's Entrez eInfo to list all available databases
    and print a brief description for each.

    Args:
        email (str): Email address to identify the user.
        api (str, optional): NCBI API key for higher rate limits.
                            Defaults to None.
    """
    set_entrez_account(email, api)

    print("Querying NCBI eInfo for available databases...")
    # Explicitly ask for XML to ensure BioPython parses correctly
    with Entrez.einfo() as handle:
        record = Entrez.read(handle)

    if not record:
        raise ValueError("No records found in NCBI eInfo response.")
    print(f"records found:\n{record}")
    return record


def get_db_info(
    db_name: str,
    email: str,
    api: str = None,
) -> DictionaryElement | ListElement | Any | IntegerElement | NoneElement | None:
    """
    Get information about a specific NCBI database.
    Args:
        db_name (str): Name of the NCBI database to query.
        email (str): Email address to identify the user.
        api (str, optional): NCBI API key for higher rate limits.
    """
    set_entrez_account(email, api)

    with Entrez.einfo(db=db_name) as handle:
        try:
            record = Entrez.read(handle)
        except NotXMLError as e:
            print(
                f"Error reading NCBI eInfo response for database '{db_name}': {e}",
                file=sys.stderr,
            )
            return None

        if not record:
            print(f"No records found for database '{db_name}'", file=sys.stderr)
            return None
        return record


def show_available_dbs(
    db_names: Union[DictionaryElement, ListElement], email: str, api: str = None
) -> None:
    """
    Print the names and descriptions of all available NCBI databases.
    Args:
        record (Union[DictionaryElement, ListElement]): Parsed NCBI eInfo response.
    """
    if not isinstance(db_names, DictionaryElement):
        raise ValueError("Expected a DictionaryElement from Entrez eInfo response.")
    if "DbList" not in db_names:
        raise ValueError("Response does not contain 'DbList'.")

    print("Available databases:")
    # record['DbList'] is a list of database names (strings)
    for db_name in db_names["DbList"]:

        info = get_db_info(db_name, email, api_key)

        print(f"\n• {db_name}")
        print("-------------------------------------------")
        print("Description:")

        if not info:
            print(
                f"Failed to retrieve information for database '{db_name}'",
                file=sys.stderr,
            )
            continue

        from utils import pretty_dict        
        pretty_dict(info)


        time.sleep(1)
if __name__ == "__main__":
    # Always tell NCBI who you are; if you have a key, set Entrez.api_key too.
    email = "-----------------------------------------TO BE FILLED MANUALLY OR FROM ENV VARS------------------------------------------------"
    api_key = "---------------------------------------TO BE FILLED MANUALLY OR FROM ENV VARS------------------------------------------------"
    show_available_dbs(get_ncbi_dbs(email, api_key))


