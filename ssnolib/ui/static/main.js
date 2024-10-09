

let counter = 1000;

function generateUniqueId(prefix = 'id') {
    counter += 1;
    return `${prefix}-${counter}`;
}


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




// Function to add new qualification fields with Bootstrap classes and delete button
function addTransformation() {
    const transformationContainer = document.getElementById('transformation-container');
    const newTransformationDiv = document.createElement('div');
    newTransformationDiv.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center', 'mb-2');

    const innerDiv = document.createElement('div');
    innerDiv.classList.add('w-100');

    const formRow = document.createElement('div');
    formRow.classList.add('form-row');

    const transformationID = generateUniqueId('transformation_name_field');

    const colMd3Name = document.createElement('div');
    colMd3Name.classList.add('col-md-3');
    const labelName = document.createElement('label');
    labelName.textContent = 'Name:';
    const inputName = document.createElement('input');
    inputName.type = 'text';
    inputName.id = transformationID;
    inputName.classList.add('form-control');
    inputName.name = 'transformation_name[]';
    inputName.required = true;
    inputName.oninput = function() { onTransformationNameChange(inputName.id, counter); };
    colMd3Name.appendChild(labelName);
    colMd3Name.appendChild(inputName);

    const colMd3AltersUnit = document.createElement('div');
    colMd3AltersUnit.classList.add('col-md-3');
    const labelAltersUnit = document.createElement('label');
    labelAltersUnit.textContent = 'Alters Unit:';

    const inputAltersUnit = document.createElement('input');
    inputAltersUnit.type = 'text';
    inputAltersUnit.id = generateUniqueId('transformation_alterUnit');
    inputAltersUnit.classList.add('form-control');
    inputAltersUnit.name = 'transformation_altersUnit[]';
    inputAltersUnit.oninput = function() { onChangeAltersUnit(inputAltersUnit.id, inputName.id); };
    inputAltersUnit.required = true;
    colMd3AltersUnit.appendChild(labelAltersUnit);
    colMd3AltersUnit.appendChild(inputAltersUnit);

    const colMd4Description = document.createElement('div');
    colMd4Description.classList.add('col-md-4');
    const labelDescription = document.createElement('label');
    labelDescription.textContent = 'Description:';
    const textareaDescription = document.createElement('textarea');
    textareaDescription.classList.add('form-control');
    textareaDescription.name = 'transformation_description[]';
    textareaDescription.rows = 3;
    textareaDescription.required = true;
    colMd4Description.appendChild(labelDescription);
    colMd4Description.appendChild(textareaDescription);

    formRow.appendChild(colMd3Name);
    formRow.appendChild(colMd3AltersUnit);
    formRow.appendChild(colMd4Description);

    const uniqueId = generateUniqueId('characters-container');

    const addButton = document.createElement('button');
    addButton.type = 'button';
    addButton.classList.add('btn', 'btn-secondary');
    addButton.textContent = 'Add Character';
    addButton.onclick = function() { addCharacter(uniqueId); };

    innerDiv.appendChild(formRow);
    innerDiv.appendChild(addButton);

    const colMd2Delete = document.createElement('div');
    colMd2Delete.classList.add('col-md-2', 'text-right', 'mt-2');
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('btn', 'btn-danger', 'mt-4');
    deleteButton.textContent = 'Delete Transformation';
    deleteButton.onclick = function() { deleteTransformation(deleteButton); };
    colMd2Delete.appendChild(deleteButton);

    newTransformationDiv.appendChild(innerDiv);
    newTransformationDiv.appendChild(colMd2Delete);

    transformationContainer.appendChild(newTransformationDiv);
    updateConfiguration();
}


