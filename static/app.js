const filterForm = document.querySelector(".date-form");
const mealResults = document.querySelector("#meal-results");

const filterCheckboxes = filterForm.querySelectorAll(
    'input[type="checkbox"]'
);

const dateButtons = filterForm.querySelectorAll(
    ".date-option"
);

const dayResults = mealResults.querySelectorAll(
    ".day-results"
);

const mealCards = mealResults.querySelectorAll(".meal-card");

const restaurantSections = mealResults.querySelectorAll(
    ".restaurant-section"
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

    const selectedDayResults = mealResults.querySelector(
        ".day-results:not([hidden])"
    );

    const noFilterResults = selectedDayResults.querySelector(
        ".no-filter-results"
    );
    
    if (noFilterResults !== null) {

        if (noFilterResults !== null) {
            const visibleMeal = selectedDayResults.querySelector(
                ".meal-card:not([hidden])"
            );

            noFilterResults.hidden = visibleMeal !== null;
        }
    }
}

function handleDateClick(event) {
    event.preventDefault();

    const selectedButton = event.currentTarget;
    const selectedDate = selectedButton.value;

    dateButtons.forEach((dateButton) => {
        dateButton.classList.toggle(
            "date-option--selected",
            dateButton === selectedButton
        );
    });

    dayResults.forEach((dayResult) => {
        dayResult.hidden =
            dayResult.dataset.menuDate !== selectedDate;
    });

    handleFilterChange();
}

dateButtons.forEach((dateButton) => {
    dateButton.addEventListener(
        "click",
        handleDateClick
    );
});

// visits all three checkboxes; addEventListener connects each checkbox to the function
filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", handleFilterChange);
});


// this call is necessary because it performs synchronization immediately
handleFilterChange();
document.documentElement.classList.add("js-enabled");