from __future__ import unicode_literals
from django.db import models


class OauthCredentials(models.Model):
    """Stores the OAuth credentials"""
    client_id = models.TextField()
    client_secret = models.TextField()
    token_created_ts = models.DateTimeField(null=True, default=None)
    expires_on = models.DateTimeField(null=True, default=None)
    access_token = models.TextField(default='')
