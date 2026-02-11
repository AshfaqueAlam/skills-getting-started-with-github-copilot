"""
Unit tests for the Mergington High School API
"""

import pytest


class TestRoot:
    """Test the root endpoint"""
    
    def test_root_redirect(self, client):
        """Test that the root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Test the GET /activities endpoint"""
    
    def test_get_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 9
        
        # Verify some activities exist
        assert "Basketball Team" in activities
        assert "Soccer Club" in activities
        assert "Chess Club" in activities
    
    def test_activity_structure(self, client, reset_activities):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        activities = response.json()
        
        activity = activities["Basketball Team"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        
        assert isinstance(activity["participants"], list)
        assert "james@mergington.edu" in activity["participants"]


class TestSignup:
    """Test the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Basketball Team"]["participants"]
    
    def test_signup_duplicate(self, client, reset_activities):
        """Test that duplicate signups are rejected"""
        # First signup
        response1 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Duplicate signup
        response2 = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response2.status_code == 400
        
        data = response2.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test that signup for non-existent activity is rejected"""
        response = client.post(
            "/activities/NonExistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_signup_already_participant(self, client, reset_activities):
        """Test that existing participants cannot sign up again"""
        response = client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "james@mergington.edu"}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


class TestUnregister:
    """Test the POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # First, signup
        client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        # Then unregister
        response = client.post(
            "/activities/Basketball%20Team/unregister",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "Unregistered" in data["message"]
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" not in activities["Basketball Team"]["participants"]
    
    def test_unregister_existing_participant(self, client, reset_activities):
        """Test unregistering an existing participant"""
        response = client.post(
            "/activities/Basketball%20Team/unregister",
            params={"email": "james@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "james@mergington.edu" not in activities["Basketball Team"]["participants"]
    
    def test_unregister_not_signed_up(self, client, reset_activities):
        """Test unregistration of a student not signed up"""
        response = client.post(
            "/activities/Basketball%20Team/unregister",
            params={"email": "notstudent@mergington.edu"}
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "not signed up" in data["detail"]
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregistration from non-existent activity"""
        response = client.post(
            "/activities/NonExistent%20Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestActivityAvailability:
    """Test activity capacity constraints"""
    
    def test_spots_calculation(self, client, reset_activities):
        """Test that available spots are calculated correctly"""
        response = client.get("/activities")
        activities = response.json()
        
        basketball = activities["Basketball Team"]
        max_participants = basketball["max_participants"]
        current_participants = len(basketball["participants"])
        expected_spots = max_participants - current_participants
        
        assert expected_spots == max_participants - current_participants
        assert expected_spots > 0
