"""Test searching Pocket data with the `pockette search` command."""

import json
import os
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
import pytest

from pockette import DATA_FILE
from pockette.cli import search


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Temporarily set environment variables."""
    monkeypatch.setenv("POCKET_CONSUMER_KEY", "consumer_key")
    monkeypatch.setenv("POCKET_ACCESS_TOKEN", "access_token")


@pytest.fixture
def fake_pocket_response(scope="module") -> MagicMock:  # pylint: disable=unused-argument
    """Get fake Pocket response."""
    response = MagicMock()

    fake_pocket_response_file = os.path.realpath(
        os.path.join(os.path.dirname(DATA_FILE), '..', 'tests', 'data', 'pocket.json')
    )
    with open(fake_pocket_response_file, 'r', encoding='utf-8') as f_in:
        response.text = json.dumps(json.load(f_in))

    return response


@patch('pockette.pocket_handler.requests.post')
class TestSearch:  # pylint: disable=redefined-outer-name,unused-argument
    """Test searching Pocket data."""

    def test_search(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search)

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '44: ' not in result.output  # Default count is used

    # pylint: disable=unused-argument
    def test_search_missing_consumer_key(self, mock_post: MagicMock, monkeypatch):
        """Test handling for when POCKET_CONSUMER_KEY environment variable is not set."""
        monkeypatch.delenv("POCKET_CONSUMER_KEY", raising=False)
        monkeypatch.setenv("POCKET_ACCESS_TOKEN", "access_token")

        runner = CliRunner()
        result = runner.invoke(search)

        assert result.exit_code == 1

    # pylint: disable=unused-argument
    def test_search_missing_access_token(self, mock_post: MagicMock, monkeypatch):
        """Test handling for when POCKET_ACCESS_TOKEN environment variable is not set."""
        monkeypatch.setenv("POCKET_CONSUMER_KEY", "consumer_key")
        monkeypatch.delenv("POCKET_ACCESS_TOKEN", raising=False)

        runner = CliRunner()
        result = runner.invoke(search)

        assert result.exit_code == 1

    def test_search_bad_json_response(self, mock_post: MagicMock, mock_env_vars):
        """Test handling bad Pocket data JSON response."""
        response = MagicMock()
        response.text = '{"invalid": "json"'

        mock_post.return_value = response

        runner = CliRunner()
        result = runner.invoke(search)

        assert result.exit_code == 1

    def test_search_all(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --all option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--all'])

        assert result.exit_code == 0

        assert 'Pages found (44)' in result.output
        assert '44: ' in result.output

    def test_search_include(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --include option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--include', 'nytimes.com'])

        assert result.exit_code == 0
        assert 'Pages found (18)' in result.output
        assert 'nytimes.com' in result.output

    def test_search_exclude(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --exclude option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--exclude', 'nytimes.com'])

        assert result.exit_code == 0
        assert 'Pages found (26)' in result.output
        assert 'nytimes.com' not in result.output

    def test_search_start_date(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --start option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--start', '2020-01-01'])

        assert result.exit_code == 0
        assert 'Pages found (17)' in result.output

    def test_search_end_date(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --end option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--end', '2019-06-01'])

        assert result.exit_code == 0
        assert 'Pages found (16)' in result.output

    def test_search_short_length(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --lenth=short option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--length', 'short'])

        assert result.exit_code == 0
        assert 'Pages found (10)' in result.output

    def test_search_long_length(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --lenth=long option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--length', 'long'])

        assert result.exit_code == 0
        assert 'Pages found (19)' in result.output

    def test_search_count(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --count option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--count', '5'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '5: ' in result.output
        assert '6: ' not in result.output

    def test_search_sort_by_time(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --sort=time option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--sort', 'time'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: Yes, We Mean Literally Abolish the Police' in result.output

    def test_search_sort_by_site(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --sort=site option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--sort', 'site'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: You Are Not Google' in result.output

    def test_search_sort_by_time_reverse(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --reverse option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--reverse'])  # Default is to sort by time

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: The Rent Racket — ProPublica' in result.output

    def test_search_offset(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --offset option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search, args=['--offset', '1'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: The Virus Will Win' in result.output

    def test_search_random(self, mock_post: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test searching Pocket data with the --random option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(search)
        default_output = result.output

        result = runner.invoke(search, args=['--random'])
        random_output = result.output

        assert result.exit_code == 0
        assert default_output != random_output
