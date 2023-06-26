import pytest
import requests
from pydantic import ValidationError
from serializers.auth_model import AuthRequestModel

#CREATE TOKEN TESTS HERE

@pytest.mark.auth
@pytest.mark.parametrize('username, password, headers', [
    ('admin', 'password123', {"Content-Type": "application/json"}),  # Valid data positive test
    ('admin', 'password123', {"Content-Type": ""}),                  # Invalid (empty) Content-Type negative test
    ('admin', 'password123', {}),                                    # No header negative test
    ('', '', {"Content-Type": "application/json"}),                  # No data negative test
    ('dsaqwe', 'asd123', {"Content-Type": "application/json"}),      # Invalid data negative test
])
def test_auth_request(username, password, headers):
    url = "https://restful-booker.herokuapp.com/auth"

    try:
        data = AuthRequestModel(username=username, password=password)
    except ValidationError as e:
        if username == '' and password == '':
            assert str(e) == "1 validation error for AuthRequestModel\nusername\n  " \
                             "field required (type=value_error.missing)\npassword\n  " \
                             "field required (type=value_error.missing)"
        else:
            pytest.fail(f"Failed to validate request data: {e}")

    response = requests.post(url, headers=headers, json=data.dict())

    assert response.status_code == 200, f"Request failed with status code {response.status_code}"
    if "reason" in response.json() and response.json()["reason"] == "Bad credentials":
        assert "token" not in response.json(), "Response contains a token for invalid credentials"
    else:
        assert "token" in response.json(), "Response does not contain a token"
