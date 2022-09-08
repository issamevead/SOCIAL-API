import asyncio
import functools
import re
import time
import urllib
from contextlib import suppress
from copy import deepcopy
from datetime import datetime

from random import randint, shuffle
from threading import Thread
from typing import Any, Generator, List, Optional, Union


from src.utils.countries import countries



def create_thread(function):
    @functools.wraps(function)
    def wrapper_timer(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return wrapper_timer


def go_sleep(seconds: int) -> None:
    """Sleep for a given number of seconds"""
    time.sleep(randint(3, seconds))


def json_extract(obj, key) -> List[Any]:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, val in obj.items():
                if isinstance(val, (list, dict)) and k != key:
                    extract(val, arr, key)
                elif k == key:
                    arr.append(val)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def get_timestamp_from_date(date: str) -> Optional[int]:
    """Return timestamp from date"""
    with suppress(Exception):
        return int(datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y").timestamp())
    return None


def url_quote(query):
    """Return URL quote String"""
    return urllib.parse.quote(query)


def parse_cookies_to_str(cookies: dict) -> str:
    """Parse cookies to string"""
    return "; ".join(f"{k}={v}" for k, v in cookies.items())


def get_result_from_regex_pattern(
    element: str, pattern: str, group_id: int = 1
) -> Union[str, None]:
    """Get the result of a regex compile using a certain pattern
    Args:
        element (str): Text to search
        pattern (str): Patter to compile
        group_id (int, optional): Group ID after the search. Defaults to 1.
    Returns:
        Union[str, None]: Result of the search
    """
    reg = re.compile(str(pattern))
    result = reg.search(element)
    if result is not None:
        return result.group(group_id)
    return None


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (list, dict)) and k != key:
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def json_extract_strict(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (list, dict)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


def get_tz_by_iso(country: str) -> Optional[str]:
    search = list(filter(lambda x: x.get("code") == country.upper(), countries))
    if len(search) > 0:
        return search[0].get("timezones")[0]
    return None


def get_result_from_regex_pattern(
    element: str, pattern: str, group_id: int = 1
) -> Union[str, None]:
    """Get the result of a regex compile using a certain pattern
    Args:
        element (str): Text to search
        pattern (str): Patter to compile
        group_id (int, optional): Group ID after the search. Defaults to 1.
    Returns:
        Union[str, None]: Result of the search
    """
    reg = re.compile(str(pattern))
    result = reg.search(element)
    if result is not None:
        return result.group(group_id)
    return None
