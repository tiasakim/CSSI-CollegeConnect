
var instance = M.FloatingActionButton.getInstance(elem);


document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.fixed-action-btn');
  var instances = M.FloatingActionButton.init(elems, {
    direction: 'left',
    hoverEnabled: false
  });
});

// 
// var toggleButton = document.querySelector('.btn-floating');
// var navBar = document.querySelector('.nav_bar');
// toggleButton.addEventListener('click', function(){
//   navBar.classList.toggle('hidden');
// });
