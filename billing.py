import boto3
import os
import datetime
import requests
import json
from typing import Any, Dict
from mypy_boto3_cloudwatch import Client as CloudWatchClient


def handler(event, context):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    now = datetime.datetime.now()
    billing = get_billing_in_dollars(now)
    payload = build_slack_payload(billing, now)
    requests.post(webhook_url, data=json.dumps(payload))
    return {"message": billing}


def get_cloudwatch_client() -> CloudWatchClient:
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


def build_slack_payload(
    billing: float, now: datetime.datetime
) -> Dict[str, Any]:
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


if __name__ == '__main__':
    handler({}, {})
