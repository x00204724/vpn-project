// File Transfer Animation - Fixed for website/index.html
document.addEventListener('DOMContentLoaded', function() {
  // Tunnel config with real data from vpn_measurements.json
  const tunnels = {
    'Baseline (No VPN)': { time: 0.29, color: '#28a745', throughput: 587 },
    'GRE Tunnel': { time: 0.31, color: '#667eea', throughput: 551 },
    'GRE + IPSec': { time: 0.94, color: '#764ba2', throughput: 181 },
    'WireGuard': { time: 0.60, color: '#ffc107', throughput: 285 },
    'PriTunnel': { time: 0.80, color: '#e74c3c', throughput: 213 }
  };

  // Button clicks
  document.querySelectorAll('.tunnel-buttons button').forEach(btn => {
    btn.addEventListener('click', function() {
      const tunnelName = this.textContent.trim();
      if (!tunnels[tunnelName]) return;
      
      const config = tunnels[tunnelName];
      runTransfer(tunnelName, config.time, config.color, config.throughput);
    });
  });

  function runTransfer(name, duration, color, throughput) {
    // Elements
    const packet = document.getElementById('anim-packet');
    const fill = document.getElementById('anim-fill');
    const label = document.getElementById('tunnel-label');
    const statTunnel = document.getElementById('stat-tunnel');
    const statTime = document.getElementById('stat-time');
    const statSpeed = document.getElementById('stat-speed');
    const statStatus = document.getElementById('stat-status');

    // Reset
    packet.style.transition = 'none';
    packet.style.left = '-30px';
    fill.style.transition = 'none';
    fill.style.width = '0%';
    fill.style.background = color;
    requestAnimationFrame(() => {
      packet.style.transition = `left ${duration}s linear`;
      packet.style.left = 'calc(100% + 10px)';
      fill.style.transition = `width ${duration}s linear`;
      fill.style.width = '100%';
    });

    // Update stats
    label.textContent = name;
    label.style.color = color;
    statTunnel.textContent = name;
    statTime.textContent = duration.toFixed(2) + 's';
    statSpeed.textContent = throughput.toFixed(0) + ' KB/s';
    statStatus.textContent = 'Transferring...';
    statStatus.style.color = color;

    // Complete
    setTimeout(() => {
      statStatus.textContent = 'Complete';
      statStatus.style.color = '#28a745';
    }, duration * 1000);
  }
});

// Load real data charts (rttChart, transferChart)
async function initCharts() {
  try {
    const response = await fetch('../vpn_measurements.json');
    const data = await response.json();
    updateTransferChart(data.results);
  } catch (e) {
    // Fallback hardcoded
    updateTransferChart([
      { vpn_name: 'Baseline', transfer_time: { mean: 0.29 }, throughput: { mean: 587 } },
      { vpn_name: 'GRE', transfer_time: { mean: 0.31 }, throughput: { mean: 551 } },
      { vpn_name: 'GRE + IPSec', transfer_time: { mean: 0.94 }, throughput: { mean: 181 } },
      { vpn_name: 'WireGuard', transfer_time: { mean: 0.60 }, throughput: { mean: 285 } },
      { vpn_name: 'PriTunnel', transfer_time: { mean: 0.80 }, throughput: { mean: 213 } }
    ]);
  }
}

function updateTransferChart(results) {
  const ctx = document.getElementById('transferChart')?.getContext('2d');
  if (!ctx) return;

  const labels = results.map(r => r.vpn_name);
  const times = results.map(r => r.transfer_time.mean);
  new Chart(ctx.canvas, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Transfer Time (s)', data: times, backgroundColor: ['#28a745', '#667eea', '#764ba2', '#ffc107', '#e74c3c'] }] },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
  });
}

initCharts();

