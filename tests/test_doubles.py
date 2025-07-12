import datetime
from typing import Any, Dict, List


class FakeCloudWatchRepository:
    def __init__(self, billing_amount: float = 10.50) -> None:
        self._billing_amount = billing_amount

    def get_billing_in_dollars(self, now: datetime.datetime) -> float:
        return self._billing_amount


class FakeBillingService:
    def __init__(self, billing_amount: float = 15.75) -> None:
        self._billing_amount = billing_amount

    def get_current_billing(self, now: datetime.datetime) -> float:
        return self._billing_amount


class SpyNotificationService:
    def __init__(self, webhook_url: str = "http://test.example.com") -> None:
        self._webhook_url = webhook_url
        self.sent_notifications: List[Dict[str, Any]] = []

    def build_slack_payload(self, billing: float, now: datetime.datetime) -> Dict[str, Any]:
        return {
            "username": "AWS Billing",
            "icon_emoji": ":money_with_wings:",
            "attachments": [
                {
                    "color": "#2eb886",
                    "title": "AWS Billing Update",
                    "fields": [
                        {
                            "title": "Date",
                            "value": now.strftime("%Y-%m-%d"),
                            "short": True
                        },
                        {
                            "title": "Month to date",
                            "value": f"{billing:.2f} USD",
                            "short": True
                        }
                    ]
                }
            ]
        }

    def send_notification(self, billing: float, now: datetime.datetime) -> None:
        self.sent_notifications.append({
            "billing": billing,
            "now": now,
            "payload": self.build_slack_payload(billing, now)
        })