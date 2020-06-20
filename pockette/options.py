"""Command-line options and arguments."""

import click

from pockette import COUNT_DEFAULT, SHORT_MIN_DEFAULT, LONG_MIN_DEFAULT


def count_option(func):
    """Option for the number of items to return."""
    return click.option(
        '--count',
        default=COUNT_DEFAULT,
        help=f"Number of sites to show (default: {COUNT_DEFAULT})."
    )(func)


def offset_option(func):
    """Option for the number of items to offset the results."""
    return click.option('--offset', default=0, help="Offset count for results.")(func)


def random_option(func):
    """Option to randomize the items to return."""
    return click.option('--random', 'is_random', is_flag=True, default=False, help="Randomize selection.")(func)


def sort_option(func):
    """Option for changing the sort method."""
    default = 'time'
    return click.option(
        '--sort',
        'sort_order',
        default=default,
        type=click.Choice(['time', 'site']),
        help=f"Sort method (default: {default})."
    )(func)


def reverse_option(func):
    """Option for reversing the result items."""
    return click.option(
        '--reverse', 'reverse_order', is_flag=True, default=False, help="Show selections in reverse."
    )(func)


def include_option(func):
    """Option for including keyword(s)."""
    return click.option(
        '--include', 'include_keywords', help="Include pages with keyword(s) (comma-separated)."
    )(func)


def exclude_option(func):
    """Option for exclusing keyword(s)."""
    return click.option(
        '--exclude', 'exclude_keywords', help="Exclude pages with keyword(s) (comma-separated)."
    )(func)


def start_option(func):
    """Option for setting a start date in the search."""
    return click.option(
        '--start',
        'start_date',
        type=click.DateTime(formats=['%Y-%m-%d']),
        help="Show sites after this date (YYYY-MM-DD)."
    )(func)


def end_option(func):
    """Option for setting an end date in the search."""
    return click.option(
        '--end',
        'end_date',
        type=click.DateTime(formats=['%Y-%m-%d']),
        help="Show sites before this date (YYYY-MM-DD)."
    )(func)


def length_option(func):
    """Option to return short or long items."""
    return click.option(
        '--length',
        'length',
        type=click.Choice(['short', 'long']),
        help=f'Show short (<{SHORT_MIN_DEFAULT} min) or long (>{LONG_MIN_DEFAULT} min) pages.'
    )(func)


def all_option(func):
    """Option to return all items."""
    return click.option('--all', 'show_all', is_flag=True, help="Show all unread results.")(func)


def report_options(func):
    """Common report options."""
    func = all_option(func)
    func = count_option(func)
    func = length_option(func)
    func = end_option(func)
    func = start_option(func)
    func = exclude_option(func)
    func = include_option(func)
    return func


def search_options(func):
    """Common search options."""
    func = random_option(func)
    func = all_option(func)
    func = offset_option(func)
    func = count_option(func)
    func = reverse_option(func)
    func = sort_option(func)
    func = length_option(func)
    func = end_option(func)
    func = start_option(func)
    func = exclude_option(func)
    func = include_option(func)
    return func
