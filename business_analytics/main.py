#!/usr/bin/env python3
'''
'''

from openai import OpenAI
import anthropic

from pydantic import BaseModel, Field
from typing import List

import sys, os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())







def main():
    pass


if __name__ == "__main__":
    logging.config(filename="main.log",level=logging.INFO)
    sys.exit(main())