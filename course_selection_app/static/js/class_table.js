/**
 * This function formats the given information as a table in row child.
 * @param {Array.<string>} rowData - List of data from the row.
 * @returns {string} - The formatted row data in a div.
 */
function format (rowData) {
  // Format some information ahead of time.
  const exam = rowData[9] === '' ? '' : `Exam: ${rowData[9]}`
  const area = rowData[12] === '' ? '<td></td>' : `<td>Area: ${rowData[12]}</td>`
  const division = rowData[11] === '' ? '<td></td>' : `<td>Division: ${rowData[11]}</td>`
  const foundation = rowData[10] === '' ? '<td></td>' : `<td>Foundation: ${rowData[10]}</td>`
  const connection = rowData[13] === '' ? '<td></td>' : `<td>Connection: ${rowData[13]}</td>`
  // TODO: formatting needs much more work.
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

/**
 * Convert HTML table to data table.
 * @param {string} table - HTML table that needs to be converted to data table.
 * @returns {void} - This function has no return.
 */
export function convertDataTable (table) {
  // Convert input HTML table to data table.
  table.dataTable({
    bInfo: false,
    bSort: false,
    paging: false,
    scrollY: 700,
    scrollX: true,
    scrollCollapse: true,
    sDom: 'l<"toolbar">frtip',
    language: {
      emptyTable: 'Sorry, no class meets your expectation.'
    },
    columnDefs: [
      {
        targets: 1,
        className: 'text-center'
      },
      {
        targets: [6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        visible: false
      }
    ]
  })
}

/**
 * This function sets expand data row when click.
 * @param {Object} event - The event object that was clicked.
 * @returns {void} - This function has no return.
 */
export function expandDataRow (event) {
  // Get the data table selector.
  const courseTable = $('#course-table')
  // Get the data table object.
  const dataTable = courseTable.DataTable()
  // Get the jQuery table object.
  const jQueryTable = courseTable.dataTable()
  // Find the closest tr.
  const tr = $(event.currentTarget).closest('tr')
  // Format the row data.
  const formattedRow = format(jQueryTable.fnGetData(tr))
  // Get the data table row.
  const row = dataTable.row(tr)

  // Check if row child is shown. If it is, hide it.
  if (row.child.isShown()) {
    $('div.slider', row.child()).slideUp(function () {
      row.child.hide()
      tr.removeClass('shown')
    })
    $(event.currentTarget).html(`<i class="fas fa-angle-down fa-lg" style="color: #EE6551"></i>`)
  } else {
    // If not shown, display it.
    row.child(formattedRow, 'no-padding').show()
    tr.addClass('shown')
    $('div.slider', row.child()).slideDown()
    $(event.currentTarget).html(`<i class="fas fa-angle-up fa-lg" style="color: darkcyan;"></i>`)
  }
}
