# MAPAPI Pytest BDD Framework

The MAPAPI project is a Python-based testing framework designed to validate the functionality of APIs hosted on an Azure environment. It uses Behavior-Driven Development (BDD) practices to ensure that the APIs meet specified requirements. The framework focuses on the Field Data API and User Access API, leveraging `httpx` for API communication to address SSL issues, and `pyodbc` for database interactions.

## Overview

This project utilizes a Python-based architecture for validating APIs through BDD-style testing. It employs `pytest` for test execution and `pytest-bdd` for defining BDD-style test scenarios. The framework includes utilities for API communication using the `httpx` library and database interactions via `pyodbc`. Configuration management is handled through a `settings.ini` file, and logging is implemented to track API requests and database operations. The project is structured with a focus on modularity and reusability, with distinct directories for configuration, utilities, tests, and feature files.

## Features

- **Field Data API Validation**: Validates the Field Data API by sending a GET request to retrieve field data, ensuring the response code is 200.
- **User Access API Validation**: Validates user access through the User Access API by sending a GET request for each user, checking for response codes 200 for valid users and 404 for invalid ones.
- **BDD-Style Testing**: Uses `pytest-bdd` for writing clear and human-readable test scenarios in `.feature` files.
- **Configuration Management**: Manages API and database settings via a `settings.ini` file, allowing easy modification of base URLs and credentials.
- **Logging**: Records API request statuses and database operations to aid in debugging and audit trails.
- **Database Interaction**: Connects to a SQL Server database to fetch user emails and field names necessary for API requests.

## Getting started

### Requirements

To run this project, ensure the following technologies and setups are available on your system:

- Python 3.x
- SQL Server (can be a cloud instance or installed on another server)
- The following Python libraries:
  - `pytest`
  - `pytest-bdd`
  - `httpx`
  - `pyodbc`
  - `pytest-html`

### Quickstart

1. **Clone the repository**:
   - Clone the project repository to your local machine.

2. **Install dependencies**:
   - Navigate to the project directory and run the following command to install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure settings**:
   - Update the `config/settings.ini` file with the appropriate base URLs and database credentials.

4. **Run tests**:
   - Execute the following command to run the tests:
     ```bash
     pytest --maxfail=5 --disable-warnings
     ```

### License

The project is proprietary.  
Copyright (c) 2024.