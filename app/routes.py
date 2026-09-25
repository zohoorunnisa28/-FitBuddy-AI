from pathlib import Path

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter()


# ==========================================
# HOMEPAGE
# ==========================================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ==========================================
# WORKOUT + NUTRITION RESULT
# ==========================================

@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,

    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    # TEMPORARY PLAN
    # We will connect your Gemini AI here.

    workout_plan = """
DAY 1 — Full Body Strength
Squats — 3 × 12
Push-ups — 3 × 10
Lunges — 3 × 10
Plank — 3 × 30 sec

DAY 2 — Active Recovery
Walking — 30 min
Stretching — 10 min

DAY 3 — Upper Body
Push-ups — 3 × 10
Shoulder Press — 3 × 12
Rows — 3 × 12

DAY 4 — Recovery
Light Walking — 20 min
Mobility — 10 min

DAY 5 — Lower Body
Squats — 3 × 12
Lunges — 3 × 10
Glute Bridges — 3 × 15

DAY 6 — Cardio + Core
Cardio — 25 min
Crunches — 3 × 15
Plank — 3 × 30 sec

DAY 7 — Rest & Recovery
Light Walking
Stretching
Hydration
Quality Sleep
"""

    nutrition_tip = """
Focus on balanced meals, adequate protein,
vegetables, fruits, whole grains and hydration.
Prioritize recovery and consistent sleep.
"""


    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "username": username,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


# ==========================================
# FEEDBACK PAGE
# ==========================================

@router.get("/feedback", response_class=HTMLResponse)
async def feedback_page(
    request: Request,
    username: str = ""
):

    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={
            "request": request,
            "username": username
        }
    )


# ==========================================
# SUBMIT FEEDBACK
# ==========================================

@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,

    username: str = Form(""),

    difficulty: str = Form("Just Right"),

    changes: list[str] = Form([]),

    feedback: str = Form("")
):

    # TEMPORARY UPDATED PLAN
    # Later this section will use Gemini
    # to actually generate the adapted plan.

    updated_plan = f"""
UPDATED FITBUDDY PLAN

User Feedback:
Difficulty: {difficulty}

Requested Changes:
{", ".join(changes) if changes else "No specific changes"}

Additional Feedback:
{feedback if feedback else "No additional comments"}

DAY 1 — Adapted Strength
Squats — 3 × 10
Push-ups — 3 × 10
Lunges — 2 × 10
Plank — 3 × 30 sec

DAY 2 — Recovery
Walking — 25 min
Stretching — 10 min

DAY 3 — Upper Body
Push-ups — 3 × 10
Rows — 3 × 12
Shoulder Press — 3 × 10

DAY 4 — Active Recovery
Light Cardio — 20 min
Mobility — 10 min

DAY 5 — Lower Body
Squats — 3 × 10
Glute Bridges — 3 × 15
Lunges — 2 × 10

DAY 6 — Cardio + Core
Moderate Cardio — 20 min
Crunches — 3 × 15
Plank — 3 × 30 sec

DAY 7 — Rest
Recovery
Hydration
Stretching
Quality Sleep
"""


    return templates.TemplateResponse(
        request=request,
        name="updated_plan.html",
        context={
            "request": request,
            "username": username,
            "difficulty": difficulty,
            "changes": changes,
            "feedback": feedback,
            "updated_plan": updated_plan
        }
    )


# ==========================================
# TEST
# ==========================================

@router.get("/test")
async def test():

    return {
        "message": "FitBuddy routes are working!"
    }


# ==========================================
# HEALTH
# ==========================================

@router.get("/health")
async def health():

    return {
        "status": "ok"
    }