// Global constants
var height_adjust = 200; // Adjust the table size.

// When browser size changed, find proper size of new data table.
function resize_result_table() {
    // Get the new proper window height.
    var window_height = window.innerHeight-height_adjust;

    // Reinitialize data table to a proper size.
    $('#result_table').DataTable( {
        "destroy":        true,
        "scrollY":        800,
        "scrollX":        true,
        "scrollCollapse": true,
        "paging":         false,
        "bInfo" :         false,
        "columnDefs": [
            {
                "targets": [6, 7, 8, 9, 10, 11, 12, 13, 14],
                "visible": false
            }
        ]
    } );
}

// Format result to display as a table in row child.
function format(CRN, Exam, Connection, Location, Textbook, Info, Seats, Special) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td width="25%">'+CRN+'</td>'+
            '<td width="25%">'+Exam+'</td>'+
            '<td width="25%">'+Location+'</td>'+
            '<td width="25%">'+Textbook+'</td>'+
        '</tr>'+
        '<tr>'+Info+'</tr>'+
        '<tr>'+Seats+'</tr>'+
        '<tr>'+Special+'</tr>'+
        '</table>';
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

