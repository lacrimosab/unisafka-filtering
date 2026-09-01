from src.providers.sodexo import get_hertsi_meal

meals = get_hertsi_meal("2026-09-01")

for meal in meals:
    diets = ", ".join(sorted(meal.diets)) or "No specific diets"
    allergens = ", ".join(sorted(meal.allergens)) or "No allergens"

    print(f"\n{meal.name}")
    print(f"  Diet codes: {diets}")
    print(f"  Allergens: {allergens}")

