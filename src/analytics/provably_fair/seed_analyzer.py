from typing import List, Dict, Any
from src.analytics.provably_fair.hmac_verifier import HMACVerifier


class SeedAnalyzer:
    """Batch audits seed consistency and round cryptographic fairness."""

    @staticmethod
    def audit_rounds(rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid_count = 0
        total_checked = 0

        for r in rounds:
            server_seed = r.get("server_seed")
            client_seed = r.get("client_seed")
            multiplier = r.get("multiplier")
            nonce = r.get("nonce", 1)

            if server_seed and client_seed and multiplier is not None:
                total_checked += 1
                if HMACVerifier.verify(server_seed, client_seed, nonce, multiplier):
                    valid_count += 1

        integrity_rate = (valid_count / total_checked * 100.0) if total_checked > 0 else 100.0
        return {
            "total_checked": total_checked,
            "valid_count": valid_count,
            "integrity_rate_percent": round(integrity_rate, 2)
        }
