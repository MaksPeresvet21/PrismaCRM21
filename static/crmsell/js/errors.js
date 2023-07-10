var formCheckInputs = document.querySelectorAll('.form-check-input');
formCheckInputs.forEach(function(input) {
    if (input.classList.contains('form-check-input')) {
        var wrapperDiv = document.createElement('div');
        wrapperDiv.classList.add('form-check', 'form-switch');
        input.parentNode.insertBefore(wrapperDiv, input);
        wrapperDiv.appendChild(input);
    }
});

$(document).on('submit', 'form', function(event) {
    event.preventDefault();
    var form = $(this);

    var formData = new FormData(form[0]);

    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                window.location.reload();
            } else {
                var errorMessage = response.errors;
                appendAlert(errorMessage, 'dark');
            }
        },
    });
});

const alertPlaceholder = document.getElementById('liveAlertPlaceholder');

const appendAlert = (message, type) => {
  const existingAlert = alertPlaceholder.querySelector('.alert'); // Проверка наличия уже отображаемого алерта

  if (!existingAlert) { // Показывать алерт только если его нет
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('');

    alertPlaceholder.append(wrapper);
  }
};

const alertTrigger = document.getElementById('liveAlertBtn');
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
  });
}