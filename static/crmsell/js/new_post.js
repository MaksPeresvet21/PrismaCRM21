const url = 'https://api.novaposhta.ua/v2.0/json/';
const apiKey = 'fc5584eb01a9ff27ea35f964fb94bc64';
let cities = [];
let citiesRef = [];

$(function() {
  $("#city_client").autocomplete({
    source: function(request, response) {
      const query = request.term.trim();
      if (query.length < 1) {
        return;
      }
      const payload = {
        apiKey: apiKey,
        modelName: 'Address',
        calledMethod: 'searchSettlements',
        methodProperties: {
          CityName: query,
          Limit: 10,
          Page: 1,
          SettlementTypeCode: 'своє',
        },
      };

      $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(payload),
        contentType: 'application/json',
        success: function(data) {
          const addresses = data.data[0].Addresses;
          cities = addresses.map(address => address.Present);
          citiesRef = addresses.map(address => address.Ref);
          response(cities);
        },
        error: function(error) {
          console.error(error);
        }
      });
    },
    minLength: 2,
    appendTo: "#form-dash"
  });

  $("#dep_np").autocomplete({
    source: function(request, response) {
      const query = request.term.trim();
      const cityIndex = cities.findIndex(city => city === $("#city_client").val());
      if (query.length < 1 || cityIndex < 0) {
        return;
      }
      const cityRef = citiesRef[cityIndex];

      const payload = {
        apiKey: apiKey,
        modelName: 'Address',
        calledMethod: 'getWarehouses',
        methodProperties: {
          SettlementRef: cityRef,
          FindByString: query
        },
      };

      $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify(payload),
        contentType: 'application/json',
        success: function(data) {
          const warehouses = data.data;
          const departments = warehouses.map(warehouse => warehouse.Description);
          response(departments);
        },
        error: function(error) {
          console.error(error);
        }
      });
    },
    minLength: 1,
    appendTo: "#form-dash"
  });
});