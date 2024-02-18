Feature: Users

  Background:
    Given I create and login the following user
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """

  Scenario: Get all users
    When I do a GET request to /users
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: John
        lastname: Doe
        email: john_doe@example.com
        avatar: null
      """

  Scenario: Get current user
    When I do a GET request to /users/me
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: John
      lastname: Doe
      email: john_doe@example.com
      avatar: null
      """

  Scenario: Update user
    When I do a POST request to /users/me with the following data
      """
      name: Ricardo
      lastname: Beckenbauer
      """
    Then I get a 200 response
    And I do a GET request to /users/me
    And The response JSON is
      """
      id: 1
      name: Ricardo
      lastname: Beckenbauer
      email: john_doe@example.com
      avatar: null
      """
