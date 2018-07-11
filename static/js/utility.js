/**
 * The function to convert the form into json.
 * @returns {{string: string}}: the form converted to json.
 */
export function jsonifyForm() {
  const form = {};
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  });
  return form
}

/**
 * Send the ajax request.
 * @param {string} url: the url to post.
 * @param {{string: string}} form: the form data packed into an object.
 * @returns {jQuery.Ajax}: an jQuery Ajax object.
 */
export function sendAjaxRequest(url, form) {
  return $.ajax({
    url: url,
    type: 'POST',
    data: JSON.stringify(form),
    contentType: 'application/json; charset=utf-8'
  })
}

/**
 * Check if any subject was selected.
 */
export function checkSelectedSubjects() {
  // Get selected subjects from the drop down.
  const subjects = $('#subjects').val();
  // Check if no subject was selected.
  if (subjects.length === 0) {
    // Specify the alert details.
    $.confirm(
      {
        type: 'red',
        icon: 'fa fa-warning',
        theme: 'supervan',
        title: 'No subject selected!',
        content: `Please click on the subject(s) drop down and select at least one subject.`,
        buttons: {
          confirm: {
            text: 'Got it!',
            btnClass: 'btn-success'
          }
        }
      }
    )
  }
}