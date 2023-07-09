var deliveryFields = document.querySelectorAll("#delivery input[type='radio']");
var hiddenFields = document.querySelectorAll("#name_client, #phone_client, #city_client, #dep_np, #id_weight, #id_status, label[for='name_client'], label[for='phone_client'], label[for='city_client'], label[for='dep_np'], label[for='id_weight'], label[for='id_status']");

hiddenFields.forEach(function(field) {
  field.style.display = "none";
});

deliveryFields.forEach(function(deliveryField) {
  deliveryField.addEventListener("change", function() {
    if (this.value == "NP") {
      hiddenFields.forEach(function(field) {
        field.style.display = "block";
      });
    } else {
      hiddenFields.forEach(function(field) {
        field.style.display = "none";
      });
    }
  });
});









