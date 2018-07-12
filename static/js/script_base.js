import * as utility from './utility.js'
import * as calendar from './calendar.js'
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
        $('.to-calendar').click(calendar.toCalendar);
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
  calendar.readyCalendar();
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