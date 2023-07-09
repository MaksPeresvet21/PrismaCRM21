const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => {
    return new bootstrap.Popover(popoverTriggerEl, {
      html: true
    });
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function createTTNbutton(orderId) {
  const csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/create_ttn/',
    method: "POST",
    headers: {
    'X-CSRFToken': csrftoken
    },
    data: {
      order_id: orderId,
    },
    success: function (response) {
      window.location.href = window.location.href;

    },
    error: function (xhr, status, error) {
      const errorMessage = xhr.responseText;
      console.log("Произошла ошибка при отправке запроса");
    },
  });
}

function updateStatusOnLoad() {
  const csrftoken = getCookie('csrftoken');
  $.ajax({
    url: '/update_status/',
    method: "POST",
    headers: {
    'X-CSRFToken': csrftoken
    },
    success: function(response) {
      if (response.success) {
        // Обновление статуса заказа на странице
        console.log("Статус успешно обновлен:", response.status);
      } else {
        console.log("Не удалось обновить статус заказа");
      }
    },
    error: function(xhr, status, error) {
      console.log("Произошла ошибка при отправке запроса");
    }
  });
}

$(document).ready(function() {
  updateStatusOnLoad();
  setInterval(updateStatusOnLoad, 900000);
});








