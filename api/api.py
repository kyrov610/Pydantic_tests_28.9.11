import requests
from serializers.auth_model import AuthResponse
from serializers.booking_model import BookingResponse


def auth_token():
    url = 'https://restful-booker.herokuapp.com/auth'
    headers = {'Content-Type': 'application/json'}
    data = {
        'username': 'admin',
        'password': 'password123'
    }
    response = requests.post(url, headers=headers, json=data)
    response_model = AuthResponse(**response.json())
    return response_model.token


def create_booking(auth_token):
    url = 'https://restful-booker.herokuapp.com/booking'
    headers = {'Content-Type': 'application/json'}
    data = {
        'firstname': 'Jim',
        'lastname': 'Brown',
        'totalprice': 111,
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2018-01-01',
            'checkout': '2019-01-01'
        },
        'additionalneeds': 'Breakfast'
    }
    response = requests.post(url, headers=headers, json=data)
    response_model = BookingResponse(**response.json())
    return response_model.bookingid
