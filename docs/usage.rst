:gitlab_url: https://gitlab.wikimedia.org/toolforge-repos/python-toolforge/-/blob/main/docs/usage.rst

Usage
=====

Installation
------------

Use ``pip`` to install the latest stable version of ``toolforge``:

.. code-block:: bash

    python3 -m pip install --upgrade toolforge

The current development version is available on gitlab.wikimedia.org_, and can
be installed directly from the git repository:

.. code-block:: bash

    python3 -m pip install --upgrade git+https://gitlab.wikimedia.org/toolforge-repos/python-toolforge.git

Connect to databases
--------------------

The :meth:`toolforge.connect` method simplifies connecting to a `Wiki
Replicas`_ database. It will automatically read your tool's database
credentials from ``$HOME/replica.my.cnf`` and determine the correct host to
connect to based on the provided database name.

.. code-block:: python

   import toolforge

   conn = toolforge.connect("enwiki")  # You can also use "enwiki_p"
   # conn is a pymysql.connection object.
   with conn.cursor() as cur:
       cur.execute(query)  # Or something....

The :meth:`toolforge.toolsdb` method provides similar functionality for
databases hosted on *tools.db.svc.wikimedia.cloud*.

Please keep the `connection handling policy`_ in mind -- web tools should
create connections per request, not during application initialization.

Set policy compliant User-Agent
-------------------------------

Set the default Requests_ user-agent to one that complies with the `Wikimedia
User-Agent policy`_:

.. code-block:: python

   import requests
   import toolforge

   toolforge.set_user_agent("mycooltool")
   # Sets user-agent to:
   # mycooltool (https://mycooltool.toolforge.org/; tools.mycooltool@toolforge.org) python-requests/2.28.2
   requests.get("...")

For cases where the default Requests User-Agent is not used, the function also
returns the string to use:

.. code-block:: python

   import mwapi
   import toolforge

   user_agent = toolforge.set_user_agent("mycooltool")
   session = mwapi.Session("https://meta.wikimedia.org", user_agent=user_agent)
   session.get(action="...")

.. warning::
    :py:meth:`~toolforge.set_user_agent`'s automatic application works by
    `monkey patching <https://en.wikipedia.org/wiki/Monkey_patch>`_ the
    :py:mod:`requests` module. Any :py:class:`requests.Session` object created
    before :meth:`~toolforge.set_user_agent` was called will ***not***
    automatically inherit the new User-Agent value.

    Workarounds for this behavior include:

    - Calling :py:meth:`~toolforge.set_user_agent` before importing an
      affected library.

      .. code-block:: python

          import toolforge

          toolforge.set_user_agent("...")
          import module_that_creates_session

    - Explicitly setting the :py:class:`requests.Session`'s *User-Agent*
      header to the return value of your
      :py:meth:`requests.utils.default_user_agent` call.

      .. code-block:: python

          user_agent = toolforge.set_user_agent("...")
          existing_session.headers["User-Agent"] = user_agent

Loading configuration files
---------------------------

To load configuration files with potentially sensitive information
(e.g. OAuth credentials), you can use the :meth:`toolforge.assert_private_file`
decorator to wrap any other "load"-like function,
for example from the standard library ``json`` module:

.. code-block:: python

   import json
   import toolforge

   with open("config.json", "r") as f:
       config = toolforge.assert_private_file(json.load)(f)

This will ensure that the config file is not world-readable,
and raise a :class:`toolforge.exceptions.PrivateFileWorldReadableError` if it is.
In that case, you should recreate the config file and replace all secrets in it.

.. code-block:: shell

   mv config.yaml config.yaml.leaked
   install -m600 /dev/null config.yaml
   # edit config.yaml

If you use a YAML configuration file and install the PyYAML_ library,
you can also use the :meth:`toolforge.load_private_yaml` function directly:

.. code-block:: python

   import toolforge

   with open("config.yaml", "r") as f:
       config = toolforge.load_private_yaml(f)

Note that PyYAML is not a dependency of the ``toolforge`` library,
and the function will only be available if PyYAML is otherwise installed.
You should add it to your ``pyproject.toml``, ``requirements.txt`` or other dependency list if you want to use it.

In a Flask_ tool, you can load the configuration like this:

.. code-block:: python

   app.config.from_file("config.yaml", load=toolforge.load_private_yaml)

.. _gitlab.wikimedia.org: https://gitlab.wikimedia.org/toolforge-repos/python-toolforge
.. _Wiki Replicas: https://wikitech.wikimedia.org/wiki/Wiki_Replicas
.. _connection handling policy: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Database#Connection_handling_policy
.. _Requests: https://requests.readthedocs.io/
.. _Wikimedia User-Agent policy: https://meta.wikimedia.org/wiki/User-Agent_policy
.. _PyYAML: https://pyyaml.org/
.. _Flask: https://flask.palletsprojects.com/
