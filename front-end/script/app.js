'use strict';

const lanIP = `http://${window.location.hostname}:5000`;
console.log(lanIP)
const socketio = io(`${lanIP}`);
// Get

// Show
const ShowAlcohol=function(alcohol){
  document.querySelector('js-alcoholpercentage').innerHTML=`${alcohol}`
}
const ShowTemperatuur=function(temperatuur){
  console.log(temperatuur)
  document.querySelector('.js-temperatuur').innerHTML=`<p class="c-temperatuur js-temperatuur">${temperatuur}°C</p>`
}

//Event listner
const listenToLockbuttons = function () {
  const buttons = document.querySelectorAll('.js-lock');
  for (const b of buttons) {
    b.addEventListener('click', function () {
      const locktime= b.getAttribute('data-locktime')
      console.log(`locktime: ${locktime}`)
      socketio.emit('F2B_locktime', locktime);
    });
  }
};


//Socketio
const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('B2F_connected', function (parameter) {
    console.log(`Het is ${parameter.temperatuur} °C`);
    ShowTemperatuur(parameter.temperatuur)
  });
  socketio.on('TempData', function (parameter) {
    ShowTemperatuur(parameter.temperatuur)
  });
  socketio.on('AlcoholData', function (parameter) {
    ShowAlcohol(parameter.alcohol)
  });
};


const init = function () {  
  listenToLockbuttons()
    listenToSocket();
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});