
from dataclasses import dataclass


class PurelymailAPIError(Exception):
    """Custom Exception raised when API request is unsuccessful."""
    pass


@dataclass
class RoutingRule:
    """Represent a routing rule."""
    id: int
    domainName: str
    prefix: bool
    matchUser: str
    targetAddresses: list[str]
    catchall: bool


@dataclass
class User:
    userName: str
    domainName: str
    password: str
    enablePasswordReset: bool
    recoveryEmail: str
    recoveryEmailDescription: str
    recoveryPhone: str
    recoveryPhoneDescription: str
    enableSearchIndexing: bool
    sendWelcomeEmail: bool
