6.1.0
----------
* Add assert_private_file() and, if PyYAML is installed, load_private_yaml()
* Add support for extension databases to connect()
* Get database credentials from toolforge envvars if available
* Add project documentation built with sphinx
* Publish project documentation at https://python-toolforge.readthedocs.io/
* Update generated User-Agent header to use toolforge.org email address.
* Update ToolsDB hostname to "tools.db.svc.wikimedia.cloud"
* Add custom exception types to replace ValueError

6.0.0
-----
* [BREAKING] Drop Python versions 3.4, 3.5, 3.6
* Add Python versions 3.10, 3.11
* Move hosting to https://gitlab.wikimedia.org/toolforge-repos/python-toolforge
* Convert build system from setuptools to hatchling
* Use black for code formatting
* Use isort for import formatting
* Add a number of flake8 plugins including bugbear and spellcheck
* Add CI support for publishing tagged versions to PyPi

5.0.0
-----
* Fix pymysql dependency on Python 3.5 (AntiCompositeNumber)

5.0.0b1
-------
* [BREAKING] Switch to use new multi-instance Wiki Replicas
* [BREAKING] Remove deprecated redirect_to_https

4.4.0
-----
* Allow calling set_user_agent multiple times
* Fix pymysql dependency on Python 3.4
* Test against Python 3.9

4.3.2
-----
* Update User-Agent for new toolforge.org domain

4.3.1
-----
* Provide PEP 561 type information
* Test against Python 3.8

4.3.0
-----
* Add type hints (Lucas Werkmeister)
* Raise ValueError in toolforge.dbname() if it's not found
* Make it easy to connect to tools.db.svc.eqiad.wmflabs (Bryan Davis)

4.2.0
-----
* Turn redirect_to_https into a no-op
* Have set_user_agent return the new value
* Drop Python 3.3 support

4.1.0
-----
* Add \*.{analytics,web}.db.svc.eqiad.wmflabs support (Bryan Davis)


4.0.0
-----
* Rename library to "toolforge"

3.2.0
-----
* Add redirect_to_https() helper for flask apps

3.1.0
-----
* Add a convenience function for monkey-patching requests' user-agent

3.0.0
-----
* Initial tagged release
