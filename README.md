# US National Parks Explorer

An interactive Streamlit dashboard that visualizes US National Parks using data from the National Park Service (NPS) API. The application allows users to explore parks geographically, filter by state, and analyze park activities.

---

## Live Demo

https://nps-dashboard-project.streamlit.app/

---

## Overview

This application provides an interactive way to explore US National Parks data through:

- An interactive map-based visualization of national parks
- State-based filtering
- Activity distribution analysis
- Detailed park information viewer

The dashboard updates dynamically based on user interaction.

---

## Features

### Map View
- Interactive map of US National Parks
- Parks are color-coded by activity count
- Click on a park to view detailed information

### State Filtering
- Multi-select filtering by US states
- Dynamically updates map, KPIs, and activity analysis

### Activity Analysis
- Displays most common park activities
- Updates based on selected filters

### Data Explorer
- Structured table of park information
- Includes park name, states, designation, and activities

---

## Tech Stack

- Streamlit
- Pandas
- Plotly Express
- Requests

---

## Data Source

Data is retrieved from the National Park Service (NPS) API:

https://www.nps.gov/subjects/developer/api-documentation.htm

---

## API Usage

This application uses a server-side API key stored securely using Streamlit Secrets.

Users do not need their own API key. All requests to the National Park Service API are handled by the deployed application.

---

## API Key Setup (Deployment)

For Streamlit Cloud deployment, the following secret must be configured:

```toml
NPS_API_KEY = "your_api_key_here"