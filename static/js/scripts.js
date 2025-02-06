/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/

// close messages after 5s automatic...


document.addEventListener("DOMContentLoaded", function() {
    // Auto-dismiss messages after 5 seconds
    setTimeout(function() {
      let alerts = document.querySelectorAll('.alert');
      alerts.forEach((alert) => {
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      });
    }, 5000); // 5 seconds
  });