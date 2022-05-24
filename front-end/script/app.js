'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(`${lanIP}`);
// Get
const getHistory = function () {
    
  const url = '/api/v1/history/';
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
    // let htmlString='';
    // for(let data of data){
    //     console.log(log)
    //     htmlString +=`  <td class="c-cell_second">Error</td>
                    // <td class="c-cell_second">Error</td>
                    // <td class="c-cell_second">Error</td>
                    // <td class="c-cell_second">Error</td>
                    // <td class="c-cell_second">Error</td>
                    // <td class="c-cell_second">Error</td>`;   
    
    // }
    // document.querySelector('.js-table').innerHTML=htmlString
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


const init = function () {
    // getHistory()
    listenToLockbuttons()
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});