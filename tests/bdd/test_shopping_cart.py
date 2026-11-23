import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage


pytestmark = [
    pytest.mark.bdd,
    pytest.mark.ui,
]

scenarios("shopping_cart.feature")


@given("I am on the home page", target_fixture="home")
def open_home(page):
    home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()

    return home


@when(parsers.parse('I search for "{keyword}"'))
def search_for_product(home, keyword):
    home.search(keyword)

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text(keyword)


@when(
    parsers.parse('I open the product "{product}"'),
    target_fixture="product_page",
)
def open_product(home, product):
    product_page = home.open_product(product)

    expect(product_page.name).to_contain_text(product)
    expect(product_page.unit_price).to_be_visible()

    return product_page


@when(
    parsers.parse(
        "I add it to the cart with quantity {quantity:d}"
    ),
    target_fixture="unit_price",
)
def add_product(product_page, quantity):
    unit_price = product_page.price()

    product_page.add_to_cart(quantity=quantity)

    expect(product_page.cart_quantity).to_have_text(
        str(quantity)
    )

    return unit_price


@when("I open the cart", target_fixture="cart")
def open_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse('the cart contains "{product}"'))
def check_product(cart, product):
    expect(cart.product_titles).to_have_count(1)
    expect(cart.product_titles.first).to_have_text(product)


@then(
    parsers.parse(
        "the line price equals the unit price times {quantity:d}"
    )
)
def check_line_price(cart, unit_price, quantity):
    expect(cart.line_prices).to_have_count(1)
    expect(cart.line_prices.first).to_be_visible()

    assert cart.line_totals()[0] == pytest.approx(
        unit_price * quantity
    )


@then("the cart total equals the sum of the line prices")
def check_cart_total(cart):
    expect(cart.total).to_be_visible()

    assert cart.total_value() == pytest.approx(
        sum(cart.line_totals())
    )