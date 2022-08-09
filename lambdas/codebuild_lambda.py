import os
import time
import csv
import json
import boto3
from datetime import datetime

client = boto3.client('codebuild')

def handler(event, context):
    # Log trigger event and environment
    print(event)
    print(os.environ)

    project_name=event["project_name"]
    city=event["city"]

    response = client.start_build(
        projectName=project_name,
        environmentVariablesOverride=[
        {
            "name": "CITY",
            "value": city,
            "type": "PLAINTEXT"
        }
        ]
    )

    id=response['build']['id']

    is_running = True

    while is_running:
        response = client.batch_get_builds(
            ids=[
                id
            ]
        )

        build_status=response['builds'][0]['buildStatus']
        print(build_status)
        if build_status == 'IN_PROGRESS':
            time.sleep(5)
        elif build_status == 'SUCCEEDED':
            return project_name + " for "+ city + " succeeded."
        else:
            raise