function addCharacter(containerId){
    const characterContainer = document.getElementById(containerId);
    const newCharacterDiv = document.createElement('div');
    newCharacterDiv.classList.add('form-row');

    newCharacterDiv.innerHTML = `
    <div class="col-md-1">
        <label>Character:</label>
        <input type="text" class="form-control" name="transformation_character_character[]" required
               value="">
    </div>
    <div class="col-md-4">
        <label>associatedWith:</label>
        <select class="form-control qualification-dropdown" id="associatedWithDropdown" name="transformation_character_associatedWith[]">
            <option value="">Select an association</option>
            <option value="AnyStandardName" {% if character.associatedWith=='https://matthiasprobst.github.io/ssno#AnyStandardName' %}selected{% endif %}>Any Standard Name</option>
        </select>
    </div>
    <div class="col-md-4">
        <button type="button" class="btn btn-danger mt-4" onclick="deleteTransformation(this)">Delete Character
        </button>
    </div>
    `;
    characterContainer.appendChild(newCharacterDiv);
    updateConfiguration();
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
function deleteTransformation(button) {
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

    qualificationDropdowns.forEach(dropdown => {
        // Get the current selection:
        const selectedValue = dropdown.value;
        // Reset dropdown:
        dropdown.innerHTML = '<option value="" disabled selected>Select an Association</option>'; // Reset each dropdown
//        const option = document.createElement('option');
//        option.value = "AnyStandardName";
//        option.textContent = "Any Standard Name";
//        dropdown.appendChild(option);
        qualifications.forEach((qualification, index) => {
            const qualificationName = qualification.querySelector('input[name="qualification_name[]"]').value;
            const option = document.createElement('option');
            option.value = qualificationName
            option.textContent = qualificationName
            if (qualificationName === selectedValue) {
                option.selected = true; // Retain the selected option
            }

            dropdown.appendChild(option);
        });
    });
//    qualifications.forEach((qualification, index) => {
//        const name = qualification.querySelector('input[name="qualification_name[]"]')?.value;
//        console.log(qualificationDropdowns)
//        const selectedValue = dropdown.value;
//
//        // Add the qualifications as options, preserving the selection
//        configItems.forEach(qualificationName => {
//            const option = document.createElement('option');
//            option.value = name;
//            option.textContent = qualificationName;
//
//            if (qualificationName === selectedValue) {
//                option.selected = true; // Retain the selected option
//            }
//
//            dropdown.appendChild(option);
//        });
//    }
//    )

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

function getCapitalLetters(input) {
    return input.match(/[A-Z]/g) || [];
}

function onTransformationNameChange(parentElement, idx){
    const transformationName = document.getElementById(parentElement);
    console.log(transformationName.value);
    console.log(`index: ${idx}`);
    const capitalLetters = getCapitalLetters(transformationName.value);
    console.log(capitalLetters);

    // check if the character input fields exist
    // loop through the characters and update the associatedWith field
    capitalLetters.forEach(letter => {
        const characterRowID = `characters-row-${idx}-${letter}`;
        const foundID = document.getElementById(characterRowID)
        if (!foundID) {
            // Add the character input fields
            const characterContainer = document.getElementById(`characters-container-${idx}`);

            console.log(`Adding ${characterRowID}`);
            const newCharacterDiv = document.createElement('div');
            newCharacterDiv.classList.add('form-row');
            newCharacterDiv.id = characterRowID;

            const colmd1Div = document.createElement('div');
            colmd1Div.classList.add('col-md-1');
            const label = document.createElement('label');
            label.textContent = 'Character:';
            const input = document.createElement('input');
            input.type = 'text';
            input.id = `transformation_character_character-${idx}-${letter}`;
            input.classList.add('form-control');
            input.name = `transformation_character_character-${idx}[]`;
            input.required = true;
            input.disabled = true;
            input.value = letter;
            colmd1Div.appendChild(label);
            colmd1Div.appendChild(input);

            const colmd4Div = document.createElement('div');
            colmd4Div.classList.add('col-md-4');
            const labelAssociatedWith = document.createElement('label');
            labelAssociatedWith.textContent = 'associatedWith:';
            const selectAssociatedWith = document.createElement('select');
            selectAssociatedWith.classList.add('form-control', 'qualification-dropdown');
            selectAssociatedWith.id = 'associatedWithDropdown';
            selectAssociatedWith.name = `transformation_character_associatedWith-${idx}[]`;
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Select an association';
            selectAssociatedWith.appendChild(option);
            colmd4Div.appendChild(labelAssociatedWith);
            colmd4Div.appendChild(selectAssociatedWith);

            newCharacterDiv.appendChild(colmd1Div);
            newCharacterDiv.appendChild(colmd4Div);
            characterContainer.appendChild(newCharacterDiv);
        }
    });

    // loop over all letters from A...Z and check if they are in the transformation name
    // if they are not, delete the character input fields
    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        if (!capitalLetters.includes(letter)) {
            console.log(`Checking for ${letter} in ${capitalLetters}`);
            const foundID = document.getElementById(`characters-row-${idx}-${letter}`);
            if (foundID) {
                console.log(`Removing div ${foundID.id} for ${letter} because it is ${letter} not in ${capitalLetters}`);
                foundID.remove();
            }
        }
    }

}

function onChangeAltersUnit(alterUnitID, transformationNameID){
    console.log(`Updating ${alterUnitID}`);

    const altersUnit = document.getElementById(alterUnitID);
    console.log(altersUnit.value);
    const capitalLetters = getCapitalLetters(altersUnit.value);
    console.log(capitalLetters);

    // check if capital letters are in letters found in the name field:
    const transformationName = document.getElementById(transformationNameID);
    const expectedCapitalLetters = getCapitalLetters(transformationName.value);

    console.log(`Comparing ${capitalLetters} with ${expectedCapitalLetters}`);
    if (capitalLetters.length > 0){
        if (expectedCapitalLetters.length > 0){
            if (capitalLetters.length > expectedCapitalLetters.length){
                alert(`The letters in the "Alters Unit" field do not match the letters in the "Name" field. Please correct this.`);
                // Keep what is not a problem:
                            // Filter out non-matching letters
            const filteredValue = altersUnit.value.split('').filter(char => {
                return !/[A-Z]/.test(char) || expectedCapitalLetters.includes(char);
            }).join('');

            // Set the filtered value back to the input
            altersUnit.value = filteredValue;
            }
        }
    }

    const unmatchedLetters = [];

    capitalLetters.forEach(letter => {
        const regex = new RegExp(`\\[${letter}\\]`);
        if (!regex.test(altersUnit.value)) {
            unmatchedLetters.push(letter);
        }
    });

    if (unmatchedLetters.length > 0) {
        alert(`The following capital letters are not surrounded by square brackets: ${unmatchedLetters.join(', ')}`);
    }
}