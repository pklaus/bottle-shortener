

function ajax_submit() {
  request = new XMLHttpRequest();
  var url, requesting;
  url = document.forms['new']['url'].value;
  requesting = document.forms['new']['requesting'].value;
  request.open('GET', '/new?url='+url+'&requesting='+requesting, true);

  request.onload = function() {
    if (this.status >= 200 && this.status < 400){
      // Success!
      data = JSON.parse(this.response);
      if (data['success']) {
        show_success(url, data['result']);
      } else {
        show_error('Error: ' + data['error'])
      }
    } else {
      // We reached our target server, but it returned an error
      show_error('Sorry, could not request a short URL.')
    }
  };
  
  request.onerror = function() {
    // There was a connection error of some sort
  };
  
  request.send();
}

function show_success(url, short_form) {
  document.querySelectorAll('#error')[0].style.display = 'none';
  document.querySelectorAll('#newentry')[0].style.display = 'none';
  //alert('Success:\n' + url + '\n' + short_form);
  document.querySelectorAll('#orig_url')[0].textContent = url;
  document.querySelectorAll('#short_url')[0].textContent = short_form;
  selection = window.getSelection();        
  range = document.createRange();
  range.selectNodeContents(document.querySelectorAll('#short_url')[0]);
  selection.removeAllRanges();
  selection.addRange(range);
  var num_entries  = document.querySelectorAll('#num_entries')[0];
  num_entries.textContent = parseInt(num_entries.textContent) + 1;
  document.querySelectorAll('#success')[0].style.display = '';
}

function show_error(message) {
  //alert('Error:\n' + message);
  document.querySelectorAll('#error_message')[0].textContent = message;
  document.querySelectorAll('#error')[0].style.display = '';
}

