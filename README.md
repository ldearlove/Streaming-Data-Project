# Data Streaming Project

## Contributors
[Liam Dearlove](https://github.com/ldearlove)

## Overview

This project fetches articles from The Guardian API based on specific search queries and streams them to an Amazon Kinesis stream. It is designed to interact with The Guardian's content search API, format relevant articles, and send them to Kinesis for further processing or analysis. The project also features testing, security checks, and continuous integration through GitHub Actions.

## Features

* Fetch Articles: Pulls articles from The Guardian based on a search term and optional date filter.
* Format Data: Extracts relevant article information and provides a preview of the content.
* Send to Kinesis: Streams formatted articles to Amazon Kinesis for real-time data processing.
* Test-Driven Development: Contains unit tests to ensure all components work as expected.
* Security Checks: Ensures security best practices by running code analysis using Bandit and Safety.
* PEP8 Compliant: Usage of flake8 and autopep8 to ensure PEP8 compliance.
* Continuous Integration (CI): GitHub Actions workflow that automatically runs tests and checks on every commit.

## Repository Structure

* src/ - Contains the core logic of the project, split across multiple modules:
    * api_interaction.py: Fetches articles from The Guardian API.
    * format_article.py: Formats and structures article data.
    * send_to_kinesis.py: Sends formatted articles to Kinesis.
    * main.py: Orchestrates the entire process by fetching, formatting, and sending data to Kinesis.
* test/ - Contains unit tests for each function, ensuring the functionality and accuracy of the core logic.
* .github/workflows/main.yml - GitHub Actions workflow to run automated tests and security checks with each commit.
* requirements.txt - Lists all required Python libraries.
* streaming_data.md - Contains project specification.
* Makefile - Provides commands to automate common tasks (used in main.yml to run checks and tests):
    * `make create-environment` - Create Python environment.
    * `make requirements` - Install Python libraries listed in requirements.txt.
    * `make dev-setup` - Install bandit, safety, flake and coverage libraries.
    * `make security-test` - Run safety and bandit to check for security vulnerabilities.
    * `make run-flake` - Run flake8 to check for PEP8 compliance.
    * `make unit-test` - Run all unit tests for Python code.
    * `make run-checks` - Run all checks and tests.

## Setup Instructions

### Prerequisites

* Python 3.x
* AWS credentials (for Kinesis)
* The Guardian API key

### Steps to Set Up

1. Clone the repository:
   `git clone https://github.com/ldearlove/NC-Streaming-Data-Project
    cd NC-Streaming-Data-Project
   `
2. Set up environment:
   `make create-environment`
   `make requirements`
   `make dev-setup`
3. Set up the .env file - Create a .env file in the root directory and add your Guardian API key:
   `Guardian_API_Key=your_guardian_api_key`
4. Run tests and checks to ensure everything works correctly:
   `make run-checks`

## How It Works

### Main Functionality

1. Fetching Articles:
    The api_interaction() function retrieves articles from The Guardian API using a keyword query and optional date filter.
2. Formatting Articles:
    The format_article() function formats the article data, extracting key details like the title, publication date, and a 1000-character content preview.
3. Streaming to Kinesis:
    The send_to_kinesis() function sends the formatted articles to an Amazon Kinesis stream. This enables real-time data streaming for analytics.
4. Orchestrating the Flow:
    The main() function in main.py coordinates the process: fetching articles, formatting them, and streaming them to Kinesis.

Example flow:
    `main('machine learning', 'test-kinesis-stream', '2024-01-01')`

This will fetch recent articles on 'machine learning', format them, and stream the results to your Kinesis stream.

## Continuous Integration

The project is set up with GitHub Actions for continuous integration. Each commit triggers the following workflow:
* Run-checks: Use safety and bandit to check for security vulnerabilities.
* Run-tests: Runs tests to ensure the functionality of the code.

## Project Specifications

To see the specifications that this project was based on, please refer to `streaming_data.md`.
