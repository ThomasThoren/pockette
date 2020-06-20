"""Test setting up Pocket CLI with the `pockette setup` command."""

import json
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
import pytest  # type: ignore
from requests import Response

from pockette.cli import setup


@pytest.fixture
def fake_oauth_request_response(scope="module") -> MagicMock:  # pylint: disable=unused-argument
    """Get fake /oauth/request response."""
    response = MagicMock()
    response.text = json.dumps({'code': 'REQUEST_TOKEN'})
    return response


@pytest.fixture
def fake_oath_authorize_response(scope="module") -> MagicMock:  # pylint: disable=unused-argument
    """Get fake /oauth/authorize response."""
    response = MagicMock()
    response.text = json.dumps({'access_token': 'ACCESS_TOKEN'})
    return response


class TestSetup:  # pylint: disable=no-self-use,redefined-outer-name
    """Test setting up Pocket CLI."""

    @patch('pockette.pocket_handler.requests.post')
    def test_setup_new(self, mock_post: MagicMock, monkeypatch, fake_oauth_request_response: MagicMock,
                       fake_oath_authorize_response: MagicMock):
        """Test setting up Pocket CLI for the first time."""
        monkeypatch.delenv("POCKET_CONSUMER_KEY", raising=False)
        monkeypatch.delenv("POCKET_ACCESS_TOKEN", raising=False)

        mock_post.side_effect = [
            fake_oauth_request_response,
            fake_oath_authorize_response
        ]

        runner = CliRunner()
        result = runner.invoke(setup, input='CONSUMER_KEY\nAnyKey\n')

        assert result.exit_code == 0
        assert 'export POCKET_CONSUMER_KEY=CONSUMER_KEY' in result.output
        assert 'export POCKET_ACCESS_TOKEN=ACCESS_TOKEN' in result.output

    def test_setup_existing_dismiss(self, monkeypatch):
        """Test ignoring Pocket CLI setup when it is already configured."""
        monkeypatch.setenv("POCKET_CONSUMER_KEY", "consumer_key")
        monkeypatch.setenv("POCKET_ACCESS_TOKEN", "access_token")

        runner = CliRunner()
        result = runner.invoke(setup, input='n\n')

        assert result.exit_code == 0
        assert 'Pocket environment variables already configured' in result.output

    @patch('pockette.pocket_handler.requests.post')
    def test_setup_existing_update(self, mock_post: MagicMock, monkeypatch, fake_oauth_request_response: MagicMock,
                                   fake_oath_authorize_response: MagicMock):
        """Test setting up Pocket CLI when it is already configured."""
        monkeypatch.setenv("POCKET_CONSUMER_KEY", "consumer_key")
        monkeypatch.setenv("POCKET_ACCESS_TOKEN", "access_token")

        mock_post.side_effect = [
            fake_oauth_request_response,
            fake_oath_authorize_response
        ]

        runner = CliRunner()
        result = runner.invoke(setup, input='y\nCONSUMER_KEY\nAnyKey\n')

        assert result.exit_code == 0
        assert 'export POCKET_CONSUMER_KEY=CONSUMER_KEY' in result.output
        assert 'export POCKET_ACCESS_TOKEN=ACCESS_TOKEN' in result.output

    @patch('pockette.pocket_handler.requests.post')
    def test_setup_bad_consumer_key(self, mock_post: MagicMock, monkeypatch):
        """Test that bad /oauth/request responses are caught."""
        monkeypatch.delenv("POCKET_CONSUMER_KEY", raising=False)
        monkeypatch.delenv("POCKET_ACCESS_TOKEN", raising=False)

        oauth_request_response = Response()
        oauth_request_response.status_code = 403

        mock_post.side_effect = [
            oauth_request_response
        ]

        runner = CliRunner()
        result = runner.invoke(setup, input='CONSUMER_KEY\n')
        assert result.exit_code == 1

    @patch('pockette.pocket_handler.requests.post')
    def test_setup_bad_request_token(self, mock_post: MagicMock, monkeypatch,
                                     fake_oauth_request_response: MagicMock):
        """Test that bad /oauth/authorize responses are caught."""
        monkeypatch.delenv("POCKET_CONSUMER_KEY", raising=False)
        monkeypatch.delenv("POCKET_ACCESS_TOKEN", raising=False)

        oauth_authorize_response = Response()
        oauth_authorize_response.status_code = 403

        mock_post.side_effect = [
            fake_oauth_request_response,
            oauth_authorize_response
        ]

        runner = CliRunner()
        result = runner.invoke(setup, input='CONSUMER_KEY\nAnyKey\n')
        assert result.exit_code == 1
