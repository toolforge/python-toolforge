# This file is part of Toolforge python helper library
# Copyright (C) 2023 Kunal Mehta <legoktm@debian.org> and contributors
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
Typed exceptions
"""
from __future__ import annotations  # PEP 563

from typing import Any
from typing import IO


class UnknownClusterError(ValueError):
    """Raised when an unknown "cluster" value is encountered."""

    # pass


class UnknownDatabaseError(ValueError):
    """Raised when a dbname cannot determined for a value."""

    # pass


class PrivateFileWorldReadableError(ValueError):
    """
    Raised when a function decorated with :func:`toolforge.assert_private_file`
    encounters a world-readable file.
    """

    def __init__(self, f: IO[Any]) -> None:
        super().__init__(
            f"{getattr(f, 'name', 'config file')} should be private, "
            "but is currently world-readable!",
        )
