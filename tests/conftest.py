import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import Store, get_store


@pytest.fixture
def store() -> Store:
    return Store()


@pytest.fixture
def client(store: Store):
    app.dependency_overrides[get_store] = lambda: store
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def make_txn(**overrides) -> dict:
    txn = {
        "reference": "TXN-TEST",
        "amount": 120.50,
        "currency": "EUR",
        "originator_name": "Bob Sample",
        "originator_country": "DE",
        "beneficiary_name": "Alice Demo",
        "beneficiary_country": "FR",
    }
    return txn | overrides


@pytest.fixture
def screening_list_entry(client: TestClient) -> str:
    name = "Ivan Placeholderov"
    assert client.post("/watchlist", json={"name": name}).status_code == 201
    return name


@pytest.fixture
def screening_hit(screening_list_entry: str) -> dict:
    return make_txn(originator_name=screening_list_entry)


@pytest.fixture
def screening_partial(screening_list_entry: str) -> dict:
    return make_txn(originator_name="Ivan Placehold")


@pytest.fixture
def screening_clean() -> dict:
    return make_txn(originator_name="Cedar Example")


@pytest.fixture
def alert_id(client: TestClient) -> str:
    """An open alert raised by a watchlist hit in a high-risk country."""
    response = client.post(
        "/transactions/screen",
        json=make_txn(beneficiary_name="Globex Front LLC", beneficiary_country="XQ"),
    )
    return response.json()["alert_id"]
