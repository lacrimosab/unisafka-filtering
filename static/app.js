const filterForm = document.querySelector(".date-form");
const mealResults = document.querySelector("#meal-results");

const filterCheckboxes = filterForm.querySelectorAll(
    'input[type="checkbox"]'
);

// function that runs after checkbox changes
function handleFilterChange(event) {
    const formData = new FormData(filterForm)
    const parameters = new URLSearchParams(formData);
    
    const selectedDateButton = filterForm.querySelector(
        ".date-option--selected"
    );
    
    parameters.set(
        "menu_date",
        selectedDateButton.value
    )
    
    console.log(parameters.toString());
}

// visits all three checkboxes; addEventListener connects each checkbox to the function
filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", handleFilterChange);
});