class GreenGoldError(Exception):
    """Base exception for Green Gold Crash Engine."""
    pass


class IngestionError(GreenGoldError):
    """Raised when data ingestion fails."""
    pass


class StorageError(GreenGoldError):
    """Raised when database or cache operation fails."""
    pass


class ModelError(GreenGoldError):
    """Raised when ML model training or prediction fails."""
    pass


class VerificationError(GreenGoldError):
    """Raised when Provably Fair HMAC verification fails."""
    pass


class CleaningError(GreenGoldError):
    """Raised when raw data fails data cleaning/validation."""
    pass
