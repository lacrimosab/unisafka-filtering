from src.providers.sodexo import get_hertsi_meal

meals = get_hertsi_meal("2026-09-01")

for meal in meals:
    print(meal)