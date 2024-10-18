Feature: Users

  Background:
    Given I create and login the following user
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: hunter2
      """
    And The following user exists
      """
      name: Tom
      lastname: Thomson
      email: tom_thomson@example.com
      password: secret
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
      - id: 2
        name: Tom
        lastname: Thomson
        email: tom_thomson@example.com
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

  Scenario: Update user - Name
    When I do a POST request to /users/me with the following data
      """
      name: Ricardo
      """
    Then I get a 200 response
    And I do a GET request to /users/me
    And The response JSON is
      """
      id: 1
      name: Ricardo
      lastname: Doe
      email: john_doe@example.com
      avatar: null
      """

  Scenario: Update User - lastname
    When I do a POST request to /users/me with the following data
      """
      lastname: Beckenbauer
      """
    Then I get a 200 response
    And I do a GET request to /users/me
    And The response JSON is
      """
      id: 1
      name: John
      lastname: Beckenbauer
      email: john_doe@example.com
      avatar: null
      """

  Scenario: Get Squads - empty
    When I do a GET request to /users/me/squads
    Then I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Get squads
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a GET request to /users/me/squads
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        logo: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """

  Scenario: Get invites - Empty
    When I do a GET request to /users/me/invites
    Then I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Get invites
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I do a POST request to /squads/1/invites with the following data
      """
      email: tom_thomson@example.com
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a GET request to /users/me/invites
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        logo: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """

  Scenario: Get invites - multiple
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I do a POST request to /squads/1/invites with the following data
      """
      email: tom_thomson@example.com
      """
    And I do a POST request to /squads with the following data
      """
      name: Synergy seekers
      description: catchy phrase
      """
    And I do a POST request to /squads/2/invites with the following data
      """
      email: tom_thomson@example.com
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a GET request to /users/me/invites
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        logo: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      - id: 2
        name: Synergy seekers
        description: catchy phrase
        logo: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """

  Scenario: Get applies
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a PUT request to /squads/1/apply
    Then I get a 200 response
    And The response JSON is
      """
      message: Application created
      """
    And I do a GET request to /users/me/applies
    And I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        logo: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """
