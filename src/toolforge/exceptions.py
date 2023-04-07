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


class UnknownClusterError(ValueError):
    """Raised when an unknown "cluster" value is encountered."""

    # pass


class UnknownDatabaseError(ValueError):
    """Raised when a dbname cannot determined for a value."""

    # pass
