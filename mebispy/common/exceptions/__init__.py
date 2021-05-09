from datetime import date
from requests import Response


class LoginError(Exception):
    def __init__(self, username: str):
        self._username = username
        super().__init__(f'Error during login for user "{username}".'
                         + ' Most likely the password is incorrect.')


class ActionFailedError(Exception):
    def __init__(self, message='Action failed to complete.'):
        super().__init__(message)


class HTTPError(Exception):  # Craft more sophisticated messages.
    def __init__(self, r: Response):
        code = r.status_code
        match code:
            case 400:
                m = 'Bad request. The server could not understand the'\
                    ' request due to invalid syntax.'
            case 401:
                m = 'Unauthorized. The client lacked authentication.'
            case 403:
                m = 'Forbidden. The client authorized to the server but'\
                    ' does not have the rights to access this resource.'
            case 404:
                m = 'Not found. The requested resource could not be found'\
                    ' on this server.'
            case 405:
                m = 'Method not allowed. The request mothod has been disabled'\
                    ' by the server. Most likely POST was used wrongly.'
            case 406:
                m = 'Not acceptable. The content type set in the request'\
                    ' headers can not be matched by the server.'
            case 407:
                m = 'Proxy authentication required. The cllient did not'\
                    ' authorize (correctly). Authorization should be done by'\
                    ' a proxy.'
            case 408:
                m = 'Request timeout. The connection to the server has been'\
                    ' inactive for too long.'
            case 409:
                m = 'Conflict. The request conflicted with the current state'\
                    ' of the server.'
            case 410:
                m = 'Gone. The requested resource has been deleted from the'\
                    ' server.'
            case 411:
                m = 'Length required. Header field "Content-Length" is'\
                    ' missing.'
            case 412:
                m = 'Precontidion failed. The client has indicated conditions'\
                    ' in the headers, which the server does not meet.'
            case 413:
                m = 'Payload too large. The request payload is too large.'
            case 414:
                m = 'URI too long. The URI specified is too long for the'\
                    ' server to interpret.'
            case 415:
                m = 'Unsupported media type. The requested media type is not'\
                    ' supported by the server.'
            case 416:
                m = 'The range specified in the "Range" header field could'\
                    ' not be satisfied.'
            case 417:
                m = 'Expactation failed. The expectation present in the'\
                    ' "Expect" header field could not be met.'
            case 418:
                m = 'I´m a teapot. The server did not wish to fulfill this'\
                    ' request.'
                t = date.today()
                if t.strftime(r'%d-%m') == '01-04':
                    a = str(int(t.strftime(r'%Y')) - 1998)
                    o = ('st' if a.endswith('1') else
                         'nd' if a.endswith('2') else
                         'rd' if a.endswith('3') else
                         'th')
                    m = f'I´m a teapot. Happy 1st of April and {a}{o}'\
                        ' anniversary of the Hyper Text Coffee Pot Control'\
                        ' Protocol!'
            case 421:
                m = 'Misdirected request. The request was sent to a server is'\
                    ' not able to create a response to your request.'
            case 422:
                m = 'Unprocessable entity. The request could not be processed'\
                    ' due to semantic errors.'
            case 423:
                m = 'Locked. The resource you are trying to access is locked.'
            case 424:
                m = 'Failed Dependancy. The request failed due to failure of'\
                    ' a previous request.'
            case 426:
                m = 'Upgrade required. The server refuses to perform the'\
                    ' request using the current protocol but might be willing'\
                    ' to do so after the client upgrades to one of these'\
                    f' protocols: {r.headers["Upgrade"]}'
            case 428:
                m = 'Precondition required. The client has to indicate'\
                    ' preconditions in the headers.'
            case 429:
                m = 'Too many requests. The user has sent too many requests'\
                    ' in a given amount of time ("rate limiting").'
            case 431:
                m = 'Request header fields too large. The client has sent too'\
                    'many headers.'
            case 451:
                m = 'Unavailable for legal reasons. The requested resource'\
                ' cannot legally be provided, such as a web page censored by'\
                ' a government.'
            case 500:
                m = 'Internal server error. The server has encountered a'\
                    'situation it doesn´t know how to handle.'
            case 501:
                m = 'Not implemented. The request method is not supported by'\
                    ' the server and cannot be handled.'
            case 502:
                m = 'Bad gateway. The server working as a gateway got a bad'\
                    ' response.'
            case 503:
                m = 'Service unavailable. The server is not currently able to'\
                    ' respond due to mainenance, overload, etc.'
                t = (r.headers['Retry-After'] if 'Retry-After' in r.headers
                     else None)
                m += f' Try again after {t}.' if t else ''
            case 504:
                m = 'Gateway timeout. The server requested by the gateway did'\
                    ' not respond in time.'
            case 506:
                m = 'Internal configuration error.'
            case 507:
                m = 'Insufficient storage. The request could not be met'\
                    ' because of insufficient storage on the server side.'
            case 508:
                m = 'Loop detected. The server stopped processing the request'\
                    ' since it detected an infinite loop.'
            case 510:
                m = 'Not extended. The request must be extended for the'\
                    ' server to fulfill it.'
            case 511:
                m = 'Network authentication required. The client need to'\
                    ' authenticate to access the network.'
            case _:
                m = 'Unknown error.'
        short_desc = ('Client error,' if code < 500 else
                      'Server error,' if code < 600 else
                      'Unknown,')
        super().__init__(f'{short_desc} {code}: {m} If this issue persists, please'
                         + ' open an issue in the GitHub repository.')
