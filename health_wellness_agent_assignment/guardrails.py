from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict
import re

class Goal(BaseModel):
    action: str
    quantity: float
    metric: str
    duration: Optional[str] = None

class MealPlan(BaseModel):
    meals: List[str]

class WorkoutPlan(BaseModel):
    exercises: Dict[str, str]

class Schedule(BaseModel):
    checkins: List[str]

class ProgressUpdate(BaseModel):
    update: Dict[str, str]

def validate_goal_input(input_str: str) -> bool:
    pattern = r"^(lose|gain)\s+(\d+\.?\d*)\s*(kg|lbs|pounds)\s*(in)?\s*(\d+\s*(months|weeks))?$"
    return bool(re.match(pattern, input_str.lower()))

def validate_goal_output(data: dict) -> Goal:
    try:
        return Goal(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid goal output format: {e}")

def validate_dietary_input(input_str: str) -> bool:
    valid_diets = ["vegetarian", "vegan", "keto", "gluten-free", "diabetic"]
    return input_str.lower() in valid_diets

def validate_meal_plan_output(data: dict) -> MealPlan:
    try:
        return MealPlan(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid meal plan output format: {e}")

def validate_workout_plan_output(data: dict) -> WorkoutPlan:
    try:
        return WorkoutPlan(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid workout plan output format: {e}")

def validate_schedule_output(data: dict) -> Schedule:
    try:
        return Schedule(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid schedule output format: {e}")

def validate_progress_update_output(data: dict) -> ProgressUpdate:
    try:
        return ProgressUpdate(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid progress update output format: {e}")