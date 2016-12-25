from slackclient import SlackClient
import boto3
import os
import datetime

now = datetime.datetime.now()
slack_token = os.environ["SLACK_API_TOKEN"]
channel_to_post = os.environ["SLACK_CHANNEL_TO_POST"]
sc = SlackClient(slack_token)

def handler(event, context):
    b = get_billing_in_dollars()
    ret = sc.api_call(
        "chat.postMessage",
        channel=channel_to_post,
        text="Billing in this month: {} USD".format(b),
        username="aws",
        icon_emoji=":aws:"
    )
    print(ret)
    return {'text': ret}

def get_billing_in_dollars():
    cloud_watch = boto3.client('cloudwatch', region_name='us-east-1')
    metric = cloud_watch.get_metric_statistics(
        Namespace="AWS/Billing",
        Dimensions=[{
            "Name":"Currency",
            "Value":"USD",
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
