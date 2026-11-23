import json
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


pytestmark = pytest.mark.ui

PRODUCT_LIST = re.compile(r"/products(\?.*)?$")

EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0,
}


def test_home_without_images_still_shows_products(page):
    """Goal: kiểm tra trang khi ảnh bị chặn.
    Precondition: đăng ký route chặn ảnh trước khi mở trang.
    Expected: tên sản phẩm hiện và có yêu cầu ảnh bị chặn."""
    blocked = []

    def block(route):
        blocked.append(route.request.url)
        route.abort()

    page.route(
        re.compile(
            r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$",
            re.IGNORECASE,
        ),
        block,
    )

    home = HomePage(page).open()

    expect(home.product_names.first).to_be_visible()

    assert blocked, "Không có yêu cầu ảnh nào bị chặn"


def test_home_empty_product_response_shows_no_results(page):
    """Goal: kiểm tra trạng thái danh sách rỗng.
    Precondition: API danh sách được giả lập trả dữ liệu rỗng.
    Expected: hiện thông báo không tìm thấy và không có sản phẩm."""
    mocked = []

    def empty_products(route):
        mocked.append(route.request.url)

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(EMPTY_PAGE),
        )

    page.route(PRODUCT_LIST, empty_products)

    home = HomePage(page).open()

    expect(home.no_results).to_have_text(
        "There are no products found."
    )
    expect(home.product_names).to_have_count(0)

    assert mocked, "Route giả lập chưa chạy"