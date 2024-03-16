Feature: Games

  Background: Create an admin, a user and a field for that user
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
    And I do a POST request to /fields/ with the following data
      """
      owner: tom_thomson@example.com
      field:
        name: Minorva
        description: Noveatu
        latitude: 90.00
        longitude: 45.00
      """
    And I get a 200 response

  Scenario: Book to a game and get accepted
    Given The date is 2020-01-01T12:00:00
    And I'm logged with the user tom_thomson@example.com
    And I do a POST request to /games/field/1/ with the following data
      """
      name: Match saturday morning
      description: Free for all
      max_players: 20
      played_at: '2020-01-02T12:00:00'
      teams:
        - RED
        - BLUE
      """
    And I create and login the following user
      """
      name: John
      lastname: Doe
      email: john_doe@example.com
      password: secret
      """
    When I'm logged with the user john_doe@example.com
    And I do a POST request to /bookings/game/1/ with the following data
      """
      team_name: RED
      """
    Then I get a 200 response
    And The response JSON is
      """
      game_id: 1
      player_id: 3
      team_id: 1
      created_at: '2020-01-01T12:00:00'
      """
    And I do a GET request to /users/me/bookings
    Then I get a 200 response
    And The response JSON is
      """
      - game_id: 1
        player_id: 3
        team_id: 1
        created_at: '2020-01-01T12:00:00'
      """
