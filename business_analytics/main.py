#!/usr/bin/env python3
'''
A basic business analytics software demonstrating the use of AI in programming techniques.
'''

from openai import OpenAI
# import anthropic # Not yet implemented

from pydantic import BaseModel, Field
from typing import List

from langsmith import Client, traceable, tracing_context
from langsmith.wrappers import wrap_openai

import sys, os
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())







def main():
    pass


if __name__ == "__main__":
    logging.config(filename="main.log",level=logging.INFO)
    sys.exit(main())