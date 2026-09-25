import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-flash"
)

TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-2.5-flash"
)

client = None

if API_KEY and API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


def demo_workout(
    name,
    age,
    weight,
    goal,
    intensity
):
    return f"""
DAY 1 — FULL BODY FOUNDATION

Warm-up:
• 5 minutes brisk walking
• Arm circles
• Bodyweight squats

Workout:
• Bodyweight Squats — 3 sets × 12 reps
• Push-ups — 3 sets × 8 reps
• Glute Bridges — 3 sets × 15 reps
• Plank — 3 sets × 30 seconds

Recovery:
5–10 minutes of stretching and hydration.


DAY 2 — CARDIO & CORE

Warm-up:
• 5 minutes light walking
• Dynamic stretching

Workout:
• Brisk Walk — 20 minutes
• Mountain Climbers — 3 × 20
• Bicycle Crunches — 3 × 15
• Plank — 3 × 30 seconds

Recovery:
Walk slowly for 5 minutes and stretch.


DAY 3 — LOWER BODY

Warm-up:
• 5 minutes easy movement

Workout:
• Squats — 3 × 12
• Reverse Lunges — 3 × 10 each leg
• Glute Bridges — 3 × 15
• Calf Raises — 3 × 20

Recovery:
Lower-body stretching and hydration.


DAY 4 — ACTIVE RECOVERY

Activity:
• 20–30 minute relaxed walk
• Mobility exercises
• Full-body stretching

Focus:
Recovery, hydration and quality sleep.


DAY 5 — UPPER BODY

Warm-up:
• Arm circles
• Shoulder mobility

Workout:
• Push-ups — 3 × 8
• Incline Push-ups — 3 × 10
• Shoulder Taps — 3 × 16
• Plank — 3 × 30 seconds

Recovery:
Upper-body stretching.


DAY 6 — CARDIO CHALLENGE

Warm-up:
• 5 minutes walking

Workout:
• Fast Walk — 10 minutes
• Easy Jog — 10 minutes
• High Knees — 3 × 20
• Jumping Jacks — 3 × 20

Recovery:
Slow walking and stretching.


DAY 7 — RESET & RECOVER

Activity:
• Gentle walking
• Full-body mobility
• Light stretching

Reflection:
Review your energy, consistency and progress from the week.

FITBUDDY SAFETY NOTE:
Start at a comfortable level and stop if you experience pain, dizziness or unusual discomfort.
"""


def generate_workout(
    name,
    age,
    weight,
    goal,
    intensity
):
    prompt = f"""
You are FitBuddy, an intelligent personal fitness coach.

Create a personalized 7-day beginner-friendly fitness plan.

User:
Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:

1. Create exactly 7 days.
2. Give every day a clear title.
3. Include a warm-up.
4. Include exercises.
5. Include sets and repetitions where appropriate.
6. Include recovery guidance.
7. Make the plan practical and easy to understand.
8. Adapt the plan to the user's goal and intensity.
9. Include an active recovery/rest day.
10. Do not make dangerous medical claims.
11. Finish with a short safety note.

Use this format:

DAY 1 — TITLE

Warm-up:
• ...

Workout:
• Exercise — sets × reps
• Exercise — sets × reps

Recovery:
...

DAY 2 — TITLE

...

Continue through DAY 7.
"""

    if client is None:
        return demo_workout(
            name,
            age,
            weight,
            goal,
            intensity
        )

    try:
        response = client.models.generate_content(
            model=WORKOUT_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Gemini workout error:", error)

        return demo_workout(
            name,
            age,
            weight,
            goal,
            intensity
        )


def generate_nutrition_tip(
    goal,
    weight,
    intensity
):
    prompt = f"""
You are FitBuddy AI.

Give a concise personalized wellness and nutrition recommendation.

Goal: {goal}
Weight: {weight} kg
Workout intensity: {intensity}

Include:
• hydration
• protein/whole-food guidance
• vegetables/fruits
• recovery
• sleep

Do not prescribe medical treatment.

Keep the answer motivational and practical.
Maximum 150 words.
"""

    if client is None:
        return """
💧 Stay hydrated throughout the day.

🥗 Build meals around vegetables, fruits,
whole grains and protein-rich foods.

🍳 Include a quality protein source with meals
to support recovery.

😴 Aim for consistent, good-quality sleep.

⚡ Most importantly, focus on consistency rather
than trying to be perfect every day.
"""

    try:
        response = client.models.generate_content(
            model=TIP_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Gemini nutrition error:", error)

        return """
💧 Stay hydrated.

🥗 Choose balanced meals with vegetables,
fruits, whole foods and protein.

😴 Prioritize recovery and consistent sleep.

💪 Consistency matters more than perfection.
"""


def adapt_workout(
    old_plan,
    feedback
):
    prompt = f"""
You are FitBuddy AI.

The user has completed a personalized workout plan
and provided feedback.

ORIGINAL PLAN:
{old_plan}

USER FEEDBACK:
{feedback}

Create an improved version of the workout plan.

Rules:
1. Respect the user's feedback.
2. Keep the plan realistic.
3. Keep exactly 7 days.
4. Adjust exercise volume or difficulty when appropriate.
5. Clearly show the updated 7-day plan.
6. Include recovery guidance.
7. Do not make medical claims.
8. End with a short safety reminder.

Make the adaptation obvious and practical.
"""

    if client is None:
        return old_plan + f"""

AI ADAPTATION

Your feedback:
{feedback}

FitBuddy recommends gradually adjusting workout
difficulty based on your energy, recovery and
consistency.
"""

    try:
        response = client.models.generate_content(
            model=WORKOUT_MODEL,
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Gemini adaptation error:", error)

        return old_plan + f"""

AI ADAPTATION

Your feedback:
{feedback}

Please continue at a comfortable intensity and
gradually adjust your workload.
"""