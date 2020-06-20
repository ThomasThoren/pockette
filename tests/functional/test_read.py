"""Test reading Pocket data with the `pockette read` command."""

import json
import os
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
import pytest  # type: ignore

from pockette import DATA_FILE, COUNT_DEFAULT
from pockette.cli import read


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
    with open(fake_pocket_response_file, 'r') as f_in:
        response.text = json.dumps(json.load(f_in))

    return response


@patch('pockette.pocket_handler.webbrowser.open')
@patch('pockette.pocket_handler.requests.post')
class TestRead:  # pylint: disable=no-self-use,redefined-outer-name,unused-argument
    """Test reading Pocket data."""

    def test_read(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                  fake_pocket_response: dict):
        """Test reading Pocket data."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read)

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert mock_webbrowser.called

    def test_read_all(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                      fake_pocket_response: dict):
        """Test reading Pocket data with the --all option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--all'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert mock_webbrowser.called

    def test_read_include(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                          fake_pocket_response: dict):
        """Test reading Pocket data with the --include option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--include', 'nytimes.com'])

        assert result.exit_code == 0

        assert 'Pages found (18)' in result.output
        assert 'nytimes.com' in result.output
        assert mock_webbrowser.called

    def test_read_exclude(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                          fake_pocket_response: dict):
        """Test reading Pocket data with the --exclude option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--exclude', 'nytimes.com'])

        assert result.exit_code == 0

        assert 'Pages found (26)' in result.output
        assert 'nytimes.com' not in result.output
        assert mock_webbrowser.called

    def test_read_start_date(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                             fake_pocket_response: dict):
        """Test reading Pocket data with the --start option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--start', '2020-01-01'])

        assert result.exit_code == 0
        assert 'Pages found (17)' in result.output
        assert mock_webbrowser.called

    def test_read_end_date(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                           fake_pocket_response: dict):
        """Test reading Pocket data with the --end option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--end', '2019-06-01'])

        assert result.exit_code == 0
        assert 'Pages found (16)' in result.output
        assert mock_webbrowser.called

    def test_read_short_length(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                               fake_pocket_response: dict):
        """Test reading Pocket data with the --lenth=short option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--length', 'short'])

        assert result.exit_code == 0
        assert 'Pages found (10)' in result.output
        assert mock_webbrowser.called

    def test_read_long_length(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                              fake_pocket_response: dict):
        """Test reading Pocket data with the --lenth=long option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--length', 'long'])

        assert result.exit_code == 0
        assert 'Pages found (19)' in result.output
        assert mock_webbrowser.called

    def test_read_count(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                        fake_pocket_response: dict):
        """Test reading Pocket data with the --count option. Check that count default isn't exceeded."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--count', str(COUNT_DEFAULT + 1)])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert f'{COUNT_DEFAULT}: ' in result.output
        assert f'{COUNT_DEFAULT + 1}: ' not in result.output
        assert mock_webbrowser.call_count == COUNT_DEFAULT * 2


    def test_read_sort_by_time(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                               fake_pocket_response: dict):
        """Test reading Pocket data with the --sort=time option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--sort', 'time'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: Yes, We Mean Literally Abolish the Police' in result.output
        assert mock_webbrowser.called

    def test_read_sort_by_site(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                               fake_pocket_response: dict):
        """Test reading Pocket data with the --sort=site option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--sort', 'site'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: You Are Not Google' in result.output
        assert mock_webbrowser.called

    def test_read_sort_by_time_reverse(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                                       fake_pocket_response: dict):
        """Test reading Pocket data with the --reverse option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--reverse'])  # Default is to sort by time

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: The Rent Racket — ProPublica' in result.output
        assert mock_webbrowser.called

    def test_read_offset(self, mock_post: MagicMock, mock_webbrowser: MagicMock, mock_env_vars,
                         fake_pocket_response: dict):
        """Test reading Pocket data with the --offset option."""
        mock_post.return_value = fake_pocket_response

        runner = CliRunner()
        result = runner.invoke(read, args=['--offset', '1'])

        assert result.exit_code == 0
        assert 'Pages found (44)' in result.output
        assert '1: The Virus Will Win' in result.output
        assert mock_webbrowser.called
