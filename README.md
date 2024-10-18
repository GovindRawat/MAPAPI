# **API Testing Framework with Pytest-BDD**

This is a **dynamic and scalable API testing framework** built using **Pytest, Pytest-BDD, and Pyodbc**. The framework integrates seamlessly with **Azure CI/CD pipelines** to support continuous testing and deployment. It follows best practices, ensuring robust error handling, logging, and test reporting.

## **Project Structure**

├── tests/
│   ├── features/
│   │   └── access_api.feature  # BDD Feature file for API tests
│   ├── test_get_user_access_api.py      # Test file for user access API
│   └── test_field_data_api.py  # Test file for field data API (future)
├── config/
│   └── config.py               # DB credentials and configurations
├── utils/
│   └── db_manager.py           # Database manager to interact with DB
│   └── api_client.py           # API client to send requests
│   └── logger.py               # Logging setup
├── conftest.py                 # Pytest fixtures setup
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation (this file)


---

## **Features**

- **BDD Approach:** Uses **pytest-bdd** to implement behavior-driven tests.
- **Azure CI/CD Integration:** Supports seamless execution in CI/CD pipelines.
- **Database Integration:** Fetches **user emails and input data** from the database.
- **Logging:** Captures test execution details and errors.
- **Reports:** Generates detailed HTML test reports.
- **Scalable Framework:** Easily extendable with new test cases and APIs.

---

## **Setup Instructions**

### **Prerequisites**

1. Install **Python 3.8+**.
2. Ensure you have **access to the required database**.
3. Install **Azure CLI** if running tests in CI/CD.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>

2. Create a virtual environment and activate it:
    ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate  # For Windows

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   
## **Configuration**

1. Update the database credentials in config/config.py:
```python
DB_CONFIG = {
    "server": "your_db_server",
    "database": "your_database",
    "username": "your_username",
    "password": "your_password",
    "driver": "{ODBC Driver 17 for SQL Server}"
}

```
2. Modify API base URLs or endpoints as needed in the respective feature files and test scripts.

## **How to run Tests Locally**

1. To run all tests:
```bash
pytest --html=reports/report.html --self-contained-html
```
2. To run a specific feature file:
```bash
pytest tests/features/access_api.feature --html=reports/report.html
```

---

## **Logging**

- All logs are stored in the logs/ directory. The logger.py module ensures that logs are captured for each test run, including error details if any test fails.
---


## **Writing New Test Cases**

- Create a new feature file under tests/features/.
- Add corresponding test logic in a new test file inside tests/.
- Use the db_manager.py utility to fetch dynamic input data from the database.
- Use API endpoints via the api_client.py module.

---

## **License**
- This project is licensed under the MIT License. See the LICENSE file for more details.
