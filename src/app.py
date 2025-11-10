"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
# Additional activities to be merged into the in-memory database at startup
_extra_activities = {
    # Sports (2)
    "Soccer Team": {
        "description": "Competitive and recreational soccer practices and matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Lap training, technique work and friendly swim meets",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu"]
    },

    # Artistic (2)
    "Art Club": {
        "description": "Open-studio time for painting, drawing, and mixed media",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["charlotte@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stagecraft, and production of student plays",
        "schedule": "Tuesdays, 5:00 PM - 7:00 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu"]
    },

    # Intellectual (2)
    "Science Olympiad": {
        "description": "Team-based STEM challenges and competition preparation",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive policy and public forum debating practice",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["mason@mergington.edu"]
    }
}

@app.on_event("startup")
def _merge_extra_activities():
    # Merge the extra activities into the main activities dict once it's available.
    if "activities" in globals() and isinstance(globals()["activities"], dict):
        globals()["activities"].update(_extra_activities)
    else:
        # If activities hasn't been defined yet for some reason, initialize it.
        globals()["activities"] = _extra_activities.copy()
activities = {
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


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate student is not already signed up
    for activity in activities.values():
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up for an activity")
        
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
