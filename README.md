# AMS Monitoring Connector

## Overview

AMS Monitoring Connector is a vendor-independent monitoring integration platform.

The connector retrieves logs from enterprise monitoring tools and exposes a unified API for downstream systems such as ServiceNow, Jira, PagerDuty, and AI Agents.

---

## Supported Monitoring Providers

- New Relic
- Datadog
- Splunk
- Grafana
- Elastic (Planned)

---

## Supported Incident Providers

- ServiceNow
- Jira
- PagerDuty
- Opsgenie

---

## Architecture

Applications

↓

Monitoring Tool

↓

AMS Monitoring Connector

↓

Incident Platform

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Requests

---