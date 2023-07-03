import requests
from mocked import Mocked

SIGNIN_URL = 'https://app.alpha3d.io/alphaar/auth/oauth/token?grant_type=password'
class Login:
    def __init__(self, username, password, mocked=False):
        self.username = username
        self.password = password
        self.mocked = mocked

    def sign_in(self):
        if self.mocked:
            return Mocked.mocked_access_token()
        token = None
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic c2VsZi1zZXJ2aWNlOg=='}
        data = {
            'username': self.username,
            'password': self.password
        }

        try:
            response = requests.request('POST', SIGNIN_URL, headers=headers, data=data)
            if response.status_code == 200:
                print(response.json())
                token = response.json().get('access_token')
                if token:
                    print("Successfully logged in! Token: " + token)
                else:
                    print("An error occurred while logging in.")
            elif response.status_code == 401:
                print("User login failed. Response code: 401")
            else:
                print("An error occurred while logging in. Error code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("There was an error sending the request:", e)

        return token
