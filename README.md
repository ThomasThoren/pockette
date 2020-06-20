# `pockette`: Pocket command-line interface

Command line tools for working with Pocket data.

- [Requirements](#requirements)
- [Setup](#setup)
  - [Dependencies](#dependencies)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Commands](#commands)
  - [Options](#options)
- [Development](#development)
  - [Tests](#tests)
  - [Lint checks](#lint-checks)
  - [Type checks](#type-checks)

## Requirements

- Python 3.7
- Pocket API credentials

## Setup

### Dependencies

```shell
pip install pockette
```

### Configuration

Set the `POCKET_CONSUMER_KEY` and `POCKET_ACCESS_TOKEN` environment variables. Use the `pockette setup` command for help.

## Usage

### Commands

#### `pockette setup`

Create a Pocket application and authorize it to read your data.

```shell
pockette setup
```

#### `pockette report`

Create an overview report of all data.

```shell
pockette report
```

#### `pockette search`

Search for specific links.

```shell
pockette search
```

#### `pockette read`

Search for links and open them in a browser.

```shell
pockette read
```

### Options

#### `--help`

Show the help messages for each command.

#### `--count`

The number of links to select.

#### `--offset`

Offset the links selection by this count.

#### `--random`

Randomize the links selection.

#### `--sort time/site`

Sort links by chronological (default) or alphabetical order.

#### `--reverse`

Sort links in the reverse order.

#### `--include`

Include links with these keyword(s) (comma-separated).

#### `--exclude`

Exclude links with these keyword(s) (comma-separated).

#### `--start YYYY-MM-DD`

Show links after this date.

#### `--end YYYY-MM-DD`

Show links before this date.

#### `--length short/long`

Show only short (<4 minutes) or long (>10 minutes) links.

#### `--all`

Show all unread links. Overrides all other search options.

## Development

Install development dependencies.

```shell
pip install -e .[dev]
```

### Tests

```shell
make test
```

### Lint checks

```shell
make lint
```

### Type checks

```shell
make typecheck
```
