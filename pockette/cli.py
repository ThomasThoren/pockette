"""Command line tools for working with Pocket."""

import click

from pockette import VERSION
from pockette.options import report_options, search_options
from pockette.pocket_handler import PocketDataHandler
from pockette.pocket_setup import PocketSetupHandler


@click.group()
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx, *args, **kwargs):  # pylint: disable=unused-argument
    """Command line tools for working with Pocket."""


@click.command(name='help', add_help_option=False)
@click.pass_context
def _help(ctx: click.core.Context):
    """Print the help menu."""
    click.echo(cli.get_help(ctx))


@click.command()
@click.pass_context
def setup(ctx: click.core.Context, **kwargs):  # pylint: disable=unused-argument
    """Set up Pocket CLI."""
    PocketSetupHandler()


@click.command()
@report_options
@click.pass_context
def report(ctx: click.core.Context, **kwargs):  # pylint: disable=unused-argument
    """Create summary report."""
    count = ctx.params['count']
    show_all = ctx.params['show_all']
    length = ctx.params['length']
    start_date = ctx.params['start_date']
    end_date = ctx.params['end_date']
    include_keywords = ctx.params['include_keywords']
    exclude_keywords = ctx.params['exclude_keywords']

    pdh = PocketDataHandler()
    pdh.generate_report(
        count=count, show_all=show_all, length=length, start_date=start_date, end_date=end_date,
        include_keywords=include_keywords, exclude_keywords=exclude_keywords
    )


@click.command()
@search_options
@click.pass_context
def search(ctx: click.core.Context, **kwargs):  # pylint: disable=unused-argument
    """Search through links."""
    count = ctx.params['count']
    offset = ctx.params['offset']
    is_random = ctx.params['is_random']
    sort_order = ctx.params['sort_order']
    reverse_order = ctx.params['reverse_order']
    show_all = ctx.params['show_all']
    length = ctx.params['length']
    start_date = ctx.params['start_date']
    end_date = ctx.params['end_date']
    include_keywords = ctx.params['include_keywords']
    exclude_keywords = ctx.params['exclude_keywords']

    pdh = PocketDataHandler()
    pdh.search_pocket_data(
        count=count, offset=offset, is_random=is_random, sort_order=sort_order,
        reverse_order=reverse_order, show_all=show_all, length=length, start_date=start_date, end_date=end_date,
        include_keywords=include_keywords, exclude_keywords=exclude_keywords
    )


@click.command()
@search_options
@click.pass_context
def read(ctx: click.core.Context, **kwargs):  # pylint: disable=unused-argument
    """Open links in browser."""
    count = ctx.params['count']
    offset = ctx.params['offset']
    is_random = ctx.params['is_random']
    sort_order = ctx.params['sort_order']
    reverse_order = ctx.params['reverse_order']
    show_all = ctx.params['show_all']
    length = ctx.params['length']
    start_date = ctx.params['start_date']
    end_date = ctx.params['end_date']
    include_keywords = ctx.params['include_keywords']
    exclude_keywords = ctx.params['exclude_keywords']

    pdh = PocketDataHandler()
    pdh.search_pocket_data(
        count=count, offset=offset, is_random=is_random, sort_order=sort_order,
        reverse_order=reverse_order, show_all=show_all, length=length, start_date=start_date, end_date=end_date,
        include_keywords=include_keywords, exclude_keywords=exclude_keywords, open_sites=True
    )


cli.add_command(_help)
cli.add_command(setup)
cli.add_command(read)
cli.add_command(report)
cli.add_command(search)
