# pylama:ignore=E501
from html import unescape
from requests import Session
from re import search

from .common.exceptions import LoginError, ActionFailedError


class UserSession():
    """Class representing the session of an logged-in user.

    Args:
        user (str, required) The username used to sign in.
        pwd (str, required) The password used to sign in.

    Attributes:
        sesskey: (str) The session key. (Made accessible for advanced users)
    """

    def __init__(self, user, pwd):
        self._login(user, pwd)

    def _login(self, user, pwd):
        self._session = Session()
        # fill up cookie jar
        r = self._session.get('https://lernplattform.mebis.bayern.de')
        # sign in to get session tokens
        nexturl = 'https://idp.mebis.bayern.de' + search(r'(?<=action=\").*?(?=\")', r.text).group(0)
        r = self._session.post(nexturl, data={'j_username': user, 'j_password': pwd, '_eventId_proceed': ''})
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
        """Make a GET request in the context of the user's session.
            (Made accessible for advanced users.)

        Note: This a wrapper around :func:`requests.get` [documentation here](https://docs.python-requests.org/en/master/api/)
        """
        r = self._session.get(*args, **kwargs)
        return r

    def post(self, *args, **kwargs):
        """Make a POST request in the context of the user's session.
            (Made accessible for advanced users.)

        Note: This a wrapper around :func:`requests.post`. [documentation here](https://docs.python-requests.org/en/master/api/)
        """
        r = self._session.post(*args, **kwargs)
        return r

    def make_survey_choice(self, survey_id: int, choice_id: int):
        """Helper for making survey choices.

        Args:
            survey_id (str | int, required) The id of the survey.
                (Can be found in the url when looking at the survey.)
            choice_id (str | int, required) The id of your choice.
                (Can be found through the devtools inspector.)
        """

        r = self.post('https://lernplattform.mebis.bayern.de/mod/choice/view.php',
                      {'answer': choice_id, 'sesskey': self.sesskey, 'action': 'makechoice', 'id': survey_id},
                      allow_redirects=False)
        if 'location' not in r.headers:
            raise ActionFailedError('Choice couldn`t be set. It likely got disabled by an administrator or the wrong ids were given.')
