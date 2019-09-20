'use strict()';
function formatDate(date) {

    var dd = date.getDate();
    if (dd < 10) dd = '0' + dd;
  
    var mm = date.getMonth() + 1;
    if (mm < 10) mm = '0' + mm;
  
    var yyyy = date.getFullYear();
  
    return yyyy + '-' + mm + '-' + dd;
  }
window.addEventListener('DOMContentLoaded', function () {
    let now = new Date();
    let id = formatDate(now);
    console.log("Сегодня '"+id+"'");
    // window.location = "#today";
    let listok = document.getElementById(id);
    listok.setAttribute("bgcolor","LightYellow");
    window.location.hash=id;
});