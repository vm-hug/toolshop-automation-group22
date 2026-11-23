import pytest


pytestmark = pytest.mark.api


@pytest.fixture
def new_cart(api):
    """Tạo giỏ hàng riêng cho mỗi test."""
    response = api.post("/carts")

    assert response.status == 201, response.text()

    return response.json()["id"]


def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: kiểm tra API lưu sản phẩm và số lượng.
    Precondition: một giỏ hàng mới và sản phẩm có sẵn.
    Expected: giỏ có một dòng, đúng sản phẩm, số lượng 2."""
    products_response = api.get(
        "/products",
        params={"page": 1},
    )

    assert products_response.status == 200, products_response.text()

    products = products_response.json()["data"]

    assert products, "Không có sản phẩm"

    product = products[0]

    added = api.post(
        f"/carts/{new_cart}",
        data={
            "product_id": product["id"],
            "quantity": 2,
        },
    )

    assert added.ok, added.text()

    response = api.get(f"/carts/{new_cart}")

    assert response.status == 200, response.text()

    items = response.json()["cart_items"]

    assert len(items) == 1, items
    assert items[0]["quantity"] == 2, items
    assert str(items[0]["product_id"]) == str(product["id"]), items