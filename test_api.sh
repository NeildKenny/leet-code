#!/usr/bin/env bash
# Simple script to exercise the HTTP API using curl
# Assumes the server is already running on localhost:8001

set -e

API="http://localhost:8001"

# Register a new user
curl -s -X POST "$API/register" -d "username=demo" -d "password=secret" |
  tee /tmp/user.json

USER_ID=$(jq -r '.id' /tmp/user.json)

# Create a campaign
curl -s -X POST "$API/campaigns" -d "name=My Campaign" -d "description=Test" |
  tee /tmp/campaign.json

CAMPAIGN_ID=$(jq -r '.id' /tmp/campaign.json)

# Create a note
curl -s -X POST "$API/notes" \
  -d "campaign_id=$CAMPAIGN_ID" \
  -d "author_id=$USER_ID" \
  -d "title=First Note" \
  -d "body=Hello" |
  tee /tmp/note.json

# List notes
curl -s "$API/notes" | jq
