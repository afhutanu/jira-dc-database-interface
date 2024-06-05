var searchTimeout;  // handle timeOut

function showForm(option) {
    var formHTML = '<input type="hidden" id="storedCreds" value="{{creds}}">'; 

    switch(option) {
        case 'search':
            formHTML += '<label for="searchInput">Search Username:</label>' +
                        '<input type="text" id="searchInput" class="form-control" oninput="handleInput()">' +
                        '<div id="searchResults" class="mt-2"></div>';
            break;
        case 'create_schema':
            formHTML += '<h4>Create New Schema</h4>' +
                        '<input type="text" id="schemaName" class="form-control" placeholder="Enter Schema Name">' +
                        '<button onclick="createSchema()" class="btn btn-primary mt-2">Create Schema</button>';
            break;
        case 'create_user':
            formHTML += '<h4>Create New Read User</h4>' +
                        '<input type="text" id="userName" class="form-control" placeholder="Username">' +
                        '<input type="text" id="schemaNameForUser" class="form-control mt-2" placeholder="Schema Name">' +
                        '<input type="password" id="userPassword" class="form-control mt-2" placeholder="Password">' +
                        '<button onclick="createUser()" class="btn btn-primary mt-2">Create User</button>';
            break;
        case 'add_to_schema':
            formHTML += '<h4>Add User to Schema</h4>' +
                        '<input type="text" id="schemaNameToAddUser" class="form-control" placeholder="Schema Name">' +
                        '<input type="text" id="userNameToAdd" class="form-control mt-2" placeholder="Username">' +
                        '<button onclick="addUserToSchema()" class="btn btn-primary mt-2">Add User</button>';
            break;
    }
    document.getElementById('form_area').innerHTML = formHTML;
}

function handleInput() {
    clearTimeout(searchTimeout);  // CLEAR
    searchTimeout = setTimeout(function() {
        performSearch(document.getElementById('searchInput').value);
    }, 1000);  // IF NO INPUT FOR 1 SECOND
}

function performSearch(searchTerm) {
    console.log("Triggered search with term: " + searchTerm); 
    var creds = document.getElementById('storedCreds').value;
    if(searchTerm.length >= 3) {
        $.ajax({
            url: '/api/search_user',
            type: 'GET',
            data: {'searchTerm': searchTerm, 'creds': creds},
            success: function(response) {
                document.getElementById('searchResults').innerHTML = response;
            }
        });
    }
}

function createSchema() {
    console.log("Sending data to create schema:", { schemaName, creds }); // Log data being sent

    var schemaName = document.getElementById('schemaName').value;
    var creds = document.getElementById('storedCreds').value; // Get stored credentials
    console.log("Creating schema: " + schemaName); // Check if function is called
    console.log("Credentials: " + creds); // Check if credentials are correct
    $.ajax({
        url: '/create_schema',
        type: 'POST',
        data: { 'schemaName': schemaName, 'creds': creds },
        success: function(response) {
            alert(response.message); // Assuming response is already parsed as JSON
        }
    });
}

function createUser() {
    var userName = document.getElementById('userName').value;
    var schemaName = document.getElementById('schemaNameForUser').value;
    var password = document.getElementById('userPassword').value;
    var creds = document.getElementById('storedCreds').value;  // Get stored credentials
    $.ajax({
        url: '/api/create_user',
        type: 'POST',
        data: { 'userName': userName, 'schemaName': schemaName, 'password': password, 'creds': creds },
        success: function(response) {
            alert(response.message);  // Assuming response is already parsed as JSON
        }
    });
}

function addUserToSchema() {
    var schemaName = document.getElementById('schemaNameToAddUser').value;
    var userName = document.getElementById('userNameToAdd').value;
    var creds = document.getElementById('storedCreds').value;  // Get stored credentials
    $.ajax({
        url: '/api/add_user_to_schema',
        type: 'POST',
        data: { 'schemaName': schemaName, 'userName': userName, 'creds': creds },
        success: function(response) {
            alert(response.message);  // Assuming response is already parsed as JSON
        }
    });
}