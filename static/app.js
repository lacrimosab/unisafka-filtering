const filterForm = document.querySelector(".date-form");
const mealResults = document.querySelector("#meal-results");

const filterCheckboxes = filterForm.querySelectorAll(
    'input[type="checkbox"]'
);

const mealCards = mealResults.querySelectorAll(".meal-card");

const restaurantSections = mealResults.querySelectorAll(
    ".restaurant-section"
);

const noFilterResults = document.querySelector(
    "#no-filter-results"
);

// function that runs after checkbox changes
function handleFilterChange() {
    const veganOnly = filterForm.querySelector(
        '[name="vegan_only"]'
    ).checked;

    const glutenFreeOnly = filterForm.querySelector(
        '[name="gluten_free_only"]'
    ).checked;

    const lactoseFreeOnly = filterForm.querySelector(
        '[name="lactose_free_only"]'
    ).checked;

    mealCards.forEach((mealCard) => {
        const diets = mealCard.dataset.diets.split("|");

        const matchesVegan =
            !veganOnly || diets.includes("Vegan");
        
        const matchesGlutenFree =
            !glutenFreeOnly || diets.includes("Gluten-free");

        const matchesLactoseFree =
            !lactoseFreeOnly ||
            diets.includes("Lactose-free") ||
            diets.includes("Milk-free");

        const matchesAllFilters =
            matchesVegan &&
            matchesGlutenFree &&
            matchesLactoseFree;
        
        mealCard.hidden = !matchesAllFilters;
    });

    restaurantSections.forEach((restaurantSection) => {
        const visibleMeal = restaurantSection.querySelector(
            ".meal-card:not([hidden])"
        );

        const hasVisibleMeals = visibleMeal !== null;

        restaurantSection.hidden = !hasVisibleMeals;
    });
    
    if (noFilterResults !== null) {
        const visibleMeal = mealResults.querySelector(
            ".meal-card:not([hidden])"
        );

        const hasAnyVisibleMeal = visibleMeal !== null;

        noFilterResults.hidden = hasAnyVisibleMeal;
    }
}

// visits all three checkboxes; addEventListener connects each checkbox to the function
filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", handleFilterChange);
});

handleFilterChange();
document.documentElement.classList.add("js-enabled");