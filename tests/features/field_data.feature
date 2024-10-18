Feature: Validate Field Data API

  Scenario: Get field details from API
    Given the API client and database are available
    When a GET request is sent to "/api/FieldData/GetFieldData"
    Then the response code should be 200
