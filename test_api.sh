#!/usr/bin/env bash
# Simple script to exercise the HTTP API using curl
# Assumes the server is already running on localhost:8001

set -e

API="http://localhost:8001"

# Register a new user with a profile picture
curl -s -X POST "$API/register" \
  -d "username=demo" \
  -d "password=secret" \
  -d "profile_picture_url=https://example.com/user.png" |
  tee /tmp/user.json

USER_ID=$(jq -r '.id' /tmp/user.json)

# Create a campaign with a short description
curl -s -X POST "$API/campaigns" \
  -d "name=My Campaign" \
  -d "description=Sample campaign for the demo" |
  tee /tmp/campaign.json

CAMPAIGN_ID=$(jq -r '.id' /tmp/campaign.json)

# Create a note demonstrating all fields
curl -s -X POST "$API/notes" \
  -d "campaign_id=$CAMPAIGN_ID" \
  -d "author_id=$USER_ID" \
  -d "title=First Note" \
  -d "body=This is a demo note." \
  -d "image_url=https://example.com/note.png" \
  -d "session_name=Session 1" \
  -d "session_date=2025-06-16" \
  -d "session_number=1" \
  -d "category=General" |
  tee /tmp/note.json

# List notes
curl -s "$API/notes" | jq
