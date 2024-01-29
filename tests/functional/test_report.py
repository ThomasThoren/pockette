"""Test summarizing Pocket data with the `pockette report` command."""

import datetime
import json
import os
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
import pytest

from pockette import DATA_FILE
from pockette.cli import report


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


@patch('pockette.pocket_handler.PocketDataHandler._get_current_datetime')
@patch('pockette.pocket_handler.requests.post')
class TestReport:  # pylint: disable=too-few-public-methods,redefined-outer-name,unused-argument
    """Test Pocket data report."""

    def test_report(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars, fake_pocket_response: dict):
        """Test Pocket data report."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report)

        assert result.exit_code == 0

        assert '44 unread pages across 24 sites' in result.output

        assert '32 unread pages older than 1 month' in result.output
        assert '30 unread pages older than 3 months' in result.output
        assert '26 unread pages older than 6 months' in result.output
        assert '20 unread pages older than 9 months' in result.output
        assert '17 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (18)' in result.output
        assert '2: www.wired.com (3)' in result.output
        assert '3: www.theatlantic.com (2)' in result.output
        assert '4: www.propublica.org (1)' in result.output
        assert '5: www.themarshallproject.org (1)' in result.output
        assert '6: features.propublica.org (1)' in result.output
        assert '7: blog.rapid7.com (1)' in result.output
        assert '8: www.oreilly.com (1)' in result.output
        assert '9: noisey.vice.com (1)' in result.output
        assert '10: www.newyorker.com (1)' in result.output

    def test_report_all(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                        fake_pocket_response: dict):
        """Test report with the --all option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--all'])

        assert result.exit_code == 0

        assert '44 unread pages across 24 sites' in result.output

        assert '32 unread pages older than 1 month' in result.output
        assert '30 unread pages older than 3 months' in result.output
        assert '26 unread pages older than 6 months' in result.output
        assert '20 unread pages older than 9 months' in result.output
        assert '17 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (18)' in result.output
        assert '2: www.wired.com (3)' in result.output
        assert '3: www.theatlantic.com (2)' in result.output
        assert '4: www.propublica.org (1)' in result.output
        assert '5: www.themarshallproject.org (1)' in result.output
        assert '6: features.propublica.org (1)' in result.output
        assert '7: blog.rapid7.com (1)' in result.output
        assert '8: www.oreilly.com (1)' in result.output
        assert '9: noisey.vice.com (1)' in result.output
        assert '10: www.newyorker.com (1)' in result.output
        assert '11: blog.bradfieldcs.com (1)' in result.output
        assert '12: medium.com (1)' in result.output
        assert '13: www.wbur.org (1)' in result.output
        assert '14: www.theverge.com (1)' in result.output
        assert '15: source.opennews.org (1)' in result.output
        assert '16: www.washingtonpost.com (1)' in result.output
        assert '17: strengthrunning.com (1)' in result.output
        assert '18: google.github.io (1)' in result.output
        assert '19: www.vox.com (1)' in result.output
        assert '20: www.outsideonline.com (1)' in result.output
        assert '21: flowingdata.com (1)' in result.output
        assert '22: www.podiumrunner.com (1)' in result.output
        assert '23: www.texastribune.org (1)' in result.output
        assert '24: www.texasmonthly.com (1)' in result.output

    def test_report_include(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                            fake_pocket_response: dict):
        """Test report with the --include option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--include', 'nytimes.com'])

        assert result.exit_code == 0

        assert '18 unread pages across 1 sites' in result.output

        assert '12 unread pages older than 1 month' in result.output
        assert '10 unread pages older than 3 months' in result.output
        assert '10 unread pages older than 6 months' in result.output
        assert '6 unread pages older than 9 months' in result.output
        assert '5 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (18)' in result.output

    def test_report_exclude(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                            fake_pocket_response: dict):
        """Test report with the --exclude option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--exclude', 'nytimes.com'])

        assert result.exit_code == 0

        assert '26 unread pages across 23 sites' in result.output

        assert '20 unread pages older than 1 month' in result.output
        assert '20 unread pages older than 3 months' in result.output
        assert '16 unread pages older than 6 months' in result.output
        assert '14 unread pages older than 9 months' in result.output
        assert '12 unread pages older than 1 year' in result.output

        assert '1: www.wired.com (3)' in result.output
        assert '2: www.theatlantic.com (2)' in result.output
        assert '3: www.propublica.org (1)' in result.output
        assert '4: www.themarshallproject.org (1)' in result.output
        assert '5: features.propublica.org (1)' in result.output
        assert '6: blog.rapid7.com (1)' in result.output
        assert '7: www.oreilly.com (1)' in result.output
        assert '8: noisey.vice.com (1)' in result.output
        assert '9: www.newyorker.com (1)' in result.output
        assert '10: blog.bradfieldcs.com (1)' in result.output

    def test_report_start_date(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                               fake_pocket_response: dict):
        """Test report with the --start option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--start', '2020-01-01'])

        assert result.exit_code == 0

        assert '17 unread pages across 8 sites' in result.output

        assert '5 unread pages older than 1 month' in result.output
        assert '3 unread pages older than 3 months' in result.output
        assert '0 unread pages older than 6 months' in result.output
        assert '0 unread pages older than 9 months' in result.output
        assert '0 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (8)' in result.output
        assert '2: www.wired.com (2)' in result.output
        assert '3: www.theatlantic.com (2)' in result.output
        assert '4: www.outsideonline.com (1)' in result.output
        assert '5: flowingdata.com (1)' in result.output
        assert '6: www.podiumrunner.com (1)' in result.output
        assert '7: www.texastribune.org (1)' in result.output
        assert '8: www.texasmonthly.com (1)' in result.output

    def test_report_end_date(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                             fake_pocket_response: dict):
        """Test report with the --end option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--end', '2019-06-01'])

        assert result.exit_code == 0

        assert '16 unread pages across 13 sites' in result.output

        assert '16 unread pages older than 1 month' in result.output
        assert '16 unread pages older than 3 months' in result.output
        assert '16 unread pages older than 6 months' in result.output
        assert '16 unread pages older than 9 months' in result.output
        assert '16 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (4)' in result.output
        assert '2: www.propublica.org (1)' in result.output
        assert '3: www.themarshallproject.org (1)' in result.output
        assert '4: features.propublica.org (1)' in result.output
        assert '5: blog.rapid7.com (1)' in result.output
        assert '6: www.oreilly.com (1)' in result.output
        assert '7: noisey.vice.com (1)' in result.output
        assert '8: www.newyorker.com (1)' in result.output
        assert '9: blog.bradfieldcs.com (1)' in result.output
        assert '10: medium.com (1)' in result.output

    def test_report_short_length(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                                 fake_pocket_response: dict):
        """Test report with the --lenth=short option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--length', 'short'])

        assert result.exit_code == 0

        assert '10 unread pages across 8 sites' in result.output

        assert '8 unread pages older than 1 month' in result.output
        assert '8 unread pages older than 3 months' in result.output
        assert '6 unread pages older than 6 months' in result.output
        assert '4 unread pages older than 9 months' in result.output
        assert '3 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (3)' in result.output
        assert '2: www.propublica.org (1)' in result.output
        assert '3: noisey.vice.com (1)' in result.output
        assert '4: www.washingtonpost.com (1)' in result.output
        assert '5: google.github.io (1)' in result.output
        assert '6: www.outsideonline.com (1)' in result.output
        assert '7: flowingdata.com (1)' in result.output
        assert '8: www.texasmonthly.com (1)' in result.output

    def test_report_long_length(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                                fake_pocket_response: dict):
        """Test report with the --lenth=long option."""
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--length', 'long'])

        assert result.exit_code == 0

        assert '19 unread pages across 14 sites' in result.output

        assert '17 unread pages older than 1 month' in result.output
        assert '16 unread pages older than 3 months' in result.output
        assert '15 unread pages older than 6 months' in result.output
        assert '13 unread pages older than 9 months' in result.output
        assert '11 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (6)' in result.output
        assert '2: www.propublica.org (1)' in result.output
        assert '3: www.themarshallproject.org (1)' in result.output
        assert '4: features.propublica.org (1)' in result.output
        assert '5: noisey.vice.com (1)' in result.output
        assert '6: www.newyorker.com (1)' in result.output
        assert '7: medium.com (1)' in result.output
        assert '8: www.wbur.org (1)' in result.output
        assert '9: www.theverge.com (1)' in result.output
        assert '10: source.opennews.org (1)' in result.output

    def test_report_count(self, mock_post: MagicMock, mock_now: MagicMock, mock_env_vars,
                          fake_pocket_response: dict):
        """Test report with the --count option.

        This should still show the same overall stats, but limit the number of most-common sites.
        """
        mock_post.return_value = fake_pocket_response
        mock_now.return_value = datetime.datetime(2020, 6, 12, 10, 0, 0)

        runner = CliRunner()
        result = runner.invoke(report, args=['--count', '5'])

        assert result.exit_code == 0

        assert '44 unread pages across 24 sites' in result.output

        assert '32 unread pages older than 1 month' in result.output
        assert '30 unread pages older than 3 months' in result.output
        assert '26 unread pages older than 6 months' in result.output
        assert '20 unread pages older than 9 months' in result.output
        assert '17 unread pages older than 1 year' in result.output

        assert '1: www.nytimes.com (18)' in result.output
        assert '2: www.wired.com (3)' in result.output
        assert '3: www.theatlantic.com (2)' in result.output
        assert '4: www.propublica.org (1)' in result.output
        assert '5: www.themarshallproject.org (1)' in result.output
