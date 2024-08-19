# Python client and module for BGP Ranking

Queries BGP Ranking.

## Installation

```bash
pip install pybgpranking2
```

## Usage

### Command line

You can use the `bgpranking` command to query the instance:

```bash
bgpranking -h
usage: bgpranking [-h] [--url URL] [--date DATE] {index,simple,status} ...

Run a query against BGP Ranking

options:
  -h, --help            show this help message and exit
  --url URL             URL of the instance.
  --date DATE           Date of the dataset required

Available commands:
  {index,simple,status}

```

### Library

See [API Reference](https://pybgpranking.readthedocs.io/en/latest/api_reference.html)
