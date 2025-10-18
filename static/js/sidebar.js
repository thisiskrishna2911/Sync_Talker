document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.sidebar-toggle');
    const contentWrapper = document.querySelector('.main-content-wrapper');

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            contentWrapper.classList.toggle('shifted');
        });
    }
});