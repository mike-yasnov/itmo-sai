from dataclasses import dataclass
from typing import Set, Optional


@dataclass
class UserPreferences:
    genres: Set[str]
    mechanics: Set[str]
    complexity: Optional[str]
    cooperative: Optional[bool]

