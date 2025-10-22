// Check if user info exists in browser storage
const address = localStorage.getItem('panic_address');
const area = localStorage.getItem('panic_area');

if (address && area) {
  document.getElementById('main').style.display = 'block';
} else {
  document.getElementById('setup').style.display = 'block';
}

function saveInfo() {
  const addr = document.getElementById('address').value.trim();
  const ar = document.getElementById('area').value.trim();
  if (addr && ar) {
    localStorage.setItem('panic_address', addr);
    localStorage.setItem('panic_area', ar);
    document.getElementById('setup').style.display = 'none';
    document.getElementById('main').style.display = 'block';
  } else {
    alert("Please enter both address and area.");
  }
}

async function triggerPanic() {
  if (!confirm("Are you sure? This will alert everyone!")) return;
  
  const response = await fetch('/panic', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      address: localStorage.getItem('panic_address'),
      area: localStorage.getItem('panic_area')
    })
  });
  const result = await response.json();
  alert(result.status);
}

// Poll for new alerts every 3 seconds
setInterval(async () => {
  try {
    const res = await fetch('/alerts');
    const alerts = await res.json();
    const div = document.getElementById('alerts');
    if (alerts.length > 0) {
      div.innerHTML = '<h3>🚨 Recent Alerts:</h3>' + alerts.map(a => `<p>${a}</p>`).join('');
      div.style.display = 'block';
    } else {
      div.style.display = 'none';
    }
  } catch (e) {
    console.log("Could not fetch alerts:", e);
  }
}, 3000);