const monbutton = document.getElementById('button-charger-les-donnes');

monbutton.addEventListener('mouseover', function() {
   monbutton.style.backgroundColor = 'rgb(97, 129, 226)';
});

monbutton.addEventListener('mouseout', function() {
   monbutton.style.backgroundColor = 'royalblue';
});

monbutton.addEventListener('click', function() {
    // Redirection vers la page souhaitée
    window.location.href = 'page_data.html';});