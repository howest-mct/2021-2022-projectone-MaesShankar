'use strict';

const lanIP = `http://${window.location.hostname}:5000`;
console.log(lanIP)
const socketio = io(`${lanIP}`);
let radioid=0
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
  document.querySelector('.js-alcohol').innerHTML=`<p class="c-temperatuur js-alcoholpercentage">${alcohol}%</p>`
}
const ShowTemperatuur=function(temperatuur){
  console.log(temperatuur)
  document.querySelector('.js-temperatuur').innerHTML=`<p class="c-temperatuur js-temperatuur">${temperatuur}°C</p>`
}
const showSluiting=function(locktime,id){
  let htmlid=``
  if(id==933210265772){
    htmlid=`Shankar`
  }else if(id==453047185099){
    htmlid=`Willy`
  }else{
    htmlid=`JP`
  }
  
  let htmlSluit=``
  htmlSluit=`<p class="c-temperatuur js-sluiting">${locktime} s</p>`
  document.querySelector('.js-sluiting').innerHTML=htmlSluit
  document.querySelector('.js-idsluit').innerHTML=htmlid
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
    let actie=''
    let device=''
    for(let data of jsonObject){
        // console.log(data)
        if(data.ActieID==1){
          actie='Relais'
        }else if(data.ActieID==2){
          actie='LCD'
        }else{
          actie='No Action'
        }

        if(data.DeviceID==1){
          device='Alcohol MQ-3'
        }else if(data.DeviceID==2){
          device='Temperatuursensor'
        }

        htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${device}</td>
        <td class="c-cell_second">${actie}</td>
        <td class="c-cell_second_special">${data.Datum}</td>
        <td class="c-cell_second">${data.Waarde}</td>;   
        <td class="c-cell_second">${data.Commentaar}</td>
      </tr>`;
    }
    document.querySelector('.js-table-historiek').innerHTML=htmlString
}
const fill_table_users=function(jsonObject){
  // console.log(jsonObject)
    let htmlString=''
    let access=''
    for(let data of jsonObject){
      if(data.Toegang==1){
        access='Yes'
      }else{
        access='No'
      }
      htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${data.UserID}</td>
        <td class="c-cell_second">${data.Naam}</td>
        <td class="c-cell_second">${data.Voornaam}</td>
        <td class="c-cell_second">${data.RFID}</td>
        <td class="c-cell_second">${access}</td>

      </tr>`
    }
    document.querySelector('.js-table-users').innerHTML=htmlString;
   
}
const fill_table_alc=function(jsonObject){
    console.log(jsonObject)
    let htmlString=``;
    let user=''
    for(let data of jsonObject){
       for(let data of jsonObject){
        // console.log(data)
        if(data.UserID==1){
          user='Shankar'
        }else if(data.UserID==2){
          user='Willy'
        }else{
          user='JP'
        }
        // console.log(data)
        htmlString +=` <tr class="c-row u-table o-layout__item o-layout--gutter-lg">
        <td class="c-cell_second">${user}</td>
        <td class="c-cell_second">${data.ADatum}</td>
        <td class="c-cell_second_special">${data.AWaarde}%</td>
      
        </tr>`;
    }
    document.querySelector('.js-table-alc').innerHTML=htmlString
}
}
//Event listner
const listenToLockbuttons = function () {
  const buttons = document.querySelectorAll('.js-lock');
  for(const radiobutton of document.querySelectorAll('input[name="id"]')){
        radiobutton.addEventListener('click',function(){
          if(radiobutton.checked){
            radioid=radiobutton.getAttribute('value')
          console.log(radioid)
          }
        });
      }
  for (const b of buttons) {
    b.addEventListener('click', function () {
      const locktime= b.getAttribute('data-locktime')       
      console.log(`locktime: ${locktime}`)
      // showSluiting(locktime,radioid)
      // console.log(`time ${locktime} id ${radioid}`)
      socketio.emit('F2B_locktime', locktime,radioid);
    });
  }
};


//Socketio
const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
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
  socketio.on('AlcoholData', function (parameter) {
    console.log(parameter.alcohol)
    ShowAlcohol(parameter.alcohol)
  });
  socketio.on('Sluiting', function (parameter) {
    console.log(parameter.time)
    showSluiting(parameter.time,parameter.id)
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