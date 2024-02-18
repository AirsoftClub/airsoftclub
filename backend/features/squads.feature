Feature: Squad

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

  Scenario: Create Squad
    When I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: Power Rangers Squad
      description: Po-po-power rangers!
      avatar: null
      owner:
          id: 1
          name: John
          lastname: Doe
          email: john_doe@example.com
          avatar: null
      """

  Scenario: Create Squad - Existing name
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Another power ranger squad!
      """
    Then I get a 400 response
    And The response JSON is
      """
      detail: Squad already exists
      """

  Scenario: Create too many Squad
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I get a 200 response
    And I do a POST request to /squads with the following data
      """
      name: Synergy seekers
      description: catchy phrase
      """
    And I get a 200 response
    And I do a POST request to /squads with the following data
      """
      name: Visionary Vanguards
      description: catchy phrase
      """
    And I get a 200 response
    When I do a POST request to /squads with the following data
      """
      name: Unnstopable Unisons
      description: catchy phrase
      """
    Then I get a 400 response
    And The response JSON is
      """
      detail: You can't create more than 3 squads
      """

  Scenario: Get Squads
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I do a POST request to /squads with the following data
      """
      name: Synergy seekers
      description: catchy phrase
      """
    When I do a GET request to /squads
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        avatar: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      - id: 2
        name: Synergy seekers
        description: catchy phrase
        avatar: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """

  Scenario: Get Squad
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a GET request to /squads/1
    Then I get a 200 response
    And The response JSON is
      """
      id: 1
      name: Power Rangers Squad
      description: Po-po-power rangers!
      avatar: null
      owner:
          id: 1
          name: John
          lastname: Doe
          email: john_doe@example.com
          avatar: null
      """

  Scenario: Delete Squad
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I do a GET request to /squads
    And I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: Power Rangers Squad
        description: Po-po-power rangers!
        avatar: null
        owner:
            id: 1
            name: John
            lastname: Doe
            email: john_doe@example.com
            avatar: null
      """
    When I do a DELETE request to /squads/1
    And I get a 200 response
    Then I do a GET request to /squads
    And I get a 200 response
    And The response JSON is
      """
      []
      """
    And I do a GET request to /squads/1
    And I get a 404 response
    And The response JSON is
      """
      detail: Squad not found
      """

  Scenario: Delete Squad - Non existent
    When I do a DELETE request to /squads/999
      """
      detail: Squad not found
      """

  Scenario: Delete Squad - Not owned
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a DELETE request to /squads/1
      """
      detail: You are not the owner of this squad
      """

  Scenario: Get Squads - Empty
    When I do a GET request to /squads
    Then I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Get Members
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I do a GET request to /squads/1
    And I get a 200 response
    When I do a GET request to /squads/1/members
    Then I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: John
        lastname: Doe
        email: john_doe@example.com
        avatar: null
      """

  Scenario: Update Squad - Update name
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1 with the following data
      """
      name: A-Team
      """
    Then I do a GET request to /squads/1
    And I get a 200 response
    And The response JSON is
      """
      id: 1
      name: A-Team
      description: Po-po-power rangers!
      avatar: null
      owner:
          id: 1
          name: John
          lastname: Doe
          email: john_doe@example.com
          avatar: null
      """

  Scenario: Update Squad - Update description
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1 with the following data
      """
      description: Now with more calcium!
      """
    Then I do a GET request to /squads/1
    And I get a 200 response
    And The response JSON is
      """
      id: 1
      name: Power Rangers Squad
      description: Now with more calcium!
      avatar: null
      owner:
          id: 1
          name: John
          lastname: Doe
          email: john_doe@example.com
          avatar: null
      """

  Scenario: Update Squad - not owned
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    Given I'm logged with the user tom_thomson@example.com
    When I do a PUT request to /squads/1 with the following data
      """
      description: Now with more calcium!
      """
    Then I get a 403 response
    And The response JSON is
      """
      detail: You are not the owner of this squad
      """

  Scenario: Invite a user
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a POST request to /squads/1/invites with the following data
      """
      email: tom_thomson@example.com
      """
    Then I get a 200 response
    And The response JSON is
      """
      message: User invited
      """
    And I do a GET request to /squads/1/invites
    And I get a 200 response
    And The response JSON is
      """
      - id: 2
        name: Tom
        lastname: Thomson
        email: tom_thomson@example.com
        avatar: null
      """

  Scenario: Invite a user - accept invite
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
    When I do a PUT request to /squads/1/invites with the following data
      """
      accept: true
      """
    And I get a 200 response
    And The response JSON is
      """
      message: Invitation updated
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
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
    And I do a GET request to /squads/1/invites
    And I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Invite - Accept a non invited user
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1/invites with the following data
      """
      accept: true
      """
    And I get a 400 response
    And The response JSON is
      """
      detail: User is not invited
      """

  Scenario: Invite a user - Already a member
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
    And I do a PUT request to /squads/1/invites with the following data
      """
      accept: true
      """
    And I'm logged with the user john_doe@example.com
    When I do a POST request to /squads/1/invites with the following data
      """
      email: tom_thomson@example.com
      """
    And I get a 400 response
    And The response JSON is
      """
      detail: User is already a member
      """

  Scenario: Invite a user - already applied
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    When I do a PUT request to /squads/1/apply
    And I'm logged with the user john_doe@example.com
    Then I do a POST request to /squads/1/invites with the following data
      """
      email: tom_thomson@example.com
      """
    And I get a 200 response
    And The response JSON is
      """
      message: User joined the squad
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
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

  Scenario: Invite a user - decline invite
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
    When I do a PUT request to /squads/1/invites with the following data
      """
      accept: false
      """
    And I get a 200 response
    And The response JSON is
      """
      message: Invitation updated
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: John
        lastname: Doe
        email: john_doe@example.com
        avatar: null
      """
    And I do a GET request to /squads/1/invites
    And I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Invite a user - Non existent user
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a POST request to /squads/1/invites with the following data
      """
      email: ron_ronson@example.com
      """
    Then I get a 404 response
    And The response JSON is
      """
      detail: User not found
      """

  Scenario: Apply to Squad
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
    And I do a GET request to /squads/1/applies
    And I get a 200 response
    And The response JSON is
      """
      - id: 2
        name: Tom
        lastname: Thomson
        email: tom_thomson@example.com
        avatar: null
      """

  Scenario: Apply to Squad - as member
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1/apply
    Then I get a 400 response
    And The response JSON is
      """
      detail: User is already in squad
      """
    And I do a GET request to /squads/1/applies
    And I get a 200 response
    And The response JSON is
      """
      []
      """

  Scenario: Apply to Squad - Already invited
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
    When I do a PUT request to /squads/1/apply
    Then I get a 200 response
    And The response JSON is
      """
      message: User joined the squad
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
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

  Scenario: Apply to Squad - accepted
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    And I do a PUT request to /squads/1/apply
    And I get a 200 response
    And The response JSON is
      """
      message: Application created
      """
    And I'm logged with the user john_doe@example.com
    When I do a PUT request to /squads/1/applies/2 with the following data
      """
      accept: true
      """
    Then I get a 200 response
    And The response JSON is
      """
      message: Application updated
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
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

  Scenario: Apply to Squad - decline
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    And I do a PUT request to /squads/1/apply
    And I get a 200 response
    And The response JSON is
      """
      message: Application created
      """
    And I'm logged with the user john_doe@example.com
    When I do a PUT request to /squads/1/applies/2 with the following data
      """
      accept: false
      """
    Then I get a 200 response
    And The response JSON is
      """
      message: Application updated
      """
    And I do a GET request to /squads/1/members
    And I get a 200 response
    And The response JSON is
      """
      - id: 1
        name: John
        lastname: Doe
        email: john_doe@example.com
        avatar: null
      """

  Scenario: Apply to Squad - accept not as owner
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    And I'm logged with the user tom_thomson@example.com
    And I do a PUT request to /squads/1/apply
    And I get a 200 response
    And The response JSON is
      """
      message: Application created
      """
    When I do a PUT request to /squads/1/applies/2 with the following data
      """
      accept: true
      """
    Then I get a 403 response
    And The response JSON is
      """
      detail: You are not the owner of this squad
      """

  Scenario: Apply to Squad - accept missing user
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1/applies/999 with the following data
      """
      accept: true
      """
    Then I get a 404 response
    And The response JSON is
      """
      detail: User not found
      """

  Scenario: Apply to Squad - Accept non applied user
    Given I do a POST request to /squads with the following data
      """
      name: Power Rangers Squad
      description: Po-po-power rangers!
      """
    When I do a PUT request to /squads/1/applies/2 with the following data
      """
      accept: true
      """
    Then I get a 400 response
    And The response JSON is
      """
      detail: User didn't apply to this squad
      """
