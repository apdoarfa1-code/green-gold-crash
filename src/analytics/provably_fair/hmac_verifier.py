import hmac
import hashlib


class HMACVerifier:
    """Implements Provably Fair cryptographic verification using HMAC-SHA256."""

    @staticmethod
    def generate_multiplier(server_seed: str, client_seed: str, nonce: int) -> float:
        message = f"{client_seed}:{nonce}".encode("utf-8")
        h = hmac.new(server_seed.encode("utf-8"), message, hashlib.sha256).hexdigest()
        
        # Take first 4 bytes (8 hex characters)
        hex_chunk = h[:8]
        decimal_value = int(hex_chunk, 16)
        
        # 1% house edge consideration or standard formula
        # Standard Crash formula: 100 / (decimal_value % 100 + 1) or modulo scaling
        multiplier = max(1.00, (decimal_value % 10000) / 100.0)
        return round(multiplier, 2)

    @staticmethod
    def verify(server_seed: str, client_seed: str, nonce: int, expected_multiplier: float) -> bool:
        computed = HMACVerifier.generate_multiplier(server_seed, client_seed, nonce)
        return abs(computed - expected_multiplier) < 0.01
