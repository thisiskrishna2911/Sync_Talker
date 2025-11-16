document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.sidebar-toggle');
    const contentWrapper = document.querySelector('.main-content-wrapper');
    const breakpoint = 992; // The screen width where the layout changes

    // Function to set the initial state based on window size
    const setInitialState = () => {
        if (window.innerWidth > breakpoint) {
            sidebar.classList.add('open');
            contentWrapper.classList.add('shifted');
        } else {
            sidebar.classList.remove('open');
            contentWrapper.classList.remove('shifted');
        }
    };

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            // Only shift the content if the screen is wider than the breakpoint
            if (window.innerWidth > breakpoint) {
                contentWrapper.classList.toggle('shifted');
            }
        });
    }

    // Set the correct state when the page loads
    setInitialState();

    // Optional: Adjust if the user resizes their browser window
    window.addEventListener('resize', setInitialState);
});