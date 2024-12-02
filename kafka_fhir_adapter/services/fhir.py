import datetime
import json
from typing import Optional
from faust.app import App
from fhir.resources.R4B.operationoutcome import OperationOutcome


async def send_validate_payload(app: App, message: str, url: str):
    response_promisse = await app.http_client.post(url, json=message)
    response = await response_promisse.json()
    operation_outcome = OperationOutcome(**response)
    for issue in operation_outcome.issue:
        print(issue)
    return True

async def send_payload(app: App, message: str, url: str):
    response = await app.http_client.post(url, json=message)
    return await response.json()

def epoch_timestamp_to_iso_string(value: Optional[int]):
    return datetime.datetime.fromtimestamp(value / 1000).isoformat() + 'Z'

def string_to_bool(value: str):
    if value.lower() == 'true':
        return True
    else:
        return False