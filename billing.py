import os
import datetime
import requests
import json
import xml.etree.ElementTree as ET
from typing import Any, Dict
from requests_auth_aws_sigv4 import AWSSigV4  # type: ignore


def get_billing_in_dollars(now: datetime.datetime) -> float:
    auth = AWSSigV4('monitoring', region='us-east-1')
    params = {
        'Action': 'GetMetricStatistics',
        'Version': '2010-08-01',
        'Namespace': 'AWS/Billing',
        'MetricName': 'EstimatedCharges',
        'Dimensions.member.1.Name': 'Currency',
        'Dimensions.member.1.Value': 'USD',
        'StartTime': (now - datetime.timedelta(days=1)).strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'),
        'EndTime': now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'Period': '86400',
        'Statistics.member.1': 'Maximum'
    }
    response = requests.post(
        'https://monitoring.us-east-1.amazonaws.com',
        data=params,
        auth=auth
    )
    response.raise_for_status()

    root = ET.fromstring(response.text)

    ns = '{https://monitoring.amazonaws.com/doc/2010-08-01/}'
    for datapoint in root.findall(f'.//{ns}Datapoint'):
        maximum = datapoint.find(f'.//{ns}Maximum')
        if maximum is not None and maximum.text is not None:
            return float(maximum.text)
    raise ValueError("No billing data found")


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
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    now = datetime.datetime.now()
    billing = get_billing_in_dollars(now)
    payload = build_slack_payload(billing, now)
    requests.post(webhook_url, data=json.dumps(payload))
