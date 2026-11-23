import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.api

DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "search_keywords.json"
)

KEYWORDS = json.loads(DATA_FILE.read_text(encoding="utf-8"))


def test_products_first_page_has_valid_structure(api):
    """Goal: kiểm tra cấu trúc danh sách sản phẩm.
    Precondition: API có dữ liệu sản phẩm.
    Expected: đủ khóa phân trang và sản phẩm có dữ liệu hợp lệ."""
    response = api.get("/products", params={"page": 1})

    assert response.status == 200, response.text()

    body = response.json()

    for key in (
        "current_page",
        "data",
        "per_page",
        "total",
        "last_page",
    ):
        assert key in body, f"Thiếu khóa {key}"

    assert isinstance(body["data"], list), body
    assert isinstance(body["per_page"], int), body
    assert 0 < len(body["data"]) <= body["per_page"], body

    for product in body["data"]:
        assert isinstance(product["id"], (str, int)), product

        assert (
            isinstance(product["name"], str)
            and product["name"].strip()
        ), product

        assert (
            isinstance(product["price"], (int, float))
            and product["price"] > 0
        ), product


@pytest.mark.parametrize(
    "case",
    KEYWORDS,
    ids=[case["keyword"] for case in KEYWORDS],
)
def test_products_search_returns_matching_names(api, case):
    """Goal: kiểm tra tìm kiếm với dữ liệu từ JSON.
    Precondition: từ khóa có sản phẩm phù hợp.
    Expected: có kết quả và mọi tên đều chứa chuỗi yêu cầu."""
    response = api.get(
        "/products/search",
        params={"q": case["keyword"]},
    )

    assert response.status == 200, response.text()

    names = [
        product["name"]
        for product in response.json()["data"]
    ]

    assert names, f"Không có kết quả cho {case['keyword']}"

    assert all(
        case["must_contain"].lower() in name.lower()
        for name in names
    ), names


@pytest.mark.parametrize(
    "path, expected",
    [
        ("/users/me", 401),
        ("/products/does-not-exist", 404),
    ],
)
def test_resource_without_access_or_missing_returns_4xx(
    api,
    path,
    expected,
):
    """Goal: kiểm tra mã lỗi của tài nguyên.
    Precondition: chưa xác thực hoặc sản phẩm không tồn tại.
    Expected: trả về 401 hoặc 404 tương ứng."""
    response = api.get(path)

    assert response.status == expected, response.text()