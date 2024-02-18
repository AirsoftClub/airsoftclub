Feature: Registering and login

  Scenario: Register new user
    Given I do a POST request to /auth/register with the following data
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: John
      lastname: Doe
      email: john_doe@example.com
      avatar: null
      """

  Scenario: User already exists
    Given I do a POST request to /auth/register with the following data
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """
    Given I do a POST request to /auth/register with the following data
      """
      name: Mark
      lastname: Thompson
      email: john_doe@example.com
      password: secret
      """
    Then I get a 400 response
    And The response JSON is
      """
      detail: Email already registered
      """

  Scenario: Login
    Given I do a POST request to /auth/register with the following data
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """
    Given I do a POST request to /auth/login with the following data
      """
      email: john_doe@example.com
      password: hunter2
      """
    Then I get a 200 response

  # TODO: check token is created correctly
  Scenario: Login with non existent user
    Given I do a POST request to /auth/login with the following data
      """
      email: something@example.com
      password: blablabla
      """
    Then I get a 404 response
    And The response JSON is
      """
      detail: User not found
      """

  Scenario: Login with invalid credentials
    Given I do a POST request to /auth/register with the following data
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """
    And I do a POST request to /auth/login with the following data
      """
      email: john_doe@example.com
      password: blablabla
      """
    Then I get a 401 response
    And The response JSON is
      """
      detail: Invalid credentials
      """
