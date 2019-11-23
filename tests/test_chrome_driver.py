import os
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import tempfile


def test_chrome_manager_with_specific_version():
    with tempfile.TemporaryDirectory() as tmp:
        path = ChromeDriverManager("2.26", path=tmp).install()
        assert os.path.exists(path)


def test_chrome_manager_with_latest_version():
    with tempfile.TemporaryDirectory() as tmp:
        path = ChromeDriverManager(path=tmp).install()
        assert os.path.exists(path)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]
