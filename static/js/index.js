
document.addEventListener('DOMContentLoaded', function() {
    // --- 1. HANDLE CUSTOM FILE INPUTS ---
    const allCustomFileInputs = document.querySelectorAll('.file-input-wrapper input[type="file"]');
    allCustomFileInputs.forEach(inputElement => {
        inputElement.addEventListener('change', function(event) {
            const fileNameDisplay = this.closest('.file-input-wrapper').querySelector('.file-name');
            if (event.target.files.length > 0) {
                fileNameDisplay.textContent = event.target.files[0].name;
            } else {
                fileNameDisplay.textContent = 'No file chosen';
            }
        });
    });

    // --- 2. PROVIDE FEEDBACK ON FORM SUBMISSION ---
    const form = document.querySelector('form');
    if (form) {
        const submitButton = form.querySelector('button[type="submit"]');
        form.addEventListener('submit', function() {
            submitButton.disabled = true;
            submitButton.textContent = 'Generating... Please Wait';
        });
    }
});