// Webcam and Tab Monitoring Script

let violationCount = 0;
let webcamStream = null;

// Initialize webcam
async function initWebcam() {
  try {
    const video = document.getElementById('webcam');
    webcamStream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    });
    video.srcObject = webcamStream;
    console.log('✓ Webcam initialized');
  } catch (error) {
    console.error('Webcam error:', error);
    alert('⚠️ Webcam access denied! The exam requires camera access for proctoring.');
    updateMonitorStatus('❌ Camera access denied', 'error');
  }
}

// Update monitor status
function updateMonitorStatus(message, type = 'success') {
  const statusEl = document.getElementById('monitorStatus');
  if (statusEl) {
    statusEl.innerHTML = `<p>${message}</p>`;
    statusEl.className = 'monitor-status ' + (type === 'error' ? 'error' : '');
  }
}

// Log violation
async function logViolation(type) {
  try {
    const response = await fetch('/violation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: type })
    });

    const data = await response.json();

    if (data.status === 'logged') {
      violationCount++;
      updateViolationCount();
      addViolationToLog(type);

      // Show warning
      showWarning(type);
    }
  } catch (error) {
    console.error('Error logging violation:', error);
  }
}

// Update violation count display
function updateViolationCount() {
  const countEl = document.getElementById('violation-number');
  if (countEl) {
    countEl.textContent = violationCount;

    // Add warning animation
    const violationsEl = document.getElementById('violation-count');
    violationsEl.style.animation = 'pulse 0.5s';
    setTimeout(() => {
      violationsEl.style.animation = '';
    }, 500);
  }
}

// Add violation to log
function addViolationToLog(type) {
  const logList = document.getElementById('violationList');
  if (logList) {
    // Remove "no violations" message
    const noViolations = logList.querySelector('.no-violations');
    if (noViolations) {
      noViolations.remove();
    }

    // Add new violation
    const violationItem = document.createElement('div');
    violationItem.className = 'violation-item';
    violationItem.style.cssText = 'padding: 8px; background: #fee2e2; border-radius: 6px; margin-bottom: 8px; font-size: 0.9rem; color: #991b1b;';

    const time = new Date().toLocaleTimeString();
    violationItem.innerHTML = `<strong>${type}</strong><br><small>${time}</small>`;

    logList.insertBefore(violationItem, logList.firstChild);

    // Keep only last 5 violations
    while (logList.children.length > 5) {
      logList.removeChild(logList.lastChild);
    }
  }
}

// Show warning popup
function showWarning(type) {
  const warning = document.createElement('div');
  warning.className = 'warning-popup';
  warning.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #fee2e2;
        color: #991b1b;
        padding: 15px 20px;
        border-radius: 8px;
        border-left: 4px solid #ef4444;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
    `;
  warning.innerHTML = `<strong>⚠️ Violation Detected</strong><br>${type}`;

  document.body.appendChild(warning);

  setTimeout(() => {
    warning.remove();
  }, 3000);
}

// Tab switching detection
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    logViolation('Tab Switch');
    console.warn('⚠️ Tab switch detected');
  }
});

// Prevent right-click
document.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  return false;
});

// Prevent certain keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Prevent F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
  if (e.key === 'F12' ||
    (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J')) ||
    (e.ctrlKey && e.key === 'U')) {
    e.preventDefault();
    return false;
  }
});

// Logout function
function logout() {
  if (confirm('Are you sure you want to logout? Your exam progress will be lost.')) {
    window.location.href = '/logout';
  }
}

// Initialize on page load
if (document.getElementById('webcam')) {
  window.addEventListener('load', () => {
    initWebcam();
  });
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (webcamStream) {
    webcamStream.getTracks().forEach(track => track.stop());
  }
});

// Add pulse animation for violations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .monitor-status.error {
        background: #fee2e2 !important;
        color: #991b1b !important;
    }
`;
document.head.appendChild(style);
