#!/usr/bin/env python3
#
# (C) 2020 Jannik Vogel
#
# Licensed under AGPLv3 only.
# See LICENSE.md for more information.
#

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests


# Set up your server here
HOST = "192.30.255.113"
PORT = 8000

# Set up your repository here
OWNER="alexvatti"
REPO="hello-world-lib"
BRANCH="main"
WORKFLOW_NAME="GitHub-Actions-lib-add"
WORKFLOW_EVENT="push"
ARTIFACT_NAME="lib-artifact"

API_URL="https://api.github.com"

def get_workflow_id(workflow_name):
  response = requests.get("%s/repos/%s/%s/actions/workflows" % (API_URL, OWNER, REPO))
  print(response.status_code)
  json = response.json()
  for workflow in json['workflows']:
    if workflow['name'] == workflow_name:
      print(workflow['name'])
      return workflow['id']
  return None #FIXME: Exception

def get_latest_workflow_run_id(workflow_id, workflow_event):
  response = requests.get("%s/repos/%s/%s/actions/workflows/%s/runs" % (API_URL, OWNER, REPO, workflow_id))
  print(response.status_code)
  json = response.json()
  for workflow_run in json['workflow_runs']:

    # Only consider completed runs
    if workflow_run['status'] != "completed":
      continue
    if workflow_run['conclusion'] != "success":
      continue

    # Match by BRANCH
    if workflow_run['head_branch'] != BRANCH:
      continue

    # Match by event
    if workflow_run['event'] != workflow_event:
      continue

    return workflow_run['id']

  return None #FIXME: Exception

def get_artifact_id(workflow_run_id, name):
  response = requests.get("%s/repos/%s/%s/actions/runs/%s/artifacts" % (API_URL, OWNER, REPO, workflow_run_id))
  print(response.status_code)
  json = response.json()
  for artifact in json['artifacts']:

    # Match by name
    if artifact['name'] == name:
      return artifact['id']

  return None #FIXME: Exception

def get_artifact_id(workflow_run_id, name):
  response = requests.get("%s/repos/%s/%s/actions/runs/%s/artifacts" % (API_URL, OWNER, REPO, workflow_run_id))
  print(response.status_code)
  json = response.json()
  for artifact in json['artifacts']:

    # Match by name
    if artifact['name'] == name:
      return artifact['id']

  return None #FIXME: Exception

def get_latest_artifact_url(workflow_name, worfklow_event, artifact_name):

  workflow_id = get_workflow_id(workflow_name)
  print("found workflow", workflow_id)

  workflow_run_id = get_latest_workflow_run_id(workflow_id, worfklow_event)
  print("found workflow_run_id %d" % workflow_run_id)

  artifact_id = get_artifact_id(workflow_run_id, artifact_name)
  print("found artifact_id %d" % workflow_run_id)

  return "%s/repos/%s/%s/actions/artifacts/%s/zip" % (API_URL, OWNER, REPO, artifact_id)

if __name__ == "__main__":
  # Code to test the URL fetcher
  if True:
    artifact_url = get_latest_artifact_url(WORKFLOW_NAME, WORKFLOW_EVENT, ARTIFACT_NAME)
    print(artifact_url)
