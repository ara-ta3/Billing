import boto3
import os
import datetime
import requests
import json
from mypy_boto3 import cloudwatch


def handler(event, context):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    now = datetime.datetime.now()
    b = get_billing_in_dollars(now)
    ret = requests.post(webhook_url, data=json.dumps({
        "text": "Billing in this month: {} USD".format(b)
    }))
    return {'text': ret}


def get_cloudwatch_client() -> cloudwatch.CloudWatchClient:
    return boto3.client('cloudwatch', region_name='us-east-1')


def get_billing_in_dollars(now: datetime.datetime) -> float:
    cloud_watch = get_cloudwatch_client()
    metric = cloud_watch.get_metric_statistics(
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


if __name__ == '__main__':
    handler({}, {})
