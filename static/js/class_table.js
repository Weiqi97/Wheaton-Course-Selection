/**
 * Convert HTML table to data table.
 * @param {string} table: HTML table that needs to be converted to data table.
 * @returns {void}: This function has no return.
 */
export function convertDataTable(table) {
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
      emptyTable: "Sorry, no class meets your expectation."
    },
    columnDefs: [
      {
        targets: 1,
        className: "text-center"
      },
      {
        targets: [6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        visible: false
      }
    ]
  });
}