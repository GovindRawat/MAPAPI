import pytest
from pytest_bdd import scenarios, given, when, then

# Load the feature scenarios
scenarios('features/get_user_access.feature')


@given("the API client and database are available")
def setup(api_client, db_manager):
    assert api_client is not None, "API client is not available"
    assert db_manager is not None, "Database manager is not available"


@when('a GET request is sent to "/api/Access/GetUserAccessInfo" for each user')
def send_user_access_request(api_client, db_manager):
    try:
        users = db_manager.fetch_user_emails()
    except Exception as e:
        pytest.fail(f"Failed to fetch user emails: {e}")

    pytest.responses = []

    for user_email in users:
        params = {"UserEmail": user_email}
        response = api_client.get("/api/Access/GetUserAccessInfo", params=params)
        pytest.responses.append((user_email, response))


@then("the response code should be 200 for all valid users")
def verify_response_code(logger):
    for user_email, response in pytest.responses:
        logger.info(f"Testing user: {user_email}")
        assert response.status_code == 200, f"Expected 200 for user: {user_email}, got {response.status_code}"
        logger.info(f"Response Code for {user_email}: {response.status_code}")


@then("the response code should be 404 for all invalid users")
def verify_failure_response_code(api_client, logger):
    invalid_emails = [
        "navyasree@bftg.com",
        "saranyaeeday@bftg.com",
        "benjaminenglish@bftg.com",
        "albertocanete@bftg.com",
        "sureshnagisetti@bftg.com"
    ]

    for user_email in invalid_emails:
        logger.info(f"Testing user: {user_email}")
        params = {"UserEmail": user_email}
        response = api_client.get("/api/Access/GetUserAccessInfo", params=params)
        assert response.status_code == 404, f"Expected 404 for user: {user_email}, got {response.status_code}"
        logger.info(f"Response Code for {user_email}: {response.status_code}")
