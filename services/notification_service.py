import datetime
import json
import requests
from typing import Any, Dict


class NotificationService:
    def __init__(self, webhook_url: str) -> None:
        self._webhook_url = webhook_url

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
        payload = self.build_slack_payload(billing, now)
        requests.post(self._webhook_url, data=json.dumps(payload))