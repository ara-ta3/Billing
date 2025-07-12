import datetime
from protocols import BillingServiceProtocol, NotificationServiceProtocol


class BillingApplication:
    def __init__(
        self,
        billing_service: BillingServiceProtocol,
        notification_service: NotificationServiceProtocol
    ) -> None:
        self._billing_service = billing_service
        self._notification_service = notification_service

    def run(self, now: datetime.datetime) -> None:
        billing = self._billing_service.get_current_billing(now)
        self._notification_service.send_notification(billing, now)
