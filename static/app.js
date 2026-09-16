const filterForm = document.querySelector(".date-form");
const mealResults = document.querySelector("#meal-results");

const filterCheckboxes = filterForm.querySelectorAll(
    'input[type="checkbox"]'
);

// function that runs after checkbox changes
function handleFilterChange(event) {
    // event.target is the specific checkbox the user clicked
    const changedCheckbox = event.target;

    console.log(
        changedCheckbox.name,
        changedCheckbox.checked
    );
}

// visits all three checkboxes; addEventListener connects each checkbox to the function
filterCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", handleFilterChange);
})