'use strict';

const lanIP = `http://${window.location.hostname}:5000`;
console.log(lanIP)
const socketio = io(`${lanIP}`);
// Get
const getHistory = function () {
    
  const url = lanIP + '/api/v1/history/';
  console.log(url)
  handleData(url, fill_table,error_get);
};

// Show
const error_get=function(){
  let htmlString=`  <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>`;   
  document.querySelector('.js-table').innerHTML=htmlString
}
const fill_table=function(jsonObject){
    console.log(jsonObject)
    let htmlString=`<tr class="c-row o-layout__item o-layout--gutter-lg">
                            <th class="c-cell">HistoriekID</th>
                            <th class="c-cell">DeviceID</th>
                            <th class="c-cell">ActieID</th>
                            <th class="c-cell">Datum</th>
                            <th class="c-cell">Waarde</th>
                            <th class="c-cell">Commentaar</th>
                      </tr>`;
    for(let data of jsonObject){
        console.log(data)
        htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${data.HistoriekID}</td>
        <td class="c-cell_second">${data.DeviceID}</td>
        <td class="c-cell_second">${data.ActieID}</td>
        <td class="c-cell_second_special">${data.Datum}</td>
        <td class="c-cell_second">${data.Waarde}</td>;   
        <td class="c-cell_second">${data.Commentaar}</td>
      </tr>`
    }
    document.querySelector('.js-table').innerHTML=htmlString
    listenToLockbuttons()
}

//Event listner
const listenToLockbuttons = function () {
  const buttons = document.querySelectorAll('.js-lock');
  for (const b of buttons) {
    b.addEventListener('click', function () {
      const locktime= b.getAttribute('data-locktime')
      console.log(`locktime: ${locktime}`)
    });
  }
};

const ShowTemperatuur=function(temperatuur){
  console.log(temperatuur)
  document.querySelector('.js-temperatuur').innerHTML=`<p class="c-temperatuur js-temperatuur">${temperatuur}°C</p>`
}

//Socketio
const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });

  socketio.on('B2F_connected', function (parameter) {
    console.log(`Het is ${parameter.temperatuur} °C`);
    ShowTemperatuur(parameter.temperatuur)
    socketio.emit('AskTemp');
  });
  socketio.on('TempData', function (parameter) {
    ShowTemperatuur(parameter.temperatuur)
    socketio.emit('AskTemp');
  });
};


const init = function () {
    getHistory()
    listenToSocket();
    
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});