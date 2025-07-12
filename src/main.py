import os
import datetime
from services.billing_service import BillingService
from services.notification_service import NotificationService
from billing_application import BillingApplication


if __name__ == '__main__':
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    now = datetime.datetime.now()

    billing_service = BillingService()
    notification_service = NotificationService(webhook_url)
    app = BillingApplication(billing_service, notification_service)

    app.run(now)
