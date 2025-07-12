import os
import datetime
from services.billing_service import BillingService
from services.notification_service import NotificationService


if __name__ == '__main__':
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    now = datetime.datetime.now()
    
    billing_service = BillingService()
    notification_service = NotificationService(webhook_url)
    
    billing = billing_service.get_current_billing(now)
    notification_service.send_notification(billing, now)