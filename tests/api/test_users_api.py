import pytest


pytestmark = pytest.mark.api


def test_user_register_empty_body_returns_field_errors(api):
    """Goal: kiểm tra dữ liệu đăng ký bắt buộc.
    Precondition: gửi dữ liệu đăng ký rỗng.
    Expected: trả về 422 và lỗi email, password."""
    response = api.post("/users/register", data={})

    assert response.status == 422, response.text()

    errors = response.json()

    assert "email" in errors, errors
    assert "password" in errors, errors


def test_user_profile_with_token_returns_own_email(
    api,
    auth_headers,
    test_user,
):
    """Goal: kiểm tra truy cập hồ sơ bằng token.
    Precondition: tài khoản riêng đã được tạo và đăng nhập.
    Expected: trả về 200 và đúng email tài khoản."""
    response = api.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status == 200, response.text()

    body = response.json()

    assert body["email"] == test_user["email"], body