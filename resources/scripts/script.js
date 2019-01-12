window.addEventListener("DOMContentLoaded", function() {
	if('localStorage' in window && 'background' in localStorage) {
		var bg = document.querySelectorAll('.bg');
		for(var i = 0; i < bg.length; i++) {
			bg[i].style.backgroundImage = 'url(' + localStorage.getItem('background') + ')';
		};
	} else {
		localStorage.setItem('background', 'https://i.imgur.com/3jmkrwR.jpg');
	};
});