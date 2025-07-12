import datetime
from billing.services.billing_service import BillingService
from billing.billing_application import BillingApplication
from .test_doubles import FakeCloudWatchRepository, SpyNotificationService


def test_billing_application_run():
    # Arrange
    fake_repository = FakeCloudWatchRepository(billing_amount=25.75)
    billing_service = BillingService(fake_repository)
    notification_service = SpyNotificationService()
    app = BillingApplication(billing_service, notification_service)
    test_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
    
    # Act
    app.run(test_time)
    
    # Assert
    assert len(notification_service.sent_notifications) == 1
    notification = notification_service.sent_notifications[0]
    assert notification["billing"] == 25.75
    assert notification["now"] == test_time
    assert notification["payload"]["attachments"][0]["fields"][1]["value"] == "25.75 USD"


def test_billing_application_with_different_amount():
    # Arrange
    fake_repository = FakeCloudWatchRepository(billing_amount=100.00)
    billing_service = BillingService(fake_repository)
    notification_service = SpyNotificationService()
    app = BillingApplication(billing_service, notification_service)
    test_time = datetime.datetime(2024, 2, 1, 9, 0, 0)
    
    # Act
    app.run(test_time)
    
    # Assert
    assert len(notification_service.sent_notifications) == 1
    notification = notification_service.sent_notifications[0]
    assert notification["billing"] == 100.00
    assert notification["now"] == test_time


