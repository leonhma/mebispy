# pylama:ignore=E501
class LoginError(Exception):
    def __init__(self, username: str):
        self._username = username
        super().__init__(f'Error during login for user "{username}". Most likely the password is incorrect.')
