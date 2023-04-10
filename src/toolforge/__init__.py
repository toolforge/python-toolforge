# This file is part of Toolforge python helper library
# Copyright (C) 2013, 2017 Kunal Mehta <legoktm@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Small library for common tasks on Wikimedia Toolforge
"""
import functools
import os
import stat
from typing import IO
from typing import Any
from typing import Callable
from typing import Optional

import decorator
import pymysql
import requests

from .exceptions import PrivateFileWorldReadableError
from .exceptions import UnknownClusterError
from .exceptions import UnknownDatabaseError


def connect(
    dbname: str,
    cluster: str = "web",
    **kwargs,
) -> pymysql.connections.Connection:
    """
    Get a database connection for the specified wiki.

    :param dbname: Database name
    :param cluster: Database cluster (*analytics* or *web*)
    :param `**kwargs`: For :meth:`pymysql.connect <pymysql.connections.Connection.__init__>`
    :return: :class:`pymysql.connections.Connection`
    :raise: :class:`toolforge.UnknownClusterError`: When **cluster** value is unknown
    """
    if cluster not in ["analytics", "web"]:
        raise UnknownClusterError('"cluster" must be one of: "analytics", "web"')

    domain = f"{cluster}.db.svc.wikimedia.cloud"

    if dbname.endswith("_p"):
        dbname = dbname[:-2]

    if dbname == "meta":
        host = f"s7.{domain}"
    else:
        host = f"{dbname}.{domain}"
    host = kwargs.pop("host", host)

    return _connect(
        database=dbname + "_p",
        host=host,
        **kwargs,
    )


def _connect(*args, **kwargs) -> pymysql.connections.Connection:  # pragma: no cover
    """Wraper for pymysql.connect to make testing easier."""
    kw = {
        "read_default_file": os.path.expanduser("~/replica.my.cnf"),
        "charset": "utf8mb4",
    }
    kw.update(kwargs)
    return pymysql.connect(*args, **kw)  # type: ignore


def toolsdb(dbname: str, **kwargs) -> pymysql.connections.Connection:
    """Connect to a database hosted on the ToolsDB service.

    :param dbname: Database name
    :param `**kwargs`: For :meth:`pymysql.connect <pymysql.connections.Connection.__init__>`
    :return: :class:`pymysql.connections.Connection`
    """
    return _connect(
        database=dbname,
        host="tools.db.svc.wikimedia.cloud",
        **kwargs,
    )


def dbname(domain: str) -> str:
    """
    Convert a domain/URL into its database name.

    :param domain: DNS domain or URL to wiki
    :return: Wikimedia database name (like *enwiki*)
    :raises: :class:`toolforge.UnknownDatabaseError`: When dbname mapping for domain is unknown
    """
    # First, lets normalize the name.
    if domain.startswith(("http://", "https://")):
        domain = domain.replace("http://", "", 1).replace("https://", "", 1)
    if "/" in domain:
        domain = domain.split("/", 1)[0]

    domain = "https://" + domain
    data = _fetch_sitematrix()["sitematrix"]
    for num in data:
        if num.isdigit():
            for site in data[num]["site"]:
                if site["url"] == domain:
                    return site["dbname"]
        elif num == "specials":
            for special in data[num]:
                if special["url"] == domain:
                    return special["dbname"]

    raise UnknownDatabaseError(f"Unable to find database name for {domain}")


@functools.lru_cache()
def _fetch_sitematrix():
    params = {"action": "sitematrix", "format": "json"}
    headers = {
        "User-agent": "https://wikitech.wikimedia.org/wiki/User:Legoktm/toolforge_library",
    }
    r = requests.get(
        "https://meta.wikimedia.org/w/api.php",
        params=params,
        headers=headers,
    )
    r.raise_for_status()
    return r.json()


def set_user_agent(
    tool: str,
    url: Optional[str] = None,
    email: Optional[str] = None,
) -> str:
    """
    Set the default `requests <https://requests.readthedocs.io/>`_ user-agent
    to a better one in accordance with `[[meta:User-Agent policy]]
    <https://meta.wikimedia.org/wiki/User-Agent_policy>`_.

    :param tool: Toolforge tool name
    :param url: Optional URL
    :param email: Optional email
    :return: New User-agent value
    """
    if url is None:
        url = f"https://{tool}.toolforge.org/"
    if email is None:
        email = f"tools.{tool}@toolforge.org"

    ua = f"{tool} ({url}; {email}) python-requests/{requests.__version__}"
    requests.utils.default_user_agent = lambda *args, **kwargs: ua  # noqa: U100
    return ua


def _assert_private_file(func, *args, **kwargs):
    try:
        f = args[0]
        fd = f.fileno()
    except AttributeError:
        pass
    except IndexError:
        pass
    except OSError:
        pass
    else:
        mode = os.stat(fd).st_mode
        if stat.S_IROTH & mode:
            raise PrivateFileWorldReadableError(f)
    return func(*args, **kwargs)


def assert_private_file(func):
    """Decorator to assert that a file is not world-readable."""
    decorated = decorator.decorate(func, _assert_private_file)
    decorated.__doc__ = (
        (decorated.__doc__ or "")
        + """
    If the given stream is a file, additionally
    assert that it is not world-readable.
    """
    )
    return decorated


try:
    import yaml
except ModuleNotFoundError:
    pass
else:
    load_private_yaml: Callable[[IO], Any] = assert_private_file(yaml.safe_load)
    load_private_yaml.__name__ = "load_private_yaml"
    load_private_yaml.__module__ = "toolforge"
