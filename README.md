# Business Analytics
A Demonstrative Toy LLM-Assisted Business Analytics/Finance Tool

## Description

This toy program demonstrates some of the concepts taught in fall 2026 Springboard "AI for Programmers" Bootcamp, such as structured output, 
chained output/HITL, long-lived context with skills files, and support for traceability and observability. It uses calls to ChatGPT using
OpenAI's API to answer questions about the stock market and similar financial entities, with the system instructed specifically to look at 
social media and prediction markets to help identify trends. Relevant financial data, such as about Nasdaq entities, could be turned into
vectorized embeddings and used in a RAG pipeline, as one extension of this program to exemplify the RAG techniques taught in one module.

## Getting Started
Run main.py or gui.py and enter a question about the stock market, etc., such as, "Should I invest in [company name]?".

### Dependencies

- OpenAI, Langsmith, Pydantic, in the future potentially Anthropic and Pinecone
- Version of Python 3 that supports typing and f-strings
- Platform-Independent

### Installing
- Download the repo and run main.py or gui.py
- I need to refine the package structure so it can be uploaded to test.pypi.org (as a personal exercise).
- I also need to refactor the package in general.
- The GUI was vibe-coded and still needs to be tested (and have HITL implemented).

### Executing program

- Run main.py or gui.py
- An executable for the gui using PyExe is also in the works.

## Help
- This program is pretty self-explanatory.

## Authors
[Rose Nestor](https://github.com/RuminativeRose)

## Version History
- 0.1 Initial Release

## License
This project is licensed under the Apache-2.0 License--see the LICENSE file for details

## Acknowledgments
- [Springboard 'AI for Programmers' Bootcamp](https://www.springboard.com)
- Course exercises in [aiforprogrammers](https://github.com/Springboard-CourseDev/ai-programmers) repo
- Demo exercises in [AIP-may](https://github.com/vedansh/AIP-may) repo
- [Langsmith documentation](https://docs.langchain.com/langsmith/reference)
- [Sample README.md file](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
- ['Instructor' CLAUDE.md file](https://github.com/567-labs/instructor/blob/main/CLAUDE.md)
- Skills from ["The Skills & Persistent Context Guide"](https://springboardedu.instructure.com/courses/209/files/20887/download?download_frd=1)
