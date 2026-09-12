from src.providers.sodexo import get_hertsi_meal

meals = get_hertsi_meal("2026-09-14")

for meal in meals:
    diets = ", ".join(sorted(meal.diets)) or "No dietary information"
    allergens = ", ".join(sorted(meal.allergens)) or "No allergen information"

    print(f"\n{meal.name}")
    print(f"  Dietary labels: {diets}")
    print(f"  Allergens: {allergens}")

