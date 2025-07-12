import os
import datetime
from repositories.cloudwatch_repository import CloudWatchRepository
from services.billing_service import BillingService
from services.notification_service import NotificationService
from billing_application import BillingApplication


if __name__ == '__main__':
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    now = datetime.datetime.now()

    cloudwatch_repository = CloudWatchRepository()
    billing_service = BillingService(cloudwatch_repository)
    notification_service = NotificationService(webhook_url)
    app = BillingApplication(billing_service, notification_service)

    app.run(now)
