Feature: Fields

  Background:
    Given I create and login the following user
      """
      name: Admin
      lastname: ac
      email: admin@airsoftclub.com
      password: hunter2
      """
    And The user admin@airsoftclub.com is an admin
    And The following user exists
      """
      name: Tom
      lastname: Thomson
      email: tom_thomson@example.com
      password: secret
      """

  Scenario: Create Field
    When I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: Minorva
      description: Noveatu
      avatar: null
      latitude: 90.00
      longitude: 45.00
      """

  Scenario: Create Field - Unauthorized
    Given I'm logged with the user tom_thomson@example.com
    When I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    Then I get a 403 response
    And The response JSON is
      """
      detail: Not authorized
      """

  Scenario: Get Fields
    Given I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    Given I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Zona Teta
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    When I do a GET request to /fields
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Minorva
        description: Noveatu
        avatar: null
        latitude: 90.00
        longitude: 45.00
      - id: 2
        name: Zona Teta
        description: Noveatu
        avatar: null
        latitude: 90.00
        longitude: 45.00
      """

  Scenario: Get Field
    Given I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    When I do a GET request to /fields/1
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: Minorva
      description: Noveatu
      avatar: null
      latitude: 90.00
      longitude: 45.00
      """

  Scenario: Get my Fields - Empty
    When I do a get request to /users/me/fields
    Then I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Get my Fields
    Given I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    And I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Zona Teta
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a GET request to /users/me/fields
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Minorva
        description: Noveatu
        avatar: null
        latitude: 90.00
        longitude: 45.00
      - id: 2
        name: Zona Teta
        description: Noveatu
        avatar: null
        latitude: 90.00
        longitude: 45.00
      """
