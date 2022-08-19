# Redash API Python Client

python package for interacting with the Redash API

## Getting Started

an API key is required in addition to the instance's host URL.

## Installation

```bash
pip install redash-python
```

### Usage

```python
from redash_python import Redash

client = Redash(base_url="", api_key="")


# get all dashboards
dashboards = client.dashboards.get_all()

# get specific dashboards by id
dash = client.dashboards.get(1)

# get by slug or name
query = client.queries.get_by_name("my-dashboard")

# get by tags
q = client.queries.get_by_tags(["my-tag"])

# get without tags
dash = client.dashboards.get_by_tags(["my-tag"], without=True)

# Duplicate query with a different table as source
ques = redash.queries
ques.duplicate_query_table(
    query=ques.get(1),
    table_map={"old_table": "new_table"},
    tags=["admin", "test"],
    publish=True,
)

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
├── redash.py               # Services wrapper
└── services                # implemented services
    ├── base.py             # Base service class
    └── mixins.py           # Mixins for services with shared functionality
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

### Meta features

- [x] pagination
- [x] Duplicate dashboards
- [x] Duplicate query with a different source table from same data source

for a full list of implemented methods in each service, print the service
object.

```python

>>> print(client.dashboards)
DashboardsService(methods: ['archive', 'create', 'get', 'get_all', 'get_by_slug', 'get_id', 'get_slug', 'publish', 'unarchive', 'unpublish', 'update'])
```
