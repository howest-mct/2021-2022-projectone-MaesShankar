'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`${lanIP}`);

const getHistory = function () {
    
  const url = 'http://127.0.0.1:5000/api/v1/history/';
  handleData(url, fill_table);
};
const fill_table=function(jsonObject){
    console.log(jsonObject)
    // let htmlString='';
    // for(let data of data){
    //     console.log(log)
    //     htmlString += `
    //         <tr class="c-row js-header">
    //         <td class="c-cell">${log.date}</td>
    //         <td class="c-cell">${log.amount}ml</td>
    //         </tr>`;   
    
    // }
    // document.querySelector('.js-table').innerHTML=htmlString
}



const init = function () {
    getHistory()
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});