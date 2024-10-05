
// Function to add new author fields with Bootstrap classes and "Delete" button at the end of the row
function addAuthor() {
    const authorContainer = document.getElementById('author-container');
    const newAuthorDiv = document.createElement('div');
    newAuthorDiv.classList.add('form-row', 'align-items-center', 'mb-2');

    newAuthorDiv.innerHTML = `
        <div class="col-md">
            <label>First Name:</label>
            <input type="text" class="form-control" name="first_name[]" required>
        </div>
        <div class="col-md">
            <label>Last Name:</label>
            <input type="text" class="form-control" name="last_name[]" required>
        </div>
        <div class="col-md">
            <label>ORCID ID:</label>
            <input type="text" class="form-control" name="orcid[]" required>
        </div>
        <div class="col-md">
            <label>Email:</label>
            <input type="email" class="form-control" name="email[]" required>
        </div>
        <div class="col-md-1 text-right mt-2">
            <button type="button" class="btn btn-danger" onclick="deleteAuthor(this)">Delete Author</button>
        </div>
    `;
    authorContainer.appendChild(newAuthorDiv);
}

// Function to add new standard name rows with Bootstrap classes and "Delete" button at the end of the row
function addStandardNameRow() {
    const standardNameContainer = document.getElementById('standard-name-container');
    const newRow = document.createElement('div');
    newRow.classList.add('form-row', 'align-items-center', 'mb-2');

    newRow.innerHTML = `
        <div class="col-md-3">
            <label>Name:</label>
            <input type="text" class="form-control" name="standard_name[]" required>
        </div>
        <div class="col-md-1">
            <label title="SI unit, e.g. m/s">Unit:</label>
            <input type="text" class="form-control" name="unit[]" placeholder="SI unit" title="E.g. m/s" required>
        </div>
        <div class="col-md-5">
            <label>Description:</label>
            <input type="text" class="form-control" name="name_description[]" required>
        </div>
        <div class="col-md-2">
            <label>Vector:</label>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="is_vector[]">
            </div>
        </div>
        <div class="col-md-1 text-right mt-2">
            <button type="button" class="btn btn-danger" onclick="deleteStandardName(this)">Delete</button>
        </div>
    `;
    standardNameContainer.appendChild(newRow);
}


// Function to delete an author row
function deleteAuthor(button) {
    const authorRow = button.parentNode.parentNode;
    authorRow.remove();
}



// Function to delete a standard name row
function deleteStandardName(button) {
    const standardNameRow = button.parentNode.parentNode;
    standardNameRow.remove();
}

// Function to add new qualification fields with Bootstrap classes and delete button
function addQualification() {
    const qualificationContainer = document.getElementById('qualification-container');
    const newQualificationDiv = document.createElement('div');
    newQualificationDiv.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', 'mb-2');

    newQualificationDiv.innerHTML = `
        <div class="w-100">
            <div class="form-row">
                <div class="col-md-3">
                    <label>Name:</label>
                    <input type="text" class="form-control" name="qualification_name[]" required oninput="updateConfiguration()">
                </div>
                <div class="col-md-3">
                    <label>Valid Values:</label>
                    <input type="text" class="form-control" name="valid_values[]" placeholder="Comma sep. list, e.g. x,y,z" required>
                </div>
                <div class="col-md-2">
                    <label>Preposition:</label>
                    <input type="text" class="form-control" name="preposition[]" placeholder='E.g. "at", "assuming", ...' required>
                </div>
                <div class="col-md-3">
                    <label>Description:</label>
                    <input type="text" class="form-control" name="qualification_description[]" required>
                </div>
                <div class="col-md-2">
                    <div class="form-check d-flex align-items-center">
                        <input class="form-check-input" type="checkbox" name="vector[]" id="vectorCheckbox">
                        <label class="form-check-label ml-2" for="vectorCheckbox">
                            Vector?
                        </label>
                    </div>
                </div>
            </div>
        </div>
        <button type="button" class="btn btn-danger btn-sm" onclick="deleteQualification(this)">Delete</button>
    `;

    qualificationContainer.appendChild(newQualificationDiv);
    updateConfiguration();
}

// Function to delete a qualification row
function deleteQualification(button) {
    button.parentElement.remove();
    updateConfiguration();
}

// Function to update the current configuration display
function updateConfiguration() {
    const qualificationContainer = document.getElementById('qualification-container');

    const qualificationHeading = document.getElementById('qualification-heading'); // Select the heading

    const qualifications = qualificationContainer.querySelectorAll('.list-group-item');

    // Static "AnyStandardName" line
    const defaultLine = "AnyStandardName";

    // Collect all qualifications
    const configItems = [];
    qualifications.forEach((qualification, index) => {
        const name = qualification.querySelector('input[name="qualification_name[]"]')?.value;

        const vectorText = name; // Use name as vector if checked
        configItems.push(vectorText); // Collect items for configuration
    });

    let configurationString = ''; // Initialize configuration string
    // Adding "AnyStandardName" at the end or dynamically based on the positions
    console.log("configItems")
    console.log(configItems)
    if (configItems.length > 0) {
        configItems.forEach((item, index) => {
        console.log(`${item} ${index}`)
            if (item === "AnyStandardName") {
                configurationString += "AnyStandardName"; // Append first item
            } else {
                if (item != '') {
                    configurationString += ` [${item}] `; // Append item
                }
            }
        });

        // Update the heading with the configuration
        console.log(configurationString)
        if (configurationString.trim() == 'AnyStandardName') {
            if (configItems.length > 1) {
                qualificationHeading.innerHTML = 'Construction Rule: Waiting for the qualification to get a name...';
            } else {
                qualificationHeading.innerHTML = 'Construction Rule: No Qualification added...';
            }
        }
        else {
            qualificationHeading.innerHTML = `Construction Rule: ${configurationString.trim()}`;
        }
    } else {
        qualificationHeading.innerHTML = `Qualifications`; // Reset heading if no qualifications
    }
}
