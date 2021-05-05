# pylama:ignore=E501
from html import unescape
from requests import Session
from re import search

from .common.exceptions import LoginError


class UserSession():
    """Class representing the session of an logged-in user.

    Args:
        user (str, requirede) The username used to sign in.
        pwd (str, requirede) The password used to sign in.

    Attributes:
        sesskey: (str) The session key. (Made accessible for advanced users)
    """

    def __init__(self, user: str, pwd: str):
        self._user = user
        self._pwd = pwd
        self._login()

    def _login(self):
        self._session = Session()
        # fill up cookie jar
        r = self._session.get('https://lernplattform.mebis.bayern.de')
        # sign in to get session tokens
        nexturl = 'https://idp.mebis.bayern.de' + search(r'(?<=action=\").*?(?=\")', r.text).group(0)
        r = self._session.post(nexturl, data={'j_username': self._user, 'j_password': self._pwd, '_eventId_proceed': ''})
        if 'form-error' in r.text:
            raise LoginError(self._user)
        # complete full signin
        nexturl = unescape(search(r'(?<=action=\").*?(?=\")', r.text).group(0))
        rs = unescape(search(r'(?<=name=\"RelayState\" value=\").*?(?=\")', r.text).group(0))
        saml = search(r'(?<=name=\"SAMLResponse\" value=\").*?(?=\")', r.text).group(0)
        r = self._session.post(nexturl, data={'RelayState': rs, 'SAMLResponse': saml})
        # get sesskey
        self.sesskey = search(r'(?<=sesskey\"\:\").*?(?=\")', r.text).group(0)

    def get(self, *args, **kwargs):
        """Make a GET request in the context of the user's session. (Made accessible for advanced users. Arguments are the same as :func:`requests.get`)"""
        r = self._session.get(*args, **kwargs)
        return r

    def post(self, *args, **kwargs):
        """Make a POST request in the context of the user's session. (Made accessible for advanced users. Arguments are the same as :func:`requests.post`)"""
        r = self._session.post(*args, **kwargs)
        return r
