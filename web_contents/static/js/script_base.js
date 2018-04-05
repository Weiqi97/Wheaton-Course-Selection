// This function will alert user if they left select box empty.
function checkField() {
    var subjects = document.getElementById("subjects").value;
    var semester = document.getElementById("semester").value;
    if (subjects === "") {
        swal({
            type: "warning",
            title: "Please select subject(s)!",
            confirmButtonText: "Got it!"
        });
        return false;
    }
    else if (semester === "") {
        swal({
            type: "warning",
            title: "Please select a semester!",
            confirmButtonText: "Got it!"
        });
        return false;
    }
    else{
        return true;
    }
}
// language=JQuery-CSS

