#!/usr/bin/env python

import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone


def get_mock_data(file_path: str):
    with open(file_path, "r") as file:
        return json.loads(file.read())


def write_to_gateway(datapoints, middleware_address):
    try:
        response = requests.post(
            url=f"{middleware_address}/update_observations",
            data=json.dumps(datapoints),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
    except Exception as e:
        print(e)
        exit(1)

def replace_timestamps(grouped_datapoints):
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    for datapoints in grouped_datapoints:
        for datapoint in datapoints:
            datapoint["date-time"] = now_str
    return grouped_datapoints


def main():
    data = get_mock_data(os.getenv("MOCK_DATA_SOURCE", "mock_data/hl7-monitor.json"))
    
    middleware_address = os.getenv("MIDDLEWARE_ADDRESS")
    if not middleware_address:
        print("MIDDLEWARE_ADDRESS is not set")
        exit(1)
        
    print(f"Mock CNS running for gateway: {middleware_address}")

    while True:
        for datapoints in data[:]:
            datapoints = replace_timestamps(datapoints)
            write_to_gateway(datapoints, middleware_address)
            time.sleep(4)


if __name__ == "__main__":
    main()
