Contributing
============

You can contribute to the project in multiple ways:

* Write documentation
* Implement features
* Fix bugs
* Add unit and functional tests
* Everything else you can think of

Code of Conduct
---------------

The development of this software is covered by the `Code of Conduct for
Wikimedia technical spaces`_.

Bug reports
-----------

Please report bugs and feature requests at https://phabricator.wikimedia.org/tag/tool-python-toolforge/.

Development workflow
--------------------

Before contributing, install tox_ and pre-commit_:

.. code-block:: bash

  python3 -m pip install --user --upgrade 'tox>=4.0' pre-commit
  cd python-toolforge/
  pre-commit install -t pre-commit -t commit-msg --install-hooks

This will help automate adhering to code style guidelines described below.

If you don't like using ``pre-commit``, feel free to skip installing it, but
please **ensure all your commit messages and code pass all default tox
checks** outlined below before pushing your code.

When you're ready or if you'd like to get feedback, please provide your
patches as Merge Requests on gitlab.wikimedia.org_.

Coding Style
------------

We use black_ and isort_ to format our code, so you'll need to make sure you
use them when committing.

To format your code according to our guidelines before committing, run:

.. code-block:: bash

  cd python-toolforge/
  tox -e lint

Running unit tests
------------------

Before submitting a merge request make sure that the tests and lint checks
still succeed with your change. Unit tests and functional tests run in GitLab
CI and passing checks are mandatory to get merge requests accepted.

.. code-block:: bash

   # Run unit tests using all python3 versions available on your system, and
   # all lint checks:
   tox

   # Run lint and code formatting checks:
   tox -e lint

   # Run unit tests in one python environment only (useful for quick testing
   # during development):
   tox -e py311

   # List all available tox environments
   tox list

Releases
--------

A release is automatically published when a git tag is made in the
gitlab.wikimedia.org_ repo. See our `.gitlab-ci.yml`_ for details.

.. _Code of Conduct for Wikimedia technical spaces: https://www.mediawiki.org/wiki/Code_of_Conduct
.. _tox: https://tox.wiki/
.. _pre-commit: https://pre-commit.com
.. _gitlab.wikimedia.org: https://gitlab.wikimedia.org/toolforge-repos/python-toolforge
.. _black: https://github.com/python/black
.. _isort: https://pycqa.github.io/isort/
.. _.gitlab-ci.yml: https://gitlab.wikimedia.org/toolforge-repos/python-toolforge/-/blob/main/.gitlab-ci.yml
