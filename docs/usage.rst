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

Set proper user-agent
---------------------

Set the default Requests_ user-agent to one that complies with the `Wikimedia
User-Agent policy`_:

.. code-block:: python

   import requests
   import toolforge

   toolforge.set_user_agent("mycooltool")
   # Sets user-agent to:
   # mycooltool (https://mycooltool.toolforge.org/; tools.mycooltool@toolforge.org) python-requests/2.28.2
   requests.get("...")


For cases where the default Requests user-agent is not used, the function also
returns the string to use instead:

.. code-block:: python

   import mwapi
   import toolforge

   user_agent = toolforge.set_user_agent("mycooltool")
   session = mwapi.Session("https://meta.wikimedia.org", user_agent=user_agent)
   session.get(action="...")


.. _gitlab.wikimedia.org: https://gitlab.wikimedia.org/toolforge-repos/python-toolforge
.. _Wiki Replicas: https://wikitech.wikimedia.org/wiki/Wiki_Replicas
.. _connection handling policy: https://wikitech.wikimedia.org/wiki/Help:Toolforge/Database#Connection_handling_policy
.. _Requests: https://requests.readthedocs.io/
.. _Wikimedia User-Agent policy: https://meta.wikimedia.org/wiki/User-Agent_policy
