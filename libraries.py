from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import json
from requests.models import parse_header_links
import time
import os
from pathlib import Path