import pytest

from pydisadm.configuration import Configuration

@pytest.fixture
def mock_env_alliance_id(monkeypatch):
    monkeypatch.setenv('ALLIANCE_ID', '99999')

@pytest.fixture
def mock_env_discord_app_id(monkeypatch):
    monkeypatch.setenv('DISCORD_APP_ID', 'ABC')

@pytest.fixture
def mock_env_discord_token(monkeypatch):
    monkeypatch.setenv('DISCORD_TOKEN', 'DEF')

@pytest.fixture
def mock_env_discord_channel(monkeypatch):
    monkeypatch.setenv('DISCORD_CHANNEL', 'GHJ')

@pytest.fixture
def mock_env_alliance_id_invalid(monkeypatch):
    monkeypatch.setenv('ALLIANCE_ID', 'NaN')

def test_empty_configuration():
    """Test creating configuration without any environment."""

    sut = Configuration()

    assert sut.alliance['id'] is None, "alliance_id is expected to be None"
    assert sut.discord['app_id'] is None, "discord_app_id is expected to be None"
    assert sut.discord['channel'] is None, "discord_channel is expected to be None"
    assert sut.discord['token'] is None, "discord_token is expected to be None"

def test_alliance_id_number(mock_env_alliance_id):
    """Test assigning number to alliance_id"""

    sut = Configuration()

    assert sut.alliance['id'] == 99999, "alliance_id is not matching expected value"


def test_discord_app_id(mock_env_discord_app_id):
    """Test assigning value to discord_app_id"""

    sut = Configuration()

    assert sut.discord['app_id'] == 'ABC', "discord_app_id is not matching expected value"


def test_discord_token(mock_env_discord_token):
    """Test assigning value to discord_token"""

    sut = Configuration()

    assert sut.discord['token'] == 'DEF', "discord_token is not matching expected value"


def test_discord_channel(mock_env_discord_channel):
    """Test assigning value to discord_channel"""

    sut = Configuration()

    assert sut.discord['channel'] == 'GHJ', "discord_channel is not matching expected value"


def test_alliance_id_number_invalid(mock_env_alliance_id_invalid):
    """Test assigning invalid number to alliance_id"""

    with pytest.raises(ValueError):
        Configuration()
    