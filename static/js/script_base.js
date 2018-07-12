import * as utility from './utility.js'
import * as classTable from './class_table.js'

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
 * Convert time to proper format to display.
 * @param time {string} the refined time.
 * @returns {string} time in format of "HH:MM:SS"
 */
function timeConverter(time) {
  if (time.includes('A')) {
    if (time[2] === ':')
      return `${time.slice(0, 5)}:00`;
    else
      return `0${time.slice(0, 4)}:00`;
  }
  else {
    if (Number(time.slice(0, 2)) !== 12) {
      return `${Number(time.slice(0, 1)) + 12}${time.slice(1, 4)}:00`;
    }
    return `${time.slice(0, 5)}:00`;
  }
}


/**
 * Convert day to proper format to display
 * @param day {string} the refined day.
 * @returns {string} The corresponding date.
 */
function dayConverter(day) {
  if (day === 'M') {
    return '2018-04-02T';
  } else if (day === 'T') {
    return '2018-04-03T';
  } else if (day === 'W') {
    return '2018-04-04T';
  } else if (day === 'R') {
    return '2018-04-05T';
  } else if (day === 'F') {
    return '2018-04-06T'
  }
}

//
// /**
//  * Display the data table while hiding the row child.
//  */
// $(function dataTableReady() {
//   var data_table = $("#result_table");
//
//   // Initialize data table.
//   var table = data_table.DataTable({
//     "scrollY": 643,
//     "scrollX": true,
//     "scrollCollapse": true,
//     "paging": false,
//     "bSort": false,
//     "bInfo": false,
//     "sDom": 'l<"toolbar">frtip',
//     "language": {
//       "emptyTable": "No class meets your expectation."
//     },
//     "columnDefs": [{
//       "targets": [6, 7, 8, 9, 10, 11, 12, 13, 14],
//       "visible": false
//     }]
//   });
//
//   // Get proper data for row child.
//   data_table.find("tbody").on("click", "#show_detail", function () {
//     // Set variables for row child display method.
//     var tr = $(this).closest("tr");
//     var row = table.row(tr);
//     // Get all the data from table row.
//     var CRN = table.row(this).data()[6];
//     var Exam = table.row(this).data()[7];
//     var Connection = table.row(this).data()[8];
//     var Location = table.row(this).data()[9];
//     var Textbook = table.row(this).data()[10];
//     var Info = table.row(this).data()[11];
//     var Seats = table.row(this).data()[12];
//     var Special = table.row(this).data()[13];
//
//     // TODO: UGLY. Seeking for fixing method afterwards.
//     // Refine info strings and add connection to it.
//     Info = Info.replace(/_/g, "<td>");
//     Info = Info.replace(/!/g, "</td>");
//     if (Connection !== "")
//       Info = Info + "<td>" + Connection + "</td>";
//
//     // Refine seats string.
//     Seats = Seats.replace(/_/g, "<td>");
//     Seats = Seats.replace(/!/g, "</td>");
//
//     // Refine special info string.
//     Special = Special.replace(/_/g, '<td colspan="4"><div>');
//     Special = Special.replace(/!/g, '</td>');
//
//     // This row is already open - close it.
//     if (row.child.isShown()) {
//       $("div.slider", row.child()).slideUp(function () {
//         row.child.hide();
//         tr.removeClass("shown");
//       });
//     }
//     // Open this row.
//     else {
//       row.child(format(CRN, Exam, Connection, Location, Textbook,
//         Info, Seats, Special), "no-padding").show();
//       tr.addClass("shown");
//       $('div.slider', row.child()).slideDown();
//     }
//   });
// });
//
/**
 * Display the empty calendar.
 */
