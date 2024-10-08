// Function to toggle between light and dark modes
function toggleMode() {
    const body = document.body;
    const toggleButton = document.getElementById('toggleMode');
    
    if (body.classList.contains('light-mode')) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        localStorage.setItem('mode', 'dark');
        toggleButton.innerText = 'Switch to Light Mode';
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        localStorage.setItem('mode', 'light');
        toggleButton.innerText = 'Switch to Dark Mode';
    }
}

// Check for saved mode in localStorage and apply it
document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('mode') || 'light';
    document.body.classList.add(savedMode === 'dark' ? 'dark-mode' : 'light-mode');
    document.getElementById('toggleMode').innerText = savedMode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
});
