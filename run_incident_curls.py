#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

from tests.tests_microservices.utils.incidents.incidents_api import IncidentsAPI


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    token = os.getenv("EPUTS_TOKEN")
    if not token:
        print("ERROR: Set EPUTS_TOKEN with a valid Bearer token.")
        sys.exit(2)

    base = Path("curl")
    update_json = base / "incident_update.json"
    list_json = base / "incident_list.json"

    if update_json.exists():
        data = read_json(update_json)
        incident_id = data.get("id")
        if not incident_id:
            print("incident_update.json must include 'id'")
        else:
            resp = IncidentsAPI.update_incident(incident_id=incident_id, data=data)
            print("PUT /incident/{id}:", resp.status_code)
            print(resp.text[:2000])

    if list_json.exists():
        payload = read_json(list_json)
        resp = IncidentsAPI.list_incidents(payload)
        print("POST /incident/list:", resp.status_code)
        print(resp.text[:2000])

    # Example delete flow via env var INCIDENT_DELETE_ID
    delete_id = os.getenv("INCIDENT_DELETE_ID")
    if delete_id:
        try:
            incident_id = int(delete_id)
        except ValueError:
            print("INCIDENT_DELETE_ID must be int")
        else:
            resp = IncidentsAPI.delete_incident(incident_id)
            print("DELETE /incident/{id}:", resp.status_code)
            print(resp.text[:2000])


if __name__ == "__main__":
    main()


