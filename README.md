# Redash API Python Client

python package for interacting with the Redash API

## Getting Started

an API key is required in addition to the instance's host URL.

## Installation

```bash
pip install redash-python
```

### Usage

the API uses SimpleNameSpace objects to represent resources instead of
dictionaries. this allows access to the resource's attributes using dot
notation.

```python
from redash_python import Redash

client = Redash(base_url="", api_key="")


# get all dashboards
dashboards = client.dashboards.get_all().results

# get specific dashboards by id
dash = client.dashboards.get(1)

# get by slug
dash = client.dashboards.get_by_slug("my-dashboard")

# print slug
print(dash.slug)

# get dashboard widgets
print(dash.widgets)

# get a list of implemented API endpoints
print(client.services)

# get a list of implemented endpoints in a service
print(client.policies)
```

## Development

before starting development, install required packages in `requirements.txt`

```bash
pip install -r requirements.txt
```

### Architecture

this library implements a services based architecture splitting each API
endpoint group to its own service, on top of which is the `Redash` class.

```bash
redash_python
├── __init__.py
├── redash.py              # services wrapper
├── utils                  # exceptions, encoder, etc.
└── services               # implemented services

```

### Implemented Services

- [x] Dashboards
- [x] Queries
- [x] Data Sources
- [x] Alerts
- [x] Users
- [x] Destinations
- [x] Groups
- [x] query_snippets

for a full list of implemented methods in each service, print the service
object.

```python

>>> print(client.dashboards)
DashboardsService(methods: ['archive', 'create', 'get', 'get_all', 'get_by_slug', 'get_id', 'get_slug', 'publish', 'unarchive', 'unpublish', 'update'])
```
