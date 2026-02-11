// Exam Management Script

let examDuration = 30 * 60; // 30 minutes in seconds
let timeRemaining = examDuration;
let timerInterval = null;

// Start timer
function startTimer() {
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();

        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            autoSubmitExam();
        }
    }, 1000);
}

// Update timer display
function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const display = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    const timerEl = document.getElementById('timer');
    if (timerEl) {
        timerEl.textContent = display;

        // Warning color when less than 5 minutes
        if (timeRemaining <= 300) {
            timerEl.style.background = '#ef4444';
        }
    }
}

// Auto submit when time runs out
function autoSubmitExam() {
    alert('Time is up! Your exam will be submitted automatically.');
    submitExam();
}

// Handle exam submission
async function submitExam() {
    const form = document.getElementById('examForm');
    const formData = new FormData(form);

    // Collect answers
    const answers = {};
    for (let [key, value] of formData.entries()) {
        const questionId = key.replace('question_', '');
        answers[questionId] = value;
    }

    // Check if all questions are answered
    const totalQuestions = document.querySelectorAll('.question-card').length;
    if (Object.keys(answers).length < totalQuestions) {
        if (!confirm(`You have only answered ${Object.keys(answers).length} out of ${totalQuestions} questions. Submit anyway?`)) {
            return;
        }
    }

    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    try {
        const response = await fetch('/submit_exam', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: answers })
        });

        const result = await response.json();

        if (result.status === 'success') {
            clearInterval(timerInterval);
            showResults(result);
        } else {
            alert('Error submitting exam: ' + result.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Exam';
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('Error submitting exam. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Exam';
    }
}

// Show results modal
function showResults(result) {
    const modal = document.getElementById('resultModal');
    const content = document.getElementById('resultContent');

    const violations = result.violations.violations;
    const violationText = Object.keys(violations).length > 0
        ? Object.entries(violations).map(([type, count]) => `${type}: ${count}`).join('<br>')
        : 'No violations recorded';

    content.innerHTML = `
        <div style="margin: 20px 0;">
            <div style="background: #f0f9ff; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="color: #0369a1; margin-bottom: 10px;">Exam Score</h3>
                <p style="font-size: 2.5rem; font-weight: bold; color: #0284c7; margin: 0;">
                    ${result.exam_score.toFixed(1)}%
                </p>
            </div>
            
            <div style="background: ${result.suspicious_score > 30 ? '#fee2e2' : '#d1fae5'}; padding: 20px; border-radius: 10px;">
                <h3 style="color: ${result.suspicious_score > 30 ? '#991b1b' : '#065f46'}; margin-bottom: 10px;">
                    Proctoring Score
                </h3>
                <p style="font-size: 1.8rem; font-weight: bold; color: ${result.suspicious_score > 30 ? '#dc2626' : '#10b981'}; margin-bottom: 10px;">
                    ${result.suspicious_score} suspicious points
                </p>
                <div style="font-size: 0.9rem; text-align: left;">
                    ${violationText}
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
}

// Form submission handler
document.addEventListener('DOMContentLoaded', () => {
    const examForm = document.getElementById('examForm');

    if (examForm) {
        // Start timer
        startTimer();

        // Handle form submission
        examForm.addEventListener('submit', (e) => {
            e.preventDefault();

            if (confirm('Are you sure you want to submit your exam?')) {
                submitExam();
            }
        });

        // Warn before leaving page
        window.addEventListener('beforeunload', (e) => {
            if (timeRemaining > 0) {
                e.preventDefault();
                e.returnValue = 'Your exam is in progress. Are you sure you want to leave?';
                return e.returnValue;
            }
        });
    }
});

// Prevent back button during exam
history.pushState(null, null, location.href);
window.onpopstate = function () {
    history.go(1);
};
