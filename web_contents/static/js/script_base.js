// Global constants
var height_adjust = 200; // Adjust the table size.


// Function to resize data table every time browser size changes.
$(function() {
    $(window).on("resize", resize_result_table);
} );

function resize_result_table() {
    // Get the new proper window height.
    var window_height = window.innerHeight-height_adjust;

    // Reinitialize data table to a proper size.
    $('#result_table').DataTable( {
        "destroy":        true,
        "scrollY":        window_height,
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

// A helper function for replace all.
function replaceAll(str, find, replace) {
    return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}
