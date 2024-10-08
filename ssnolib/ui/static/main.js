
// Function to add new author fields with Bootstrap classes and "Delete" button at the end of the row
function addAuthor() {
    const authorContainer = document.getElementById('author-and-organization-container');
    const newAuthorDiv = document.createElement('div');
    newAuthorDiv.classList.add('form-row', 'align-items-center', 'mb-2');

    newAuthorDiv.innerHTML = `
        <div class="col-md">
            <label>First Name:</label>
            <input type="text" class="form-control" name="person.firstName[]" required>
        </div>
        <div class="col-md">
            <label>Last Name:</label>
            <input type="text" class="form-control" name="person.lastName[]">
        </div>
        <div class="col-md">
            <label>ORCID ID:</label>
            <input type="text" class="form-control" name="person.orcidId[]" required>
        </div>
        <div class="col-md">
            <label>Role:</label>
            <select class="form-control" name="person.hadRole[]">
                <option value="" selected>Select a role</option>
                <option value="ContactPerson">Contact Person</option>
                <option value="DataCollector">Data Collector</option>
                <option value="DataCurator">Data Curator</option>
                <option value="DataManager">Data Manager</option>
                <option value="Distributor">Distributor</option>
                <option value="Editor">Editor</option>
                <option value="Other">Other</option>
                <option value="Producer">Producer</option>
                <option value="ProjectLeader">Project Leader</option>
                <option value="ProjectManager">Project Manager</option>
                <option value="ProjectMember">Project Member</option>
                <option value="RelatedPerson">Related Person</option>
                <option value="Researcher">Researcher</option>
                <option value="RightsHolder">Rights Holder</option>
                <option value="Sponsor">Sponsor</option>
                <option value="Supervisor">Supervisor</option>
                <option value="WorkPackageLeader">Workpackage Leader</option>
                <!-- Add more roles as needed -->
            </select>
        </div>
        <div class="col-md">
            <label>Email:</label>
            <input type="email" class="form-control" name="person.mbox[]">
        </div>
        <div class="col-md-1 text-right mt-2">
            <button type="button" class="btn btn-danger" onclick="deleteAuthor(this)">Delete Author</button>
        </div>
    `;
    authorContainer.appendChild(newAuthorDiv);
}

// Function to add new organization fields with Bootstrap classes and "Delete" button at the end of the row
function addOrganization() {
    const organizationContainer = document.getElementById('author-and-organization-container');
    const newOrganizationDiv = document.createElement('div');
    newOrganizationDiv.classList.add('form-row', 'align-items-center', 'mb-2');

    newOrganizationDiv.innerHTML = `
        <div class="col-md">
            <label>Name:</label>
            <input type="text" class="form-control" name="organization.name[]" required>
        </div>
        <div class="col-md">
            <label>URL:</label>
            <input type="url" class="form-control" name="organization.url[]">
        </div>
        <div class="col-md">
            <label>ROR ID:</label>
            <input type="text" class="form-control" name="organization.hasRorId[]">
        </div>
        <div class="col-md">
            <label>Role:</label>
            <select class="form-control" name="organization.hadRole[]">
                <option value="" selected>Select a role</option>
                <option value="HostingInstitution">Hosting Institution</option>
                <option value="RegistrationAgency">Data Collector</option>
                <option value="RegistrationAuthority">Registration Authority</option>
                <option value="ResearchGroup">Research Group</option>
            </select>
        </div>
        <div class="col-md">
            <label>Email:</label>
            <input type="email" class="form-control" name="organization.mbox[]">
        </div>
        <div class="col-md-1 text-right mt-2">
            <button type="button" class="btn btn-danger" onclick="deleteOrganization(this)">Delete Organization</button>
        </div>
    `;
    organizationContainer.appendChild(newOrganizationDiv);
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

// Function to delete an author row
function deleteOrganization(button) {
    const orgaRow = button.parentNode.parentNode;
    orgaRow.remove();
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
                    <label>Preposition (optional):</label>
                    <input type="text" class="form-control" name="preposition[]" placeholder='E.g. "at", "assuming", ...'>
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
    const qualificationDropdowns = document.querySelectorAll('.qualification-dropdown');

        // Reset each dropdown
    qualificationDropdowns.forEach(dropdown => {
        dropdown.innerHTML = '<option value="" disabled selected>Select a Qualification</option>'; // Reset each dropdown
    });

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

    console.log('---')
    qualifications.forEach((qualification, index) => {
        const name = qualification.querySelector('input[name="qualification_name[]"]')?.value;
        console.log(qualificationDropdowns)

        // Add qualification to all dropdowns
        qualificationDropdowns.forEach(dropdown => {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            dropdown.appendChild(option);
        });
    }
    )

    let configurationString = ''; // Initialize configuration string
    // Adding "AnyStandardName" at the end or dynamically based on the positions
    if (configItems.length > 0) {
        configItems.forEach((item, index) => {
            if (item === "AnyStandardName") {
                configurationString += "AnyStandardName"; // Append first item
            } else {
                if (item != '') {
                    configurationString += ` [${item}] `; // Append item
                }
            }
        });

        // Update the heading with the configuration
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
