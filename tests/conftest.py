from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def activities_state(monkeypatch):
    state = deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", state)
    return state


@pytest.fixture
def client(activities_state):
    with TestClient(app_module.app) as test_client:
        yield test_client
