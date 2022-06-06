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
const getAlcHistory = function () {
  const url = lanIP + '/api/v1/alchistory/';
  console.log(url)
  handleData(url, fill_table_alc,error_get);
};
const getUsers = function () {
  const url = lanIP + '/api/v1/users/';
  console.log(url)
  handleData(url, fill_table_users,error_get);
};
// Show
const ShowAlcohol=function(alcohol){
  document.querySelector('js-alcoholpercentage').innerHTML=`${alcohol}`
}
const ShowTemperatuur=function(temperatuur){
  console.log(temperatuur)
  document.querySelector('.js-temperatuur').innerHTML=`<p class="c-temperatuur js-temperatuur">${temperatuur}°C</p>`
}


const error_get=function(){
  let htmlString=`  <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>`;   
  document.querySelector('.js-table-historiek').innerHTML=htmlString
}
const fill_table=function(jsonObject){
    // console.log(jsonObject)
    let htmlString=``;
    for(let data of jsonObject){
        // console.log(data)
        htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${data.HistoriekID}</td>
        <td class="c-cell_second">${data.DeviceID}</td>
        <td class="c-cell_second">${data.ActieID}</td>
        <td class="c-cell_second_special">${data.Datum}</td>
        <td class="c-cell_second">${data.Waarde}</td>;   
        <td class="c-cell_second">${data.Commentaar}</td>
      </tr>`;
    }
    document.querySelector('.js-table-historiek').innerHTML=htmlString
}
const fill_table_users=function(jsonObject){
    let htmlString=''
    for(let data of jsonObject){
      htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${data.UserID}</td>
        <td class="c-cell_second">${data.Naam}</td>
        <td class="c-cell_second">${data.Voornaam}</td>
      </tr>`
    }
    document.querySelector('.js-table-users').innerHTML=htmlString;
   
}
const fill_table_alc=function(jsonObject){
    console.log(jsonObject)
    let htmlString=``;
    for(let data of jsonObject){
        // console.log(data)
        htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${data.AlcHistoriekID}</td>
        <td class="c-cell_second">${data.UserID}</td>
        <td class="c-cell_second">${data.ADatum}</td>
        <td class="c-cell_second_special">${data.AWaarde}</td>
        </tr>`;
    }
    document.querySelector('.js-table-alc').innerHTML=htmlString
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
  socketio.on('AlcoholData', function (parameter) {
    ShowAlcohol(parameter.alcohol)
  });
};
const listenToTempSocket=function(){
  socketio.on('B2F_connected', function (parameter) {
    console.log(`Het is ${parameter.temperatuur} °C`);
    ShowTemperatuur(parameter.temperatuur)
  });
  socketio.on('TempData', function (parameter) {
    ShowTemperatuur(parameter.temperatuur)
  });
}



const init = function () {  
  const htmlDash=document.querySelector('.js-temperatuur')
  const htmlhistory=document.querySelector('.js-table-historiek')
  const htmlUser=document.querySelector('.js-table-users')
  const htmlalc=document.querySelector('.js-table-alc')
  if(htmlUser){
    getUsers()    
    listenToSocket();
  }
  if(htmlhistory){
    console.log('history')
    getHistory() ;  
    listenToSocket()
  }
  if(htmlDash){
    listenToLockbuttons()
    listenToTempSocket();
  }
  if(htmlalc){
    getAlcHistory()
    listenToSocket()
  }

};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});