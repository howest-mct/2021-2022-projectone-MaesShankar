const lanIP = `http://${window.location.hostname}:5000`;
console.log(lanIP)
const socketio = io(`${lanIP}`);


const getUsers = function () {
  const url = lanIP + '/api/v1/users/';
  console.log(url)
  handleData(url, fill_table_users,error_get);
};
const error_get=function(){
  let htmlString=`  <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>
                    <td class="c-cell_second">Error</td>`;   
  document.querySelector('.js-table').innerHTML=htmlString
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
    listenToLockbuttons()
}
const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
}
const init = function () {
    getUsers()    
    listenToSocket();
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});