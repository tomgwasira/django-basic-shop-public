#!/usr/bin/env python
"""General tests for *Shop* project."""

# Third-party library imports
import pytest


def test_allowed_hosts(client):
    """Tests allowed hosts."""
    pass
    # response = client.get("/", HTTP_HOST="noadress.com")
    # assert response.status_code == 400

    # response = client.get("/", HTTP_HOST="127.0.0.1")
    # assert response.status_code == 200
