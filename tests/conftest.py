"""
Pytest configuration and fixtures for testing the Mergington High School API
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the src directory to the path to import the app module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state after each test"""
    # Store the initial state
    initial_state = {
        "Basketball Team": {
            "description": "Compete in basketball games and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Play soccer and develop athletic skills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and develop acting skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["ryan@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and compete in competitions",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": ["sarah@mergington.edu", "thomas@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    yield
    
    # Reset the activities to the initial state after the test
    activities.clear()
    activities.update(initial_state)
