document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.querySelector('input[name="image"]');
    const audioInput = document.querySelector('input[name="audio"]');
    const form = document.querySelector('form');

    function createFileInfoElement(inputElement) {
        const fileInfo = document.createElement('div');
        fileInfo.classList.add('file-info');
        inputElement.parentNode.insertBefore(fileInfo, inputElement.nextSibling);
        return fileInfo;
    }

    const imageFileInfo = createFileInfoElement(imageInput);
    const audioFileInfo = createFileInfoElement(audioInput);

    function updateFileInfo(inputElement, infoElement) {
        inputElement.addEventListener('change', function() {
            if (this.files.length > 0) {
                infoElement.textContent = `Selected: ${this.files[0].name}`;
            } else {
                infoElement.textContent = '';
            }
        });
    }

    updateFileInfo(imageInput, imageFileInfo);
    updateFileInfo(audioInput, audioFileInfo);

    form.addEventListener('submit', function(event) {
        if (imageInput.files.length === 0 || audioInput.files.length === 0) {
            event.preventDefault();
            alert('Please make sure to upload both an image and an audio file.');
        }
    });
});