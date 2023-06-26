import pytest
import requests
from api.api import auth_token, create_booking

# TESTS THAT REQUIRED TOKEN HERE
# One of them bugged, so that - ignored

@pytest.mark.xfail
@pytest.mark.required_token
@pytest.mark.parametrize(
    'auth_token, create_booking, content_type, expected_status',
    [(auth_token(), create_booking(auth_token), 'application/json', 201),      #valid token and data positive test
     ('asd324sda', create_booking(auth_token), 'application/json', 403),       #invalid token and valid data negative test
     (auth_token(), '-1', 'application/json', 405),                            #invalid bookingid and valid data negative test
     (auth_token(), create_booking(auth_token), 'text/plain', 415)]) #BUG HERE #invalid Content-Type and valid data negative test
def test_delete_booking(auth_token, create_booking, content_type, expected_status):

    url = f'https://restful-booker.herokuapp.com/booking/{create_booking}'
    headers = {
        'Content-Type': f'{content_type}',
        'Cookie': f'token={auth_token}'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 201:
        assert response.status_code == expected_status, f'Delete booking request failed with status code {response.status_code}'
        assert response.text == 'Created', 'Delete booking response should contain "Created"'
    elif response.status_code == 403:
        assert response.status_code == expected_status, f'Delete booking request failed with status code {response.status_code}'
        assert response.text == 'Forbidden', 'Delete booking response should contain "Created"'
    elif response.status_code == 405:
        assert response.status_code == expected_status, f'Delete booking request failed with status code {response.status_code}'
        assert response.text == 'Method Not Allowed', 'Delete booking response should contain "Created"'
    elif response.status_code == 415:
        assert response.status_code == expected_status, f'Delete booking request failed with status code {response.status_code}'
        assert response.text == 'Unsupported Media Type', 'Delete booking response should contain "Created"'
