document.querySelector('#room-name-input').focus();

document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        document.querySelector('#room-name-submit').click();
    }
};


let regex = /[\\\/^\\\/]/;
document.querySelector('#room-name-input').oninput = function() {
    this.value = this.value.replace(regex, '');
}


document.querySelector('#room-name-submit').onclick = function(e) {
    let roomName = document.querySelector('#room-name-input').value;
    window.location.pathname = '/chat/' + roomName + '/';
};