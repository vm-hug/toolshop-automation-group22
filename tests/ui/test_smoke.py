import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.ui
def test_search_pliers_shows_only_matching_products(page):
    """Goal: kiểm tra tìm kiếm sản phẩm theo từ khóa.
    Precondition: truy cập được trang chủ Toolshop.
    Expected: có kết quả và mọi tên sản phẩm đều chứa pliers."""
    home = HomePage(page).open().search("pliers")

    expect(home.search_completed).to_be_visible()
    expect(home.search_caption).to_contain_text("pliers")

    names = home.product_names.all_inner_texts()

    assert names, "Tìm kiếm không trả về sản phẩm"
    assert all("pliers" in name.lower() for name in names), names


@pytest.mark.smoke
@pytest.mark.ui
def test_add_three_hammers_updates_cart_badge(page):
    """Goal: kiểm tra thêm sản phẩm với số lượng 3.
    Precondition: giỏ hàng trống và sản phẩm Claw Hammer tồn tại.
    Expected: hiện thông báo thành công và badge giỏ hàng bằng 3."""
    product = HomePage(page).open().open_product("Claw Hammer")

    expect(product.name).to_contain_text("Claw Hammer")

    product.add_to_cart(quantity=3)

    expect(product.toast).to_contain_text(
        "Product added to shopping cart"
    )
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
@pytest.mark.ui
def test_login_invalid_credentials_shows_error(page):
    """Goal: kiểm tra từ chối thông tin đăng nhập sai.
    Precondition: dùng email không tồn tại, không dùng tài khoản chung.
    Expected: hiện thông báo lỗi và vẫn ở trang đăng nhập."""
    login_page = LoginPage(page).open()

    login_page.login(
        "nobody-here@example.com",
        "Wrong-Password-123",
    )

    expect(login_page.error).to_contain_text(
        "Invalid email or password"
    )
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
@pytest.mark.ui
def test_contact_empty_form_shows_required_errors(page):
    """Goal: kiểm tra các trường bắt buộc của form liên hệ.
    Precondition: mở trang Contact và để trống biểu mẫu.
    Expected: hiện Subject is required và Message is required."""
    contact = ContactPage(page).open()

    contact.submit()

    expect(contact.errors).to_contain_text([
        "Subject is required",
        "Message is required",
    ])