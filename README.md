# IBL edX OAuth API Client

Helper Django application that simplifies the OAuth2 authorization process between an external service and Open edX.

It exchanges Open edX OAuth2 `client_id` and `client_secret` credentials for an `access_token` that is saved to its database and made available to other processes.

## Usage

Use the following wherever you need to make a call to Open edX that is protected by an authorization layer.

```python
from ibl_edx_oauth_api_client import oauth_utils

# URL of your Open edX platform's protected API endpoint
url = 'https://your-open-edx-platform/some-protected-api-endpoint'

token = oauth_utils.get_current_access_token()
headers = {'Authorization': 'JWT {}'.format(token)}

response = requests.get(url=url, headers=headers)
```

## Setup

### Installation

Clone and install the application.

```bash
$ pip install -v git+https://github.com/ibleducation/ibl-edx-oauth-api-client.git
```

### Django

#### Add `ibl_edx_oauth_api_client` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...,
    'ibl_edx_oauth_api_client'
]
```

#### Add your Open edX Platform's Credentials

Define the following in your settings:

A dictionary named `EDX_OAUTH`:

```python
EDX_OAUTH = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret'
}
```

A dictionary named `EDX_HOST`:

```python
EDX_HOST = {
    'host_name': 'your-open-edx-platform.com',
    'protocol': 'https',
    'access_token_api': '/oauth2/access_token',
}
```

### Migrations

Run migrations to add the `OauthCredentials` table to the database.

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
