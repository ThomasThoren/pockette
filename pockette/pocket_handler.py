"""Search, analyze, and read Pocket bookmarks."""

from datetime import datetime, timedelta
import json
import os
import random
import sys
from typing import Dict, List
import webbrowser

import click
import requests

from pockette import DATA_FILE, COUNT_DEFAULT, SHORT_MIN_DEFAULT, LONG_MIN_DEFAULT


class PocketDataHandler:
    """Handle Pocket data."""

    data_file = DATA_FILE

    count_default = COUNT_DEFAULT
    short_min_default = SHORT_MIN_DEFAULT
    long_min_default = LONG_MIN_DEFAULT

    separator_length = 42
    title_width = 50
    read_url = 'https://app.getpocket.com/read'

    def __init__(self):
        self.pocket_data = self._download_pocket_data()

    @staticmethod
    def _download_pocket_data() -> dict:
        """Download Pocket data."""
        try:
            consumer_key = os.environ['POCKET_CONSUMER_KEY']
        except KeyError:
            click.echo(
                'Consumer key environment variable is not set (POCKET_CONSUMER_KEY). '
                'Run `pockette setup` for help.'
            )
            sys.exit(1)

        try:
            access_token = os.environ['POCKET_ACCESS_TOKEN']
        except KeyError:
            click.echo(
                'Access token environment variable is not set (POCKET_ACCESS_TOKEN). '
                'Run `pockette setup` for help.'
            )
            sys.exit(1)

        headers = {"Content-Type": "application/json; charset=UTF8", "X-Accept": "application/json"}
        data = {
            'consumer_key': consumer_key,
            'access_token': access_token,
            'detailType': 'complete',
            'sort': 'newest',
            'state': 'unread',
            'count': '100000',
        }

        response = requests.post('https://getpocket.com/v3/get', headers=headers, json=data)

        try:
            pocket_data = json.loads(response.text)
        except json.JSONDecodeError:
            click.echo(f'ERROR loading Pocket data: {response.reason} ({response.status_code}): {response.text}')
            sys.exit(1)

        return pocket_data

    # pylint: disable=too-many-arguments
    def generate_report(self, count: int = None, show_all: bool = False, length: str = None,
                        include_keywords: str = None, exclude_keywords: str = None,
                        end_date: datetime = None, start_date: datetime = None):
        """Generate report for Pocket data."""
        if show_all:
            count = None

        links = self._filter_links(
            include_keywords=include_keywords,
            exclude_keywords=exclude_keywords,
            end_date=end_date,
            start_date=start_date,
            length=length
        )

        domains_counts = self._get_links_domains_counts(links)
        links_ages = self._get_links_ages(links)

        self._print_centered_section_title('Summary', initial_section=True)
        click.echo('{:5,} unread pages across {:,} sites'.format(len(links), len(set(domains_counts))))
        click.echo('{:5,} unread pages older than 1 month'.format(len(links_ages['one_month'])))
        click.echo('{:5,} unread pages older than 3 months'.format(len(links_ages['three_months'])))
        click.echo('{:5,} unread pages older than 6 months'.format(len(links_ages['six_months'])))
        click.echo('{:5,} unread pages older than 9 months'.format(len(links_ages['nine_months'])))
        click.echo('{:5,} unread pages older than 1 year'.format(len(links_ages['year'])))

        self._print_centered_section_title('Most-common websites (unread)')
        self._print_domain_stats(domains_counts, max_count=count)

    @staticmethod
    def _is_match(keywords: str, item: dict) -> bool:
        """Determine if this Pocket item matches any of the specified keywords."""
        item_components = [i.lower() for i in (item['resolved_title'], item['resolved_url'], item['excerpt'])]

        is_a_match = False

        for keyword in keywords.lower().split(','):
            keyword = keyword.strip()

            if any(keyword in item_component for item_component in item_components):
                is_a_match = True
                break

        return is_a_match

    @staticmethod
    def _get_current_datetime() -> datetime:  # pragma: no cover
        """For easier test mocking."""
        return datetime.now()

    # pylint: disable=too-many-branches,too-many-statements,too-many-arguments,too-many-locals
    def _filter_links(self, include_keywords: str = None, exclude_keywords: str = None,
                      end_date: datetime = None, start_date: datetime = None, length: str = None) -> List[dict]:
        """Filter and analyze Pocket links."""
        filtered_links = []

        for link in self.pocket_data['list'].values():
            if include_keywords and not self._is_match(include_keywords, link):
                continue

            if exclude_keywords and self._is_match(exclude_keywords, link):
                continue

            time_added = datetime.fromtimestamp(int(link['time_added']))
            if end_date and time_added >= end_date:
                continue

            if start_date and time_added <= start_date:
                continue

            time_to_read = link.get('time_to_read')
            if length == 'short' and isinstance(time_to_read, int) and time_to_read > self.short_min_default:
                continue

            if length == 'long' and isinstance(time_to_read, int) and time_to_read < self.long_min_default:
                continue

            filtered_links.append(link)

        return filtered_links

    @staticmethod
    def _get_links_domains_counts(links: List[dict]) -> Dict[str, int]:
        """Count the occurrences of each domain."""
        domain_counts = {}
        for link in links:
            url = link['resolved_url'].split('//')[1].split('/')[0]
            if url not in domain_counts:
                domain_counts[url] = 0

            domain_counts[url] += 1

        return domain_counts

    def _get_links_ages(self, links: list) -> Dict[str, list]:
        """Organize links by age."""
        link_ages: Dict[str, list] = {
            'year': [],
            'nine_months': [],
            'six_months': [],
            'three_months': [],
            'one_month': [],
        }

        for link in links:
            time_added = datetime.fromtimestamp(int(link['time_added']))

            if time_added < (self._get_current_datetime() - timedelta(days=365)):
                link_ages['year'].append(link)

            if time_added < (self._get_current_datetime() - timedelta(days=9*30)):
                link_ages['nine_months'].append(link)

            if time_added < (self._get_current_datetime() - timedelta(days=6*30)):
                link_ages['six_months'].append(link)

            if time_added < (self._get_current_datetime() - timedelta(days=3*30)):
                link_ages['three_months'].append(link)

            if time_added < (self._get_current_datetime() - timedelta(days=1*30)):
                link_ages['one_month'].append(link)

        return link_ages

    def _get_pocket_item_url(self, item_id: str) -> str:
        """Get a Pocket item's URL."""
        return f'{self.read_url}/{item_id}'

    # pylint: disable=too-many-locals,too-many-arguments
    def search_pocket_data(self, count: int = COUNT_DEFAULT, offset: int = 0, is_random: bool = False,
                           sort_order: str = 'time', reverse_order: bool = False,
                           show_all: bool = False, open_sites: bool = False, length: str = None,
                           include_keywords: str = None, exclude_keywords: str = None,
                           end_date: datetime = None, start_date: datetime = None):
        """Search through Pocket bookmarks."""
        links = self._filter_links(
            include_keywords=include_keywords,
            exclude_keywords=exclude_keywords,
            end_date=end_date,
            start_date=start_date,
            length=length
        )

        click.echo('\nPages found ({:,})\n{}'.format(len(links), '-'*self.separator_length))

        if sort_order == 'time':
            links = list(reversed(sorted(links, key=lambda x: x['time_added'])))
        elif sort_order == 'site':
            links = list(sorted(
                links,
                key=lambda x: x['resolved_url'].split('//')[1].split('www.')[-1].split('/')[0]
            ))

        if reverse_order:
            links = list(reversed(links))

        if is_random:
            random.shuffle(links)

        if isinstance(offset, int) and offset >= 0:
            links = links[offset:]

        for i, link in enumerate(links, 1):
            url = link['resolved_url']
            pocket_url = self._get_pocket_item_url(link['item_id'])

            self._print_page(title=link['resolved_title'], pocket_url=pocket_url, url=url, index=i)

            if open_sites and i <= self.count_default:
                webbrowser.open(pocket_url)
                webbrowser.open(url)

                if i == self.count_default and count > self.count_default:
                    click.echo(f'\nOpening only the first {self.count_default} new tabs for better performance.')
                    break

            if i == count and not show_all:
                break

    def _print_centered_section_title(self, label: str, initial_section: bool = False):
        """Print a section title."""
        if not initial_section:
            click.echo('')

        click.echo(f' {label} '.center(self.separator_length, '─'))

    def _print_page(self, title: str, pocket_url: str, url: str, index: int):
        """Print a single Pocket bookmark.

        Ex.
        1. The Head Line  https://app.getpocket.com/read/ABC123  https://www.nytimes.com/news/of/the/day
        """
        prefix = '{:2}: '.format(index)

        if len(title) > self.title_width:
            title = title[:self.title_width]
            title_pieces = title.split(' ')[:-1]

            if len(' '.join(title_pieces)) > (self.title_width-3):
                title_pieces = title_pieces[:-1]

            title = ' '.join(title_pieces) + '...'

        click.echo(
            f'{prefix}{title:{self.title_width}.{self.title_width}} '
            f'{pocket_url:{self.separator_length}.{self.separator_length}} {url}'
        )

    @staticmethod
    def _print_domain_stats(domain_counts: Dict[str, int], max_count: int = None):
        """Print domains and their stats."""
        urls = tuple(reversed(sorted(domain_counts.items(), key=lambda x: x[1])))

        if not max_count:
            max_count = len(urls)

        for i, (url, url_count) in enumerate(urls[:max_count], 1):
            click.echo('{:{}}: {} ({})'.format(i, len(str(max_count)), url, url_count))
