from dataclasses import dataclass, field

@dataclass
class Meal:
    restaurant: str
    name: str

    diets: set[str] = field(default_factory=set)
    allergens: set[str] = field(default_factory=set)

    calories: float | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None

    price: float | None = None

