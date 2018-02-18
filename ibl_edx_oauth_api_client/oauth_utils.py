from django.conf import settings
from django.utils import timezone
from ibl_edx_oauth_api_client.models import OauthCredentials
import datetime
import logging
import requests

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


logger = logging.getLogger(__name__)


def _get_new_access_token(client_id, client_secret):
    """Requests a new access_token and saves it to the DB"""
    host = settings.EDX_HOST.get('host_name')
    protocol = settings.EDX_HOST.get('protocol', 'https')
    endpoint = settings.EDX_HOST.get('access_token_api')
    token_url = urljoin('{}://{}'.format(protocol, host), endpoint)

    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'token_type': 'jwt'
    }

    logger.info("Requesting new access token from: {}".format(token_url))

    response = requests.post(token_url, data=payload)
    token_details = response.json()
    logger.debug("Response: {}".format(response.text))
    _update_oauth_creds(client_id, client_secret, token_details)
    return token_details.get('access_token')


def _update_oauth_creds(client_id, client_secret, token_details):
    """Updates the OAuth Access Token details for `client_id`"""
    query = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    cred, created = OauthCredentials.objects.get_or_create(**query)
    cred.token_created_ts = timezone.now()
    cred.access_token = token_details.get('access_token')
    cred.expires_on = cred.token_created_ts + datetime.timedelta(
        seconds=token_details.get('expires_in'))
    cred.save()


def _token_near_expiration(expires_on, days=10):
    """Returns True if the token is within `days` of expiration"""
    return (expires_on.date() - datetime.date.today()).days <= days


def get_current_access_token():
    """Gets the current access token or retrieves a new one"""
    client_id = settings.EDX_OAUTH.get('client_id')
    secret = settings.EDX_OAUTH.get('client_secret')

    query = {
        'client_id': client_id,
        'client_secret': secret
    }

    creds, created = OauthCredentials.objects.get_or_create(**query)

    if not creds.access_token:
        logger.debug("No access token exists for: {}".format(query))
        access_token = _get_new_access_token(client_id, secret)
    else:
        # Get a new token if it's within X days of expiration
        logger.debug("Access token already exists")
        if _token_near_expiration(creds.expires_on, days=10):
            logger.info("Access token is near expiration, getting a new one")
            access_token = _get_new_access_token(client_id, secret)
        else:
            access_token = creds.access_token

    return access_token