$(function readyCalendar() {
  // --------- Calendar ---------
  $("#calendar").fullCalendar({
    height: 740,
    header: {left: "", center: "", right: ""},
    // Display just full length of weekday, without dates.
    columnFormat: 'dddd',
    defaultView: 'agendaWeek',
    hiddenDays: [0, 6],    // hide Saturday and Sunday
    weekNumbers: false,  // don't show week numbers
    minTime: '8:00:00',   // display from 8 to 22
    maxTime: '23:00:00',
    slotDuration: '00:30:00', // 15 minutes for each row
    allDaySlot: false,        // don't show "all day" at the top
    editable: true,
    defaultDate: moment('2018-04-02'),
    eventStartEditable: false,
    eventDurationEditable: false,

    // Delete events on click.
    eventRender: function (event, element) {
      element.find(".fc-bg").css("pointer-events", "none");
      element.append(
        `<div style='position: absolute; bottom: 1px; right: 2px'>
             <span id='deleteEvent'>
                 <i  class='fas fa-trash-alt fa-lg' style='color: orangered'></i>
             </span>
         </div>`
      );
      element.find("#deleteEvent").click(function () {
        $('#calendar').fullCalendar('removeEvents', event._id);
      });
    }

  });
});


/**
 * Add class from data table to calendar.
 * @returns {void}: This function has no return.
 */
function toCalendar() {
  // Get the row with the add button clicked.
  const clickedRow = $(event.currentTarget).closest('tr');
  // Get the data within the row.
  const rowData = $('#course-table').dataTable().fnGetData(clickedRow);
  // Unpack data from the row, we need title and time only.
  const courseTitle = rowData[4];
  const courseTime = rowData[5];

  // Check if the class has an assigned time.
  if (courseTime === "TBA") {
    utility.classTimeTBAError()
  } else {
    // Split times. It is possible that one class has two different times.
    const timeList = courseTime.split("<br>");
    // Use a map function to fill all class times in the calendar.
    timeList.map(function (time) {
      const days = time.replace(/AM|PM|[0-9]|-|:|\s/g, '').split('');
      const startEndTime = time.replace(/[MTWRF]|\s/g, '').split('-');
      for (let day of days) {
        const newEvent = {
          id: courseTitle,
          title: courseTitle,
          start: dayConverter(day) + timeConverter(startEndTime[0]),
          end: dayConverter(day) + timeConverter(startEndTime[1]),
          allDay: false
        };
        $("#calendar").fullCalendar('renderEvent', newEvent, 'stick');
      }
    });
  }
}

/**
 * Get all class information.
 * @returns {void}: This function has no return.
 */
function getClassTable() {
  // Send the ajax request.
  utility.sendAjaxRequest('/all_class', utility.jsonifyForm())
    .done( // If no errors.
      function (response) {
        const tableHolder = $('#course-container');
        tableHolder.html(response);
        classTable.convertDataTable(tableHolder.children());
        $('.to-calendar').click(toCalendar);
      }
    )
    .fail( // If something went wrong.
      function () {
        $.alert({
          type: `red`,
          icon: 'fa fa-warning',
          theme: 'modern',
          title: 'Error!',
          content: 'Something went wrong while getting the class information, please try again later.'
        })
      }
    )
}


/**
 * Fill user's selection into a hidden form for back end.
 * @returns {void}: This function has no return.
 */
function fillHiddenData() {
  $('#area-value').val($('#area').val());
  $('#division-value').val($('#division').val());
  $('#semester-value').val($('#semester').val());
  $('#subjects-value').val($('#subjects').val());
  $('#foundation-value').val($('#foundation').val());
}

/**
 * Run these functions when HTML finish loading.
 */
$(function () {
  // When document finishes loading, fill in default data.
  // Then get all classes by default.
  fillHiddenData();
  getClassTable();

  // When user clicks on submit.
  $('#submit').click(function () {
    // Get possible error when submitting.
    const error = utility.checkSelectedSubjects();
    if (error) {
      utility.subjectsError();
    } else {
      // Fill in users selection and refine classes.
      fillHiddenData();
      getClassTable();
    }
  })
});