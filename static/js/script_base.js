// Format result to display as a table in row child.
function format(CRN, Exam, Connection, Location, Textbook, Info, Seats, Special) {
    return '<div class="slider">'+
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
            '<tr>'+
                '<td width="25%">'+CRN+'</td>'+
                '<td width="25%">'+Exam+'</td>'+
                '<td width="25%">'+Location+'</td>'+
                '<td width="25%">'+Textbook+'</td>'+
            '</tr>'+
            '<tr>'+Info+'</tr>'+
            '<tr>'+Seats+'</tr>'+
            '<tr>'+Special+'</tr>'+
        '</table></div>';
}

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




