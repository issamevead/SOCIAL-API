from collections import namedtuple
import json
from typing import Dict, Optional
from pydantic import BaseModel, Field
from requests import get
from bs4 import BeautifulSoup as soup
import re
from src.utils.util import json_extract
import time

response = get(f"https://unsplash.com/collections/{9679712}")
r = (
    response.text.split('<script>window.__INITIAL_STATE__ = JSON.parse("')[1]
    .split("</script>")[0]
    .strip()[:-3]
)
r = r.encode().decode("unicode_escape")
r = json.loads(r)
script = json_extract(r, "9679712")[0]
script
