def validate_goal_input(user_input: str) -> bool:
    # Basic validation for goal format (e.g., "lose 5kg in 2 months")
    parts = user_input.lower().split()
    return any(word in parts for word in ["lose", "gain"]) and any(word.isdigit() for word in parts) and "in" in parts

def validate_dietary_input(user_input: str) -> bool:
    # Basic validation for dietary preferences
    valid_diets = ["vegetarian", "vegan", "diabetic", "gluten-free"]
    return any(diet in user_input.lower() for diet in valid_diets)