import * as utility from './utility.js'
import * as calendar from './calendar.js'
import * as classTable from './class_table.js'

/**
 * This function formats the given information as a table in row child.
 * @param {Array.<string>} rowData: list of data from the row.
 * @returns {string}
 */
function format(rowData) {
  // Format some information ahead of time.
  const exam = rowData[9] === '' ? '' : `Exam: ${rowData[9]}`;
  const area = rowData[12] === '' ? '<td></td>' : `<td>Area: ${rowData[12]}</td>`;
  const division = rowData[11] === '' ? '<td></td>' : `<td>Division: ${rowData[11]}</td>`;
  const foundation = rowData[10] === '' ? '<td></td>' : `<td>Foundation: ${rowData[10]}</td>`;
  const connection = rowData[13] === '' ? '<td></td>' : `<td>Connection: ${rowData[13]}</td>`;
  //TODO: formatting needs much more work.
  return `
      <div class="slider">
          <table cellpadding="0" cellspacing="0" border="0">
              <tr>
                  <td width="25%">CRN: ${rowData[6]}</td>
                  <td width="25%">${exam}</td>
                  <td width="25%">Location: ${rowData[7]}</td>
                  <td width="25%">Textbook: ${rowData[15]}</td>
              </tr>
              <tr>
                  ${area}${division}${foundation}${connection}
              </tr>
              <tr>
                  <td colspan="4">${rowData[14]}</td>
              </tr>
              <tr>
                  <td colspan="4">Note: ${rowData[16]}</td>
              </tr>
          </table>
      </div>`
}

function expandDataRow() {
  // Get the data table selector.
  const courseTable = $('#course-table');
  // Get the data table object.
  const dataTable = courseTable.DataTable();
  // Get the jQuery table object.
  const jQueryTable = courseTable.dataTable();
  // Find the closest tr.
  const tr = $(event.currentTarget).closest('tr');
  // Format the row data.
  const formattedRow = format(jQueryTable.fnGetData(tr));
  // Get the data table row.
  const row = dataTable.row(tr);

  // Check if row child is shown. If it is, hide it.
  if (row.child.isShown()) {
    $('div.slider', row.child()).slideUp(function () {
      row.child.hide();
      tr.removeClass("shown");
    });
  } else {
    // If not shown, display it.
    row.child(formattedRow, "no-padding").show();
    tr.addClass("shown");
    $('div.slider', row.child()).slideDown();
  }
}

/**
 * Get all class information.
 * @returns {void}: This function has no return.
 */
function getClassTable() {
  // Send the ajax request.
  utility.sendAjaxRequest('/course_table', utility.jsonifyForm())
    .done( // If no errors.
      function (response) {
        const tableHolder = $('#course-container');
        tableHolder.html(response);
        classTable.convertDataTable(tableHolder.children());
        $('.to-calendar').click(calendar.toCalendar);
        $('.show-detail').click(expandDataRow)
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