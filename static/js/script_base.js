import * as utility from './utility.js'
import * as calendar from './calendar.js'
import * as classTable from './class_table.js'

/**
 * Get all class information.
 * @returns {void} This function has no return.
 */
function getClassTable () {
  // Send the ajax request.
  utility.sendAjaxRequest('/course_table', utility.jsonifyForm())
    .done( // If no errors.
      function (response) {
        const tableHolder = $('#course-container')
        tableHolder.html(response)
        classTable.convertDataTable(tableHolder.children())
        $('.to-calendar').click(function (event) {
          calendar.toCalendar(event)
        })
        $('.show-detail').click(function (event) {
          classTable.expandDataRow(event)
        })
      }
    )
    .fail( // If something went wrong.
      function () {
        $.alert({
          type: `red`,
          icon: 'fas fa-exclamation-triangle',
          theme: 'supervan',
          title: 'Error!',
          content: 'Something went wrong while getting the class information, please try again later.'
        })
      }
    )
}

/**
 * Run these functions when HTML finish loading.
 */
$(function () {
  // When document finishes loading, fill in default data.
  // Then get all classes by default.
  calendar.readyCalendar()
  utility.fillHiddenData()
  getClassTable()

  // When user clicks on submit.
  $('#submit').click(function () {
    // Get possible error when submitting.
    const error = utility.checkSelectedSubjects()
    if (error) {
      utility.subjectsError()
    } else {
      // Fill in users selection and refine classes.
      utility.fillHiddenData()
      getClassTable()
    }
  })
})
