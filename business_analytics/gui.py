#!/usr/bin/env python3
'''
Simple GUI using PyQT6. Generated with  Claude Opus 5.5.
Does not yet implement HITL strategy like the CLI.
'''

import sys
import os
import logging

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit,
)

from openai import OpenAI
# import anthropic # Not yet implemented

# from pydantic import BaseModel, Field
# from typing import List

from langsmith import Client, traceable
from langsmith.wrappers import wrap_openai

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# LLM Client Setup
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = wrap_openai(openai.Client())

# LangSmith client setup
langsmith_api_key = os.environ.get("LANGCHAIN_API_KEY")
langsmith_project = "business-analytics"
langsmith_client = Client(api_key=langsmith_api_key)

# Other Constants/Setup
CHAT_MODEL = "gpt-4o-mini-2024-07-18"

TO_SEARCH=["X", "Kalshi", "Bluesky", "Polymarket", "Instagram","Google"]

 
@traceable(name="ask_openai",
        project_name=langsmith_project,
        run_type="llm")
def ask_openai(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": f"""You are a financial analyst who predicts future performance of stocks, funds, and companies based on trends on social media and prediction markets.
            You'll use {', '.join(TO_SEARCH)} as some of your sources to answer the user's query about a financial entity, its future performance, and whether or not to invest in it.""",
        },
        {
            "role": "user",
            "content": f"Question: {question}",
            
        },
    ]
    chat_completion = client.chat.completions.create(
        model=CHAT_MODEL, messages=messages
    )
    return chat_completion.choices[0].message.content
 
def process_input(text: str) -> str:
    """Take the user's input string and return the response string."""
    return ask_openai(text)
 
 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Program")
        self.resize(400, 300)
 
        layout = QVBoxLayout(self)
 
        layout.addWidget(QLabel("Enter your query about a stock, company, or financial entity."))
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.on_submit)  # Enter key also submits
        layout.addWidget(self.input_field)
 
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)
 
        layout.addWidget(QLabel("Response:"))
        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)
        layout.addWidget(self.output_field)
 
    def on_submit(self):
        user_text = self.input_field.text()
        response = process_input(user_text)
        self.output_field.setPlainText(response)
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
 