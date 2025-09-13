// Keep JS minimal and avoid setting date/time from JavaScript
(function(){
  // Auto-hide flash messages after 4 seconds
  const flashes = document.querySelectorAll('.flash');
  if(flashes.length){
    setTimeout(()=>{
      flashes.forEach(f => f.style.display = 'none');
    }, 4000);
  }
})();
