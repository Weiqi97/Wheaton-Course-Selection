export function convertDataTable(table) {
  table.DataTable({
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
    columnDefs: [{
      targets: [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
      visible: false
    }]
  });
}