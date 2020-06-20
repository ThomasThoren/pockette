"""Test general `pockette` commands."""

from click.testing import CliRunner

from pockette import VERSION
from pockette.cli import cli, _help


class TestPocket:  # pylint: disable=no-self-use
    """Test general commands."""

    def test_group_name_only(self):
        """Test that the based `pockette` command shows the help menu."""
        runner = CliRunner()
        result = runner.invoke(cli)

        assert result.exit_code == 0
        assert 'Usage: ' in result.output

    def test_help_command(self):
        """Test the `pockette help` command."""
        runner = CliRunner()
        result = runner.invoke(_help)

        assert result.exit_code == 0
        assert 'Usage: ' in result.output

    def test_help_option(self):
        """Test the `pockette --help` option."""
        runner = CliRunner()
        result = runner.invoke(cli, args=['--help'])

        assert result.exit_code == 0
        assert 'Usage: ' in result.output

    def test_version(self):
        """Test the `pockette --version` option."""
        runner = CliRunner()
        result = runner.invoke(cli, args=['--version'])

        assert result.exit_code == 0
        assert VERSION in result.output
