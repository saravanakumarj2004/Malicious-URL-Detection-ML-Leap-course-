// Tab Switching Logic
function switchTab(tabId) {
    // Update nav links
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    const clickedNav = document.querySelector(`.nav-item[href="#${tabId}"]`);
    if(clickedNav) clickedNav.classList.add('active');

    // Update content sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active-section');
    });
    document.getElementById(tabId).classList.add('active-section');
}

// Form Submission Logic
const scanForm = document.getElementById('scan-form');
const urlInput = document.getElementById('url-input');
const scanBtnBtn = document.getElementById('scan-btn');
const btnText = document.querySelector('.btn-text');
const spinner = document.getElementById('spinner');

const resultContainer = document.getElementById('result-container');
const resultCard = document.getElementById('result-card');
const resultIcon = document.getElementById('result-icon');
const resultStatus = document.getElementById('result-status');
const scannedUrlDisplay = document.getElementById('scanned-url-display');
const meterFill = document.getElementById('meter-fill');
const confidencePercentage = document.getElementById('confidence-percentage');
const resultDescription = document.getElementById('result-description');

scanForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = urlInput.value.trim();
    if (!url) return;

    // Loading State
    btnText.textContent = 'Scanning...';
    spinner.classList.remove('hidden');
    scanBtnBtn.disabled = true;
    
    // Hide previous result
    resultContainer.classList.add('hidden');
    resultCard.classList.remove('status-safe', 'status-danger');
    meterFill.style.width = '0%';

    try {
        // We are querying the local FastAPI model route
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error('Server error occurred');
        }

        const data = await response.json();
        const score = data.prediction_score;
        const isMalicious = data.is_malicious;

        // Confidence calculation
        // If > 0.5, malicious confidence is (score * 100)%
        // If < 0.5, benign confidence is ((1 - score) * 100)%
        const confidenceValue = isMalicious ? score : (1 - score);
        const confidenceText = (confidenceValue * 100).toFixed(1) + '%';

        // Update UI logic
        scannedUrlDisplay.textContent = data.url;
        confidencePercentage.textContent = confidenceText;

        // Trigger animation reflow
        setTimeout(() => {
            meterFill.style.width = confidenceText;
        }, 100);

        if (isMalicious) {
            resultCard.classList.add('status-danger');
            resultIcon.innerHTML = '⚠️';
            resultStatus.textContent = 'Threat Detected';
            resultStatus.style.color = 'var(--danger-color)';
            resultDescription.innerHTML = `Our model has determined with <strong>${confidenceText} confidence</strong> that this URL exhibits patterns consistent with defacement or malicious activity. Do not visit this site.`;
        } else {
            resultCard.classList.add('status-safe');
            resultIcon.innerHTML = '✅';
            resultStatus.textContent = 'Safe to Browse';
            resultStatus.style.color = 'var(--safe-color)';
            resultDescription.innerHTML = `No malicious patterns were found. Our model is <strong>${confidenceText} confident</strong> that this URL is benign and safe for browsing.`;
        }

        resultContainer.classList.remove('hidden');

    } catch (error) {
        console.error('Prediction failed:', error);
        alert('Failed to connect to the prediction server. Make sure the backend is running.');
    } finally {
        // Reset Button
        btnText.textContent = 'Analyze';
        spinner.classList.add('hidden');
        scanBtnBtn.disabled = false;
    }
});
