Feature: Validate User Access API

  Scenario: Check for valid users in Azure
    Given the API client and database are available
    When a GET request is sent to "/api/Access/GetUserAccessInfo" for each user
    Then the response code should be 200 for all valid users
    Then the response code should be 404 for all invalid users
