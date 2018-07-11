/**
 * The function to convert the form into json.
 * @returns {{string: string}}: the form converted to json.
 */
export function jsonifyForm () {
  const form = {}
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  })
  return form
}

/**
 * Send the ajax request.
 * @param {string} url: the url to post.
 * @param {{string: string}} form: the form data packed into an object.
 * @returns {jQuery.Ajax}: an jQuery Ajax object.
 */
export function sendAjaxRequest (url, form) {
  return $.ajax({
    type: 'POST',
    url: url,
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(form)
  })
}

/**
 * the function to submit form via ajax in dendrogram
 * @returns {void} - nothing is returned from this function.
 */
function generateDendrogram () {
  // show loading icon
  $('#status-analyze').css({'visibility': 'visible'})

  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/dendrogramDiv', form)
    .done(
      function (response) {
        $('#dendrogram-result').html(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('error encountered while plotting the dendrogram.')
      })
    .always(
      function () {
        $('#status-analyze').css({'visibility': 'hidden'})
      })
}