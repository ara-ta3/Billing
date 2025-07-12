import datetime
from protocols import CloudWatchRepositoryProtocol
from repositories.cloudwatch_repository import CloudWatchRepository


class BillingService:
    def __init__(
        self, repository: CloudWatchRepositoryProtocol | None = None
    ) -> None:
        self._repository = repository or CloudWatchRepository()

    def get_current_billing(self, now: datetime.datetime) -> float:
        return self._repository.get_billing_in_dollars(now)
