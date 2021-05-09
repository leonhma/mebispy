from html import unescape
from re import search
from typing import Union

from requests import Response, Session

from .common.exceptions import LoginError, HTTPError, ActionFailedError


class UserSession():
    """Class representing the session of a logged-in user.

    Args:
        user (str, required): The username used to sign in.
        pwd (str, required): The password used to sign in.

    Raises:
        :exc:`LoginError`: If the login failed.

    Attributes:
        sesskey (str): The session key (one of them at least).
            (Made accessible for advanced users)
    """

    def __init__(self, user: str, pwd: str):
        self._login(user, pwd)
        self.helpers = self.Helpers(self)

    def _login(self, user, pwd):
        self._session = Session()
        # fill up cookie jar
        r = self.get('https://lernplattform.mebis.bayern.de')
        # sign in to get session tokens
        nexturl = 'https://idp.mebis.bayern.de'\
            + search(r'(?<=action=\").*?(?=\")', r.text).group(0)
        r = self.post(nexturl, data={'j_username': user,
                                     'j_password': pwd,
                                     '_eventId_proceed': ''})
        if 'form-error' in r.text:
            raise LoginError(self._user)
        # complete full signin
        nexturl = unescape(search(r'(?<=action=\").*?(?=\")', r.text).group(0))
        rs = unescape(search(r'(?<=name=\"RelayState\" value=\").*?(?=\")',
                             r.text).group(0))
        saml = search(r'(?<=name=\"SAMLResponse\" value=\").*?(?=\")',
                      r.text).group(0)
        r = self.post(nexturl, data={'RelayState': rs,
                                     'SAMLResponse': saml})
        # get sesskey
        self.sesskey = search(r'(?<=sesskey\"\:\").*?(?=\")', r.text).group(0)

    def get(self, *args, **kwargs) -> Response:
        """Make a GET request in the context of the user's session.
        (Made accessible for advanced users.)

        Raises:
            :exc:`HTTPError`: If the request was answered with an error.

        Note:
            This a wrapper around :func:`requests.get`.
            `docs here
            <https://docs.python-requests.org/en/master/api/#requests.get>`_
        """
        r = self._session.get(*args, **kwargs)
        if r.status_code >= 400:
            raise HTTPError(r)
        return r

    def post(self, *args, **kwargs) -> Response:
        """Make a POST request in the context of the user's session.
        (Made accessible for advanced users.)

        Raises:
            :exc:`HTTPError`: If the request was answered with an error.

        Note:
            This a wrapper around :func:`requests.post`.
            `docs here
            <https://docs.python-requests.org/en/master/api/#requests.post>`_
        """
        r = self._session.post(*args, **kwargs)
        if r.status_code >= 400:
            raise HTTPError(r)
        return r

    def ajax(self, method: str, args: dict) -> dict:
        """Make a request to the ajax endpoint of mebis.
        (Made accessible for advanced users.)

        Args:
            method (str, required): The identifier of the method.
            args (dict, required): The arguments to the method.

        Raises:
            :exc:`ActionFailedError`: If the response indicates an error.

        Returns:
            dict: The reponse data of the request in json form.
        """
        # TODO add documentation
        r = self.post(
            'https://lernplattform.mebis.bayern.de/lib/ajax/service.php',
            params={'sesskey': self.sesskey},
            json=[{"index": 0, "methodname": method, "args": args}]).json()[0]
        if r['error'] is True:
            raise ActionFailedError(
                'The ajax request failed. Check for spelling errors or take a'
                + ' look at the docs.')
        return r['data']

    def make_survey_choice(self,
                           survey_id: Union[int, str],
                           choice_id: Union[int, str]) -> bool:
        """Helper for making survey choices.

        Args:
            survey_id (str | int, required) The id of the survey.
                (Can be found in the url when looking at the survey.)
            choice_id (str | int, required) The id of your choice.
                (Can be found through the devtools inspector.)

        Returns:
            bool: `True` if choice was succesfully set, `False` otherwise
        """

        r = self._post('https://lernplattform.mebis.bayern.de/'
                       + 'mod/choice/view.php',
                       {'answer': choice_id, 'sesskey': self._sesskey,
                        'action': 'makechoice', 'id': survey_id},
                       allow_redirects=False)
        return True if 'location' in r.headers else False
