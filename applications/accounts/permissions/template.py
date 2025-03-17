from typing import List, Literal
from dataclasses import dataclass, asdict, field

from .enums import ActionToMethod


class PermissionEffect:
    Allow: str = "Allow"
    Deny: str = "Deny"


@dataclass
class PermissionStatement:
    Resource: str
    Actions: list
    Effect: Literal["Allow", "Deny"]
    Sid: str = None
    Methods: list = field(default_factory=lambda: [])
    Condition: list = field(default_factory=lambda: [])

    def __post_init__(self):
        if self.Actions:
            for x in self.Actions:
                self.Methods.append(getattr(ActionToMethod, x))

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


@dataclass
class PermissionTemplate:
    Statement: List[PermissionStatement]
    Version: str = "2024-12-01"

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}
