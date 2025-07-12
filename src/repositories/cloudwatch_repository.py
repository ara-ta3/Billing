import boto3
import datetime
from mypy_boto3_cloudwatch import Client as CloudWatchClient


class CloudWatchRepository:
    def __init__(self) -> None:
        self._client = boto3.client('cloudwatch', region_name='us-east-1')

    def get_billing_in_dollars(self, now: datetime.datetime) -> float:
        metric = self._client.get_metric_statistics(
            Namespace="AWS/Billing",
            Dimensions=[{
                "Name": "Currency",
                "Value": "USD",
            }],
            MetricName="EstimatedCharges",
            StartTime=now - datetime.timedelta(days=1),
            EndTime=now,
            Period=86400,
            Statistics=["Maximum"]
        )
        return metric["Datapoints"][0]["Maximum"]
