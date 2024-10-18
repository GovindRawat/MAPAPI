import pytest
from pytest_bdd import scenarios, given, when, then

scenarios('features/field_data.feature')


@given("the API client and database are available")
def setup(api_client, db_manager):
    assert api_client is not None
    assert db_manager is not None


@when('a GET request is sent to "/api/FieldData/GetFieldData"')
def send_field_data_request(api_client, db_manager):
    field_name = db_manager.fetch_field_name()
    params = {"FieldName": field_name}
    response = api_client.get("/api/FieldData/GetFieldData", params=params)
    pytest.response = response


@then("the response code should be 200")
def verify_response_code(logger):
    assert pytest.response.status_code == 200
    logger.info(f"Response Code: {pytest.response.status_code}")
