import pytest
from src.analytics.provably_fair.hmac_verifier import HMACVerifier
from src.data_processing.cleaner import DataCleaner
from src.core.exceptions import CleaningError


def test_hmac_verifier_calculation():
    multiplier = HMACVerifier.generate_multiplier("test_server_seed", "test_client_seed", 1)
    assert isinstance(multiplier, float)
    assert multiplier >= 1.00


def test_hmac_verifier_verification():
    server_seed = "server123"
    client_seed = "client456"
    nonce = 1
    mult = HMACVerifier.generate_multiplier(server_seed, client_seed, nonce)
    assert HMACVerifier.verify(server_seed, client_seed, nonce, mult) is True


def test_data_cleaner_valid():
    raw = {"round_id": "r_123", "multiplier": "2.45", "source": "test"}
    cleaned = DataCleaner.clean(raw)
    assert cleaned["round_id"] == "r_123"
    assert cleaned["multiplier"] == 2.45


def test_data_cleaner_invalid_raises():
    with pytest.raises(CleaningError):
        DataCleaner.clean({"multiplier": 1.5})  # Missing round_id
