import datetime
from repositories.cloudwatch_repository import CloudWatchRepository


class BillingService:
    def __init__(self) -> None:
        self._repository = CloudWatchRepository()

    def get_current_billing(self, now: datetime.datetime) -> float:
        return self._repository.get_billing_in_dollars(now)