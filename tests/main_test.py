#!/usr/bin/env python
import io
import json

import pytest
import requests

import toolforge


class TestMain:
    def test_callable(self):
        assert callable(toolforge.connect)
        assert callable(toolforge.dbname)

    @pytest.mark.parametrize(
        ("domain", "dbname"),
        [
            ("en.wikipedia.org", "enwiki"),
            ("https://en.wikipedia.org", "enwiki"),
            ("www.wikidata.org", "wikidatawiki"),
            ("http://commons.wikimedia.org", "commonswiki"),
            ("en.wikisource.org/wiki/Article", "enwikisource"),
            ("https://wikimania2018.wikimedia.org", "wikimania2018wiki"),
        ],
    )
    def test_dbname(self, domain, dbname):
        assert toolforge.dbname(domain) == dbname

    def test_dbname_throws_for_unknown(self):
        with pytest.raises(toolforge.UnknownDatabaseError):
            toolforge.dbname("toolforge.org")

    @pytest.mark.parametrize(
        ("tool", "url", "email", "expect"),
        [
            (
                "mycooltool",
                None,
                None,
                "mycooltool (https://mycooltool.toolforge.org/; tools.mycooltool@toolforge.org)",
            ),
            ("test", "test", "test", "test (test; test)"),
        ],
    )
    def test_set_user_agent(self, tool, url, email, expect):
        expected = f"{expect} python-requests/{requests.__version__}"
        ua = toolforge.set_user_agent(tool, url, email)
        assert ua == expected
        # Allow calling set_user_agent twice (see #14)
        ua2 = toolforge.set_user_agent(tool, url, email)
        assert ua2 == expected
        assert requests.get("https://httpbin.io/user-agent").json() == {
            "user-agent": expected,
        }

    @pytest.mark.parametrize(
        ("args", "expects"),
        [
            (
                ["enwiki_p"],
                {
                    "database": "enwiki_p",
                    "host": "enwiki.web.db.svc.wikimedia.cloud",
                },
            ),
            (
                ["enwiki"],
                {
                    "database": "enwiki_p",
                    "host": "enwiki.web.db.svc.wikimedia.cloud",
                },
            ),
            (
                ["enwiki", "analytics"],
                {
                    "database": "enwiki_p",
                    "host": "enwiki.analytics.db.svc.wikimedia.cloud",
                },
            ),
            (
                ["meta", "analytics"],
                {
                    "database": "meta_p",
                    "host": "s7.analytics.db.svc.wikimedia.cloud",
                },
            ),
        ],
    )
    def test_connect(self, mocker, args, expects):
        self._assert_connect(mocker, toolforge.connect, args, expects)

    def _assert_connect(self, mocker, func, args, expect):
        """Mock toolforge._connect and assert it is called as expected.

        :param func: Function to call after mocking toolforge._connect
        :param args: Arguments for calling func
        :param expect: Dict of expected arguments to toolforge._connect
        """
        mm = mocker.patch("toolforge._connect")
        mm.return_value = None
        conn = func(*args)
        assert conn is None
        mm.assert_called_once_with(**expect)

    def test_connect_rejects_unknown_cluster(self, mocker):
        with pytest.raises(toolforge.UnknownClusterError):
            self._assert_connect(
                mocker,
                toolforge.connect,
                ["ignored", "not web or analytics"],
                {"ignored": "ignored"},
            )

    @pytest.mark.parametrize(
        ("args", "expects"),
        [
            (
                ["s12345__foo"],
                {
                    "database": "s12345__foo",
                    "host": "tools.db.svc.wikimedia.cloud",
                },
            ),
            (
                ["s12345__foo_p"],
                {
                    "database": "s12345__foo_p",
                    "host": "tools.db.svc.wikimedia.cloud",
                },
            ),
        ],
    )
    def test_toolsdb(self, mocker, args, expects):
        self._assert_connect(mocker, toolforge.toolsdb, args, expects)

    def test_assert_private_file_no_args(self, mocker):
        load = mocker.Mock(
            return_value="data",
            # these attributes (used by decorator) are not mocked automatically
            __name__="name",
            __qualname__="qualname",
        )
        data = toolforge.assert_private_file(load)()
        assert data == "data"
        load.assert_called_once_with()

    def test_assert_private_file_non_io(self, mocker):
        stream = mocker.Mock(spec=[])  # empty spec = no fileno
        load = mocker.Mock(
            return_value="data",
            __name__="name",
            __qualname__="qualname",
        )
        data = toolforge.assert_private_file(load)(stream)
        assert data == "data"
        load.assert_called_once_with(stream)

    def test_assert_private_file_non_file(self):
        stream = io.StringIO('{"a": "b"}')
        data = toolforge.assert_private_file(json.load)(stream)
        assert data == {"a": "b"}

    @pytest.mark.parametrize("mode", [0o600, 0o640])
    def test_assert_private_file_non_world_readable(self, tmp_path, mode):
        tmp_file_path = tmp_path / "config.json"
        tmp_file_path.write_text('{"a": "b"}')
        tmp_file_path.chmod(mode)
        with tmp_file_path.open() as tmp_file:
            data = toolforge.assert_private_file(json.load)(tmp_file)
        assert data == {"a": "b"}

    def test_assert_private_file_world_readable(self, tmp_path):
        tmp_file_path = tmp_path / "config.json"
        tmp_file_path.write_text('{"a": "b"}')
        tmp_file_path.chmod(0o644)
        with tmp_file_path.open() as tmp_file:
            with pytest.raises(toolforge.exceptions.PrivateFileWorldReadableError):
                toolforge.assert_private_file(json.load)(tmp_file)

    @pytest.mark.parametrize("mode", [0o600, 0o640])
    def test_load_private_yaml_non_world_readable(self, tmp_path, mode):
        tmp_file_path = tmp_path / "config.yaml"
        tmp_file_path.write_text('{"a": "b"}')
        tmp_file_path.chmod(mode)
        with tmp_file_path.open() as tmp_file:
            data = toolforge.load_private_yaml(tmp_file)
        assert data == {"a": "b"}

    def test_load_private_yaml_world_readable(self, tmp_path):
        tmp_file_path = tmp_path / "config.yaml"
        tmp_file_path.write_text('{"a": "b"}')
        tmp_file_path.chmod(0o644)
        with tmp_file_path.open() as tmp_file:
            with pytest.raises(toolforge.exceptions.PrivateFileWorldReadableError):
                toolforge.load_private_yaml(tmp_file)
