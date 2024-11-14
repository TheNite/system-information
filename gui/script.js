// Theme toggle functionality
const themeToggle = document.getElementById('darkModeToggle');
const body = document.body;

themeToggle.addEventListener('change', () => {
    if (themeToggle.checked) {
        body.classList.add('bg-dark', 'text-light');
        body.classList.remove('bg-light', 'text-dark');
    } else {
        body.classList.add('bg-light', 'text-dark');
        body.classList.remove('bg-dark', 'text-light');
    }
});

// Function to show system information
async function showSystemInfo() {
    const output = document.getElementById('output');
    const placeholderLoader = document.getElementById('placeholderLoader');
    const outputCard = document.getElementById('outputCard');
    const showInfoButton = document.getElementById('showInfo');
    const showInfoText = document.getElementById('showInfoText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Disable the button and show the loading spinner
    showInfoButton.disabled = true;
    showInfoText.classList.add('d-none');
    loadingSpinner.classList.remove('d-none');

    // Show placeholder and hide output card
    placeholderLoader.classList.remove('d-none');
    outputCard.classList.add('d-none');

    // Simulate data fetching delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Fetch system info from Python
    const systemInfo = await pywebview.api.get_system_info();

    // Hide placeholder and show the output card
    placeholderLoader.classList.add('d-none');
    outputCard.classList.remove('d-none');
    output.textContent = systemInfo;

    // Reset the button state
    showInfoButton.disabled = false;
    showInfoText.classList.remove('d-none');
    loadingSpinner.classList.add('d-none');
}

// Function to copy the system info to clipboard
async function copyToClipboard() {
    const output = document.getElementById('output').textContent;
    await navigator.clipboard.writeText(output);
    alert('System information copied to clipboard!');
}

// Event listeners
document.getElementById('showInfo').addEventListener('click', showSystemInfo);
document.getElementById('copyInfo').addEventListener('click', copyToClipboard);
