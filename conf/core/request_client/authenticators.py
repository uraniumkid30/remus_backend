from getpass import getpass

from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(
            self, custom_header_data=dict(),
            auth_type='Bearer', Content_Type='application/json',
            Accept_Type="application/json"
    ):
        self.custom_header_data = custom_header_data
        self.token = self.custom_header_data.get("token")
        self.auth_type = auth_type
        self.Content_Type = Content_Type
        self.Accept_Type = Accept_Type

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['Content-Type'] = self.Content_Type
        r.headers['Accept-Type'] = self.Accept_Type
        if self.custom_header_data:
            if self.token is not None:
                # Python 3.6+
                r.headers['Authorization'] = f'{self.auth_type} {self.token}'
            else:
                for key in self.custom_header_data:
                    r.headers[key] = f'{self.custom_header_data[key]}'
        return r