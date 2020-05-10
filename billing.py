import boto3
import os
import datetime
import requests
import json
from boto3_type_annotations.cloudwatch import Client

now = datetime.datetime.now()
webhook_url = os.environ["SLACK_WEBHOOK_URL"]


def handler(event, context):
    b = get_billing_in_dollars()
    ret = requests.post(webhook_url, data=json.dumps({
        "text": "Billing in this month: {} USD".format(b)
    }))
    return {'text': ret}


def get_cloudwatch_client() -> Client:
    return boto3.client('cloudwatch', region_name='us-east-1')


def get_billing_in_dollars() -> int:
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
