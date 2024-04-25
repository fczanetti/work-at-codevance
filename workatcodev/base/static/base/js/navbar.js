const navbarLinks = document.getElementById('nav-links')
const toggleButton = document.getElementById('toggle-button')

toggleButton.onclick = function() {
    navbarLinks.classList.toggle('active')
};