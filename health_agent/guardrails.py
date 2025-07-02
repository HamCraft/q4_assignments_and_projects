"""
Guardrails for Health & Wellness Assistant
Validates user inputs and system outputs for safety and accuracy
"""

import re
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, validator

class InputValidator:
    """Validates user inputs for safety and format"""
    
    @staticmethod
    def validate_goal(goal_text: str) -> Tuple[bool, str]:
        """Validate user's health goal input"""
        if not goal_text or len(goal_text.strip()) < 3:
            return False, "Please provide a clear health goal"
        
        goal_lower = goal_text.lower().strip()
        
        # Check for unsafe weight loss goals
        if "lose" in goal_lower and "kg" in goal_lower:
            try:
                # Extract weight amount
                numbers = re.findall(r'\d+\.?\d*', goal_text)
                if numbers:
                    weight_loss = float(numbers[0])
                    if weight_loss > 10:
                        return False, "Weight loss goal exceeds safe limits (max 10kg recommended)"
                    if weight_loss < 0.5:
                        return False, "Weight loss goal too small (minimum 0.5kg)"
            except:
                return False, "Could not understand weight loss amount"
        
        # Check for supported injury types
        if "injury" in goal_lower:
            supported_injuries = ["knee", "back", "shoulder", "ankle", "wrist"]
            if not any(injury in goal_lower for injury in supported_injuries):
                return False, f"Supported injuries: {', '.join(supported_injuries)}"
        
        # Block unsafe requests
        unsafe_terms = ["extreme", "fast", "dangerous", "starve", "overdose"]
        if any(term in goal_lower for term in unsafe_terms):
            return False, "Goal contains unsafe terms. Please use safe, healthy approaches"
        
        return True, "Goal validated successfully"
    
    @staticmethod
    def validate_diet_preferences(diet_pref: str) -> Tuple[bool, str]:
        """Validate dietary preferences"""
        allowed_diets = ["balanced", "vegetarian", "vegan", "keto", "mediterranean", "low-carb"]
        if diet_pref.lower() not in allowed_diets:
            return False, f"Supported diets: {', '.join(allowed_diets)}"
        return True, "Diet preference validated"

class OutputValidator:
    """Validates system outputs for safety and completeness"""
    
    @staticmethod
    def validate_meal_plan(meal_plan: List[str]) -> Tuple[bool, str]:
        """Validate generated meal plan"""
        if not meal_plan or len(meal_plan) < 7:
            return False, "Meal plan must contain 7 days"
        
        # Check each day has proper structure
        for i, day_plan in enumerate(meal_plan[:7]):  # Check first 7 days only
            if not day_plan.startswith(f"Day {i+1}:"):
                return False, f"Day {i+1} format incorrect"
            
            # Ensure each day has meals
            required_meals = ["breakfast", "lunch", "dinner"]
            day_lower = day_plan.lower()
            missing_meals = [meal for meal in required_meals if meal not in day_lower]
            if missing_meals:
                return False, f"Day {i+1} missing meals: {', '.join(missing_meals)}"
        
        return True, "Meal plan validated"
    
    @staticmethod
    def validate_workout_plan(workout_plan: Dict) -> Tuple[bool, str]:
        """Validate generated workout plan"""
        if not workout_plan or len(workout_plan) < 7:
            return False, "Workout plan must contain 7 days"
        
        required_days = [f"Day {i}" for i in range(1, 8)]
        missing_days = [day for day in required_days if day not in workout_plan]
        if missing_days:
            return False, f"Missing workout days: {', '.join(missing_days)}"
        
        # Check for unsafe exercises for injuries
        for day, exercise in workout_plan.items():
            if day == "Note":
                continue
                
            exercise_lower = exercise.lower()
            if "injury" in str(workout_plan.get("Note", "")).lower():
                unsafe_exercises = ["jumping", "running", "high-impact", "heavy lifting"]
                if any(unsafe in exercise_lower for unsafe in unsafe_exercises):
                    return False, f"{day} contains unsafe exercise for injury recovery"
        
        return True, "Workout plan validated"

class SafetyChecks:
    """Additional safety checks for health recommendations"""
    
    @staticmethod
    def check_calorie_deficit(daily_deficit: float) -> Tuple[bool, str]:
        """Ensure calorie deficit is safe"""
        if daily_deficit > 1000:
            return False, "Daily calorie deficit too high (max 1000 kcal recommended)"
        if daily_deficit < 200:
            return False, "Daily calorie deficit too low (min 200 kcal for weight loss)"
        return True, "Calorie deficit is safe"
    
    @staticmethod
    def medical_disclaimer() -> str:
        """Return medical disclaimer for all health advice"""
        return ("⚠️  DISCLAIMER: This is general wellness guidance only. "
                "Consult healthcare professionals before starting any new diet or exercise program, "
                "especially if you have medical conditions or injuries.")

def validate_user_input(goal_text: str, diet_pref: str = "balanced") -> Tuple[bool, str]:
    """Main input validation function"""
    # Validate goal
    goal_valid, goal_msg = InputValidator.validate_goal(goal_text)
    if not goal_valid:
        return False, f"Goal validation failed: {goal_msg}"
    
    # Validate diet preference
    diet_valid, diet_msg = InputValidator.validate_diet_preferences(diet_pref)
    if not diet_valid:
        return False, f"Diet validation failed: {diet_msg}"
    
    return True, "All inputs validated successfully"

def validate_system_output(meal_plan: List[str], workout_plan: Dict) -> Tuple[bool, str]:
    """Main output validation function"""
    # Validate meal plan
    meal_valid, meal_msg = OutputValidator.validate_meal_plan(meal_plan)
    if not meal_valid:
        return False, f"Meal plan validation failed: {meal_msg}"
    
    # Validate workout plan
    workout_valid, workout_msg = OutputValidator.validate_workout_plan(workout_plan)
    if not workout_valid:
        return False, f"Workout plan validation failed: {workout_msg}"
    
    return True, "All outputs validated successfully"