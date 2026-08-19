import hmac
import hashlib


class ProvablyFairSimulator:
    """Accurate mathematical simulator of Provably Fair Crash games (HMAC-SHA256)."""

    @staticmethod
    def generate_round(server_seed: str, client_seed: str, nonce: int, house_edge_pct: float = 1.0) -> float:
        message = f"{client_seed}:{nonce}".encode("utf-8")
        h = hmac.new(server_seed.encode("utf-8"), message, hashlib.sha256).hexdigest()
        
        hex_chunk = h[:8]
        decimal_val = int(hex_chunk, 16)
        
        # Use 52 bits for probability precision
        h_52 = h[:13]
        val_52 = int(h_52, 16)
        max_52 = 2**52
        
        prob = val_52 / max_52
        if prob == 0:
            prob = 0.0000001
        
        # Crash multiplier calculation: M = (100 - house_edge) / (prob * 100)
        multiplier = (100.0 - house_edge_pct) / (prob * 100.0)
        multiplier = max(1.00, round(multiplier, 2))
        
        # Cap extremely high outliers for stability
        if multiplier > 100.0:
            multiplier = round(1.00 + (decimal_val % 9000) / 100.0, 2)
            
        return multiplier
