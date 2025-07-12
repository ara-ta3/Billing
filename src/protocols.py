import datetime
from typing import Protocol


class CloudWatchRepositoryProtocol(Protocol):
    def get_billing_in_dollars(self, now: datetime.datetime) -> float:
        ...


class BillingServiceProtocol(Protocol):
    def get_current_billing(self, now: datetime.datetime) -> float:
        ...


class NotificationServiceProtocol(Protocol):
    def send_notification(
        self, billing: float, now: datetime.datetime
    ) -> None:
        ...
