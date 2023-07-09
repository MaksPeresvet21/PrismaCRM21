const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => {
    return new bootstrap.Popover(popoverTriggerEl, {
      html: true
    });
  });

function OpenForm(formUrl) {
    $.ajax({
        url: formUrl,
        type: 'GET',
        success: function (response) {
            $('#form-dash').html(response);
            $('#form-dash input[type="text"]:first').focus();
        },
    });
}

$(document).ready(function() {
    $.ajax({
      url: '/get_ttn/',
      method: 'GET',
      success: function(response) {
        const ttnTotal = response.ttn_total;
        $('#ttn-total').text('+' + ttnTotal);
      },
      error: function(xhr, status, error) {
        console.error('Error while fetching ttn_total:', error);
      },
    });
});







