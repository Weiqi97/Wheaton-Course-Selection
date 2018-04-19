/**
 * This function formats the given information as a table in row child.
 * @param CRN {string} - The refined CRN number
 * @param Exam {string} - Exam time.
 * @param Connection {string} - Connection.
 * @param Location {string} - Class location.
 * @param Textbook {string} - Textbook with its link.
 * @param Info {string} - Foundation, division, area.
 * @param Seats {string} - Seats info.
 * @param Special {string} - Special info.
 * @returns {string}
 */
function format(CRN, Exam, Connection, Location, Textbook, Info, Seats, Special) {
    // TODO: use `text ${var}` to get element. (string literal)
    return '<div class="slider">' +
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
            '<td width="25%">' + CRN + '</td>' +
            '<td width="25%">' + Exam + '</td>' +
            '<td width="25%">' + Location + '</td>' +
            '<td width="25%">' + Textbook + '</td>' +
        '</tr>' +
        '<tr>' + Info + '</tr>' +
        '<tr>' + Seats + '</tr>' +
        '<tr>' + Special + '</tr>' +
        '</table></div>';
}

/**
 * This function will alert user if they left select box empty.
 * @returns {boolean} to onclick.
 */
function checkField() {
    // TODO: If possible make the alert box bigger with larger font.
    // Check if subject was empty, if so alert with proper message.
    var subject = $("#subjects").val();
    console.log(subject);
    if ($("#subjects").val().length === 0) {
        swal({
            type: 'warning',
            title: 'Please select subject(s)!',
            confirmButtonText: 'Got it!'
        });
        return false;
    }

    // Check if subject was empty, if so alert with proper message.
    else if ($('#semester').val()) {
        swal({
            type: 'warning',
            title: 'Please select a semester!',
            confirmButtonText: 'Got it!'
        });
        return false;
    }
    else {
        return true;
    }
}

/**
 * Convert time to proper format to display.
 * @param time {string} the refined time.
 * @returns {string} time in format of "HH:MM:SS"
 */
function timeConverter(time) {
    if (time.includes('A')) {
        if (time[2] === ':')
            return time.slice(0, 5) + ':00';
        else
            return '0' + time.slice(0, 4) + ':00';
    }
    else {
        if (Number(time.slice(0, 2)) !== 12) {
            return String(Number(time.slice(0, 1)) + 12) + time.slice(1, 4) + ':00';
        }
        return time.slice(0, 5) + ':00';
    }
}

/**
 * Convert day to proper format to display
 * @param day {string} the refined day.
 * @returns {string} The corresponding date.
 */
function dayConverter(day) {
    if (day === 'M') return '2018-04-02T';
    else if (day === 'T') return '2018-04-03T';
    else if (day === 'W') return '2018-04-04T';
    else if (day === 'R') return '2018-04-05T';
    else if (day === 'F') return '2018-04-06T'
}
