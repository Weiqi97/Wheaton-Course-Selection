

// TODO: If possible make the alert box bigger with larger font.
// This function will alert user if they left select box empty.
function checkField() {
    // Get values of the subject select and semester select.
    var subjects = document.getElementById("subjects").value;
    var semester = document.getElementById("semester").value;

    // Check if subject was empty, if so alert with proper message.
    if (subjects === "") {
        swal( {
            type: "warning",
            title: "Please select subject(s)!",
            confirmButtonText: "Got it!"
        } );
        return false;
    }

    // Check if subject was empty, if so alert with proper message.
    else if (semester === "") {
        swal( {
            type: "warning",
            title: "Please select a semester!",
            confirmButtonText: "Got it!"
        } );
        return false;
    }
    else{
        return true;
    }
}

