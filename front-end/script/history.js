const lanIP = `http://${window.location.hostname}:5000`;
console.log(lanIP)
const socketio = io(`${lanIP}`);

const getHistory = function () {
    
  const url = lanIP + '/api/v1/history/';
  console.log(url)
  handleData(url, fill_table,error_get);
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
    document.querySelector('.js-table').innerHTML=htmlString
}

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
}
const init = function () {
    getHistory()    
    listenToSocket();
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  init();
});