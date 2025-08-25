// HealthMate JavaScript Functions

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});

// Form validation
function validateMeasurementForm() {
    const weight = document.getElementById('weight').value;
    const bpSystolic = document.getElementById('bp_systolic').value;
    const bpDiastolic = document.getElementById('bp_diastolic').value;
    const heartRate = document.getElementById('heart_rate').value;
    const bloodSugar = document.getElementById('blood_sugar').value;
    
    if (!weight && !bpSystolic && !bpDiastolic && !heartRate && !bloodSugar) {
        alert('Please enter at least one measurement value.');
        return false;
    }
    
    return true;
}

// BMI calculator
function calculateBMI(weight, height) {
    if (weight && height) {
        return weight / Math.pow(height / 100, 2);
    }
    return null;
}

// Date formatting helper
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Chart initialization (if using additional chart libraries)
function initCharts() {
    // This would be implemented if using Chart.js or another library
    console.log('Charts initialized');
}

// Auto-save form data
function setupAutoSave(formId, saveKey) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Load saved data
    const savedData = localStorage.getItem(saveKey);
    if (savedData) {
        const data = JSON.parse(savedData);
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) input.value = data[key];
        });
    }
    
    // Save on input change
    form.addEventListener('input', function() {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        localStorage.setItem(saveKey, JSON.stringify(data));
    });
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    
    // Set up auto-save for measurement form
    setupAutoSave('measurement-form', 'healthmate_measurement_draft');
    
    // Add today's date to date fields
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]:not([value])').forEach(input => {
        if (input.id === 'deadline') {
            // Set deadline to 30 days from now
            const futureDate = new Date();
            futureDate.setDate(futureDate.getDate() + 30);
            input.value = futureDate.toISOString().split('T')[0];
        } else if (!input.value) {
            input.value = today;
        }
    });
});