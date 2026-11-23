Feature: Shopping cart
  As a shopper
  I want to find a product and add a chosen quantity to my cart
  So that I can review the correct amount before checkout

  Background:
    Given I am on the home page

  Scenario Outline: Selected products have the correct cart amount
    When I search for "<keyword>"
    And I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I open the cart
    Then the cart contains "<product>"
    And the line price equals the unit price times <quantity>
    And the cart total equals the sum of the line prices

    Examples:
      | keyword | product            | quantity |
      | pliers  | Combination Pliers | 1        |
      | hammer  | Claw Hammer        | 3        |