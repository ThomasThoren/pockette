"""Set up Pocket CLI."""

import json
import os
import sys

import click
import requests


class PocketSetupHandler:  # pylint: disable=too-few-public-methods
    """Set up Pocket CLI."""

    def __init__(self):
        """Set up Pocket CLI."""
        # Check if already set up
        if os.getenv('POCKET_CONSUMER_KEY') and os.getenv('POCKET_ACCESS_TOKEN'):
            if not click.confirm('Pocket environment variables already configured. Proceed?'):
                return

            click.echo('')

        click.echo(
            'Follow these steps to authenticate the Pocket API '
            '(https://getpocket.com/developer/docs/authentication):\n'
        )

        click.echo(
            '1. Create an application (https://getpocket.com/developer/apps/new) with "Retrieve" permission '
            'and "Mac" platform.'
        )

        consumer_key = click.prompt("2. Enter your application's consumer key", type=str)

        # Get request token
        request_token = self._get_request_token(consumer_key)

        # Authorize the application in a browser window
        url = f'https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=https://google.com'
        click.prompt(f'3. Authorize your application: {url}. Enter any key when finished')

        # Convert request token to an access token
        access_token = self._get_access_token(consumer_key, request_token)

        # Save consumer_key and access_token to environment variables
        click.echo(
            '4. Save your consumer key and access token as environment variables:\n'
            f'  export POCKET_CONSUMER_KEY={consumer_key}\n'
            f'  export POCKET_ACCESS_TOKEN={access_token}\n\n'
            'You may want to save these values somewhere permanent, such as your ~/.bash_profile start-up file:\n'
            f'  echo \'export POCKET_CONSUMER_KEY={consumer_key}\' >> ~/.bash_profile\n'
            f'  echo \'export POCKET_ACCESS_TOKEN={access_token}\' >> ~/.bash_profile'
        )

    @staticmethod
    def _get_request_token(consumer_key: str) -> str:
        """Get an OAuth request token."""
        headers = {"Content-Type": "application/json; charset=UTF8", "X-Accept": "application/json"}
        data = {"consumer_key": consumer_key, "redirect_uri": "https://google.com"}

        try:
            response = requests.post('https://getpocket.com/v3/oauth/request', headers=headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            click.echo(f'HTTP error: {response.text}')
            if response.status_code == 403:
                click.echo(
                    'Verify that you have the correct consumer key and that you set the "Retrive" permission.'
                )

            sys.exit(1)

        return json.loads(response.text)['code']

    @staticmethod
    def _get_access_token(consumer_key: str, request_token: str) -> str:
        """Get an OAuth access token."""
        headers = {"Content-Type": "application/json; charset=UTF8", "X-Accept": "application/json"}
        data = {'consumer_key': consumer_key, 'code': request_token}

        try:
            response = requests.post('https://getpocket.com/v3/oauth/authorize', headers=headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            click.echo(f'HTTP error: {response.text}')
            if response.status_code == 403:
                click.echo('Did you authorize the application?')

            sys.exit(1)

        return json.loads(response.text)['access_token']
