from langchain.tools import tool

@tool
def calculate_bmi(weight: float, height: float) -> str:
    """
    Calculates the Body Mass Index (BMI) and provides a classification.

    Args:
        weight (float): Weight in kilograms (kg).
        height (float): Height in centimeters (cm).

    Returns:
        str: A string containing the calculated BMI and its classification.
    """
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    bmi = round(bmi, 2)

    if bmi < 18.5:
        classification = "Bajo peso"
    elif 18.5 <= bmi < 25:
        classification = "Peso normal"
    elif 25 <= bmi < 30:
        classification = "Sobrepeso"
    else:
        classification = "Obesidad"

    return f"Tu IMC es {bmi}, lo que se clasifica como: {classification}."

@tool
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> str:
    """
    Calculates the Basal Metabolic Rate (BMR) using the Mifflin-St Jeor formula.

    Args:
        weight (float): Weight in kilograms (kg).
        height (float): Height in centimeters (cm).
        age (int): Age in years.
        gender (str): Gender, either 'hombre' (male) or 'mujer' (female).

    Returns:
        str: The calculated Basal Metabolic Rate (BMR) as a string.
    """
    if gender.lower() == 'hombre':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender.lower() == 'mujer':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("El género debe ser 'hombre' o 'mujer'.")
    
    return str(round(bmr, 2))

@tool
def calculate_macros(bmr: float, activity_level: str, goal: str) -> str:
    """
    Calculates the recommended daily macronutrients based on BMR, activity level, and goal.

    Args:
        bmr (float): Basal Metabolic Rate.
        activity_level (str): The user's activity level.
            Options: 'Sedentario', 'Ligero', 'Moderado', 'Activo', 'Muy Activo'.
        goal (str): The user's weight goal.
            Options: 'Bajar de peso', 'Mantener peso', 'Subir de peso'.

    Returns:
        str: A formatted string detailing the recommended grams of protein, carbohydrates, and fats.
    """
    activity_multipliers = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'activo': 1.725,
        'muy activo': 1.9
    }

    goal_adjustments = {
        'bajar de peso': -500,
        'mantener peso': 0,
        'subir de peso': 500
    }

    multiplier = activity_multipliers.get(activity_level.lower())
    if not multiplier:
        raise ValueError(f"Nivel de actividad '{activity_level}' no es válido.")

    adjustment = goal_adjustments.get(goal.lower())
    if adjustment is None:
        raise ValueError(f"Objetivo '{goal}' no es válido.")

    total_calories = (bmr * multiplier) + adjustment

    # Macronutrient distribution: 40% Carbs, 30% Protein, 30% Fat
    protein_grams = round(((total_calories * 0.30) / 4), 2)
    carbs_grams = round(((total_calories * 0.40) / 4), 2)
    fats_grams = round(((total_calories * 0.30) / 9), 2)

    return f"Para alcanzar tu objetivo, te recomiendo consumir aproximadamente: Proteínas: {protein_grams}g, Carbohidratos: {carbs_grams}g, Grasas: {fats_grams}g."