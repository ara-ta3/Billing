import datetime
from billing.protocols import CloudWatchRepositoryProtocol
from billing.repositories.cloudwatch_repository import CloudWatchRepository


class BillingService:
    def __init__(self, repository: CloudWatchRepositoryProtocol) -> None:
        self._repository = repository

    def get_current_billing(self, now: datetime.datetime) -> float:
        return self._repository.get_billing_in_dollars(now)
