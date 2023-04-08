from toolforge.exceptions import PrivateFileWorldReadableError


class TestExceptions:
    def test_PrivateFileWorldReadableError_named(self, mocker):  # noqa: N802
        f = mocker.Mock()
        f.name = "config.yaml"

        e = PrivateFileWorldReadableError(f)

        assert (
            e.args[0]
            == "config.yaml should be private, but is currently world-readable!"
        )

    def test_PrivateFileWorldReadableError_unnamed(self):  # noqa: N802
        f = None

        e = PrivateFileWorldReadableError(f)

        assert (
            e.args[0]
            == "config file should be private, but is currently world-readable!"
        )
