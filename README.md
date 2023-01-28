# Redash API Python Client

python package for interacting with the Redash API

[![view - Documentation](https://img.shields.io/badge/PyPi-0.3.21-blue?style=for-the-badge)](https://pypi.org/project/redash-python "view package on PyPi")
&nbsp;&nbsp;&nbsp;
[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](https://www.blacksuan19.dev/redash-python/ "go to documentation")
&nbsp;&nbsp;&nbsp;
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](# "Build with github actions")

## Features

- Complete access to all endpoints in the Redash API
- Pagination by default
- Duplicate dashboards
- Manage users and groups
- Duplicate queries with differerent source tables

### Implemented Services

- [x] Dashboards
- [x] Queries
- [x] Data Sources
- [x] Alerts
- [x] Users
- [x] Destinations
- [x] Groups
- [x] query_snippets
- [x] Widgets\*

\* widgets endpoint does not support GET requests, only update, delete and
create.

## Getting Started

an API key is required in addition to the instance's host URL.

### Installation

```bash
pip install redash-python
```

### Usage

```python
from redash_python import Redash

rd = Redash(base_url="", api_key="")


# get all dashboards
dashboards = rd.dashboards.get_all()

# get specific dashboards by id
dash = rd.dashboards.get(1)

# get by slug or name
query = rd.queries.get_by_name("my-dashboard")

# get by tags
q = rd.queries.get_by_tags(["my-tag"])

# get without tags
dash = rd.dashboards.get_by_tags(["my-tag"], without=True)

# Duplicate query with a different table as source
ques = rd.queries
ques.duplicate_query_table(
    query=ques.get(1),
    table_map={"old_table": "new_table"},
    tags=["admin", "test"],
    publish=True,
)

# get a list of implemented API endpoints
print(rd.services)

# get a list of implemented endpoints in a service
print(rd.users)
```

for a full list of implemented methods in each service, print the service
object.

```python
>>> print(client.dashboards)
DashboardsService(attributes: ['endpoint'], methods: ['create', 'create_widget', 'delete', 'duplicate', 'exists', 'favorite', 'favorited', 'get', 'get_all', 'get_by_name', 'get_by_tags', 'get_id', 'get_slug', 'paginate', 'publish', 'refresh', 'share', 'unfavorite', 'unpublish', 'update'])
```

for more examples on usage, see examples folder on github.

## Development

before starting development, install dev depndencies:

```bash
pip install redash-python[dev]
```

### Architecture

this library implements a services based architecture splitting each API
endpoint group to its own service, on top of which is the `Redash` class. all
the services share base classes from mixins that make it easier to share common
behavior and allows rapid development for any new endpoints. for instance adding
query_snippets is as simple as:

```python
from .base import BaseService
from .mixins import CommonMixin, NameMixin, PrintMixin


class QSnipsService(CommonMixin, NameMixin, PrintMixin):
    def __init__(self, base: BaseService) -> None:
        # init mixins
        CommonMixin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/query_snippets"
```

### Directory Structure

```bash
redash_python
├── __init__.py
├── redash.py               # Services wrapper
└── services                # implemented services
    ├── base.py             # Base service class
    └── mixins.py           # Mixins for services with shared functionality
```

## Contributing

Contributions are welcome, please open an issue or PR to propse any changes.

## License

[![view - Documentation](https://img.shields.io/badge/License-BSD%202%20Clause-green?style=for-the-badge)](https://github.com/Blacksuan19/redash-python/blob/master/LICENSE "View License")
