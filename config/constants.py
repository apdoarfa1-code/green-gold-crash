from enum import Enum


class MultiplierCategory(str, Enum):
    LOW = "low"         # < 2.0x
    MEDIUM = "medium"   # 2.0x - 10.0x
    HIGH = "high"       # >= 10.0x


class CollectionSource(str, Enum):
    PLAYWRIGHT_WS = "playwright_ws"
    PLAYWRIGHT_HTTP = "playwright_http"
    SIMULATED = "simulated"
    EXTERNAL_API = "external_api"


DEFAULT_LOW_THRESHOLD = 2.00
DEFAULT_MEDIUM_THRESHOLD = 10.00
SEQUENCE_LENGTH = 50
MAX_RECENT_ROUNDS = 100
