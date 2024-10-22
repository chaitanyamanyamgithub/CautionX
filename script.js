// Function to handle result box display
function showResult(resultBox, status, message) {
  resultBox.style.display = 'block';
  resultBox.innerHTML = `<span class="result-icon">${status === 'safe' ? '✅' : '❌'}</span> ${message}`;
  resultBox.classList.toggle('safe', status === 'safe');
  resultBox.classList.toggle('threat', status === 'threat');
}

// URL Detection form submission
document.getElementById('url-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const url = document.getElementById('url-input').value;

  fetch('/url_detection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ 'url': url })
  }).then(res => res.json()).then(data => {
      const resultBox = document.getElementById('url-result');
      showResult(resultBox, data.status, data.message);
  });
});

document.getElementById('retry-url-btn').addEventListener('click', function() {
  document.getElementById('url-input').value = '';
  document.getElementById('url-result').style.display = 'none';
});

// Threat Analysis form submission
document.getElementById('threat-form').addEventListener('submit', function(e) {
  e.preventDefault();
  let formData = new FormData(this);

  fetch('/threat_analysis', {
      method: 'POST',
      body: formData
  }).then(res => res.json()).then(data => {
      const resultBox = document.getElementById('threat-result');
      showResult(resultBox, data.status, data.message);
  });
});

document.getElementById('retry-threat-btn').addEventListener('click', function() {
  document.querySelectorAll('#threat-form input[type="number"]').forEach(input => input.value = '');
  document.getElementById('threat-result').style.display = 'none';
});

// Modal functionality
function showModal() {
  document.getElementById('popup-modal').style.display = 'flex';
}

document.getElementById('logs-btn').addEventListener('click', showModal);
document.getElementById('settings-btn').addEventListener('click', showModal);

document.querySelector('.close').addEventListener('click', function() {
  document.getElementById('popup-modal').style.display = 'none';
});

// Switch between sections
document.getElementById('url-detection-btn').addEventListener('click', function() {
  document.getElementById('url-detection').classList.add('active');
  document.getElementById('threat-analysis').classList.remove('active');
});

document.getElementById('threat-analysis-btn').addEventListener('click', function() {
  document.getElementById('threat-analysis').classList.add('active');
  document.getElementById('url-detection').classList.remove('active');
});
