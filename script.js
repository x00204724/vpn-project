// RTT Chart - Real Data from Testing
const rttCtx = document.getElementById('rttChart').getContext('2d');
const rttChart = new Chart(rttCtx, {
    type: 'line',
    data: {
        labels: Array.from({length: 20}, (_, i) => i + 1),
        datasets: [
            {
                label: 'Tunnel RTT (ms)',
                data: [36, 40, 42, 48, 52, 55, 50, 54, 60, 58, 62, 52, 56, 60, 64, 68, 72, 65, 70, 80],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 4
            },
            {
                label: 'Tunnel Down (ms)',
                data: [0, 0, 92.8, 75.644, 75.704, 0, 0, 62.48, 60.945, 61.513, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 4
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Tunnel0 RTT Over 20 ICMP Packets',
                font: { size: 16 }
            },
            legend: {
                display: true,
                position: 'bottom'
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'RTT (ms)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'ICMP Sequence'
                }
            }
        }
    }
});

// Shared tunnel config — matches animation exactly
const tunnels = {
    labels:  ['Baseline (No VPN)', 'GRE Tunnel', 'GRE + IPSec', 'WireGuard', 'PriTunnel'],
    colors:  ['#28a745', '#667eea', '#764ba2', '#ffc107', '#e74c3c'],
    times:   [0.287, 0.95, 1.4, 0.6, 0.8],
    throughput: [592, 179, 121, 283, 213]
};

const bgColors = tunnels.colors.map(c => c + 'b3');

// File Transfer Time Chart
const transferCtx = document.getElementById('transferChart').getContext('2d');
new Chart(transferCtx, {
    type: 'bar',
    data: {
        labels: tunnels.labels,
        datasets: [{
            label: 'Transfer Time (seconds)',
            data: tunnels.times,
            backgroundColor: bgColors,
            borderColor: tunnels.colors,
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'AliceInWonderland.txt — Transfer Time by Tunnel', font: { size: 16 } },
            legend: { display: false },
            tooltip: { callbacks: { label: ctx => ctx.raw + 's' } }
        },
        scales: {
            y: { beginAtZero: true, title: { display: true, text: 'Seconds' } }
        }
    }
});

// Throughput Chart
const throughputCtx = document.createElement('canvas');
throughputCtx.id = 'throughputChart';
document.getElementById('transferChart').parentNode.appendChild(throughputCtx);
new Chart(throughputCtx, {
    type: 'bar',
    data: {
        labels: tunnels.labels,
        datasets: [{
            label: 'Throughput (KB/s)',
            data: tunnels.throughput,
            backgroundColor: bgColors,
            borderColor: tunnels.colors,
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'AliceInWonderland.txt — Throughput by Tunnel (KB/s)', font: { size: 16 } },
            legend: { display: false }
        },
        scales: {
            y: { beginAtZero: true, title: { display: true, text: 'KB/s' } }
        }
    }
});

// File Transfer Animation
function runTransfer(tunnelName, duration, color) {
    const packet = document.getElementById('anim-packet');
    const fill = document.getElementById('anim-fill');
    const label = document.getElementById('tunnel-label');
    const statTunnel = document.getElementById('stat-tunnel');
    const statTime = document.getElementById('stat-time');
    const statSpeed = document.getElementById('stat-speed');
    const statStatus = document.getElementById('stat-status');

    const fileSize = 170;
    const throughput = (fileSize / duration).toFixed(0);

    // Reset
    packet.style.transition = 'none';
    packet.style.left = '-30px';
    fill.style.transition = 'none';
    fill.style.width = '0%';
    fill.style.background = color;

    label.textContent = tunnelName;
    label.style.color = color;
    statTunnel.textContent = tunnelName;
    statTime.textContent = duration + 's';
    statSpeed.textContent = throughput + ' KB/s';
    statStatus.textContent = 'Transferring...';
    statStatus.style.color = color;

    // Animate after reset frame
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            packet.style.transition = `left ${duration}s linear`;
            packet.style.left = 'calc(100% + 10px)';
            fill.style.transition = `width ${duration}s linear`;
            fill.style.width = '100%';
        });
    });

    setTimeout(() => {
        statStatus.textContent = '✅ Complete';
        statStatus.style.color = '#28a745';
    }, duration * 1000);
}

// Company Size Comparison Chart
const companyCtx = document.getElementById('companyChart').getContext('2d');
new Chart(companyCtx, {
    type: 'bar',
    data: {
        labels: ['WireGuard', 'Tailscale', 'OpenVPN', 'GRE + IPSec', 'Azure Hybrid', 'PriTunnel'],
        datasets: [
            {
                label: 'Startup Suitability',
                data: [9, 9, 5, 2, 1, 7],
                backgroundColor: 'rgba(40, 167, 69, 0.7)',
                borderColor: '#28a745',
                borderWidth: 2
            },
            {
                label: 'SME Suitability',
                data: [7, 7, 8, 9, 5, 8],
                backgroundColor: 'rgba(102, 126, 234, 0.7)',
                borderColor: '#667eea',
                borderWidth: 2
            },
            {
                label: 'Enterprise Suitability',
                data: [4, 4, 7, 9, 10, 5],
                backgroundColor: 'rgba(118, 75, 162, 0.7)',
                borderColor: '#764ba2',
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'VPN Technology Suitability by Organisation Size (Score out of 10)',
                font: { size: 15 }
            },
            legend: { position: 'bottom' }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 10,
                title: { display: true, text: 'Suitability Score' }
            }
        }
    }
});

// Company transfer animation data
const companyData = {
    startup:    { name: 'Startup',    icon: 'Startup',    vpn: 'WireGuard',        time: 0.6,  color: '#4a7c59', throughput: 283 },
    sme:        { name: 'SME',        icon: 'SME',        vpn: 'GRE + IPSec',      time: 1.4,  color: '#1a2e4a', throughput: 121 },
    enterprise: { name: 'Enterprise', icon: 'Enterprise', vpn: 'Azure Hybrid VPN', time: 2.1,  color: '#c9a84c', throughput: 81  }
};

function runCompanyTransfer(type) {
    const d = companyData[type];
    const packet  = document.getElementById('co-packet');
    const fill    = document.getElementById('co-fill');
    const label   = document.getElementById('co-tunnel-label');
    const senderIcon  = document.getElementById('co-sender-icon');
    const senderLabel = document.getElementById('co-sender-label');
    const senderVpn   = document.getElementById('co-sender-vpn');

    // Reset
    packet.style.transition = 'none';
    packet.style.left = '-30px';
    fill.style.transition = 'none';
    fill.style.width = '0%';
    fill.style.background = d.color;

    senderIcon.textContent  = d.icon;
    senderLabel.textContent = d.name;
    senderVpn.textContent   = d.vpn;
    label.textContent       = `${d.name} — ${d.vpn}`;
    label.style.color       = d.color;

    document.getElementById('co-stat-company').textContent = d.name;
    document.getElementById('co-stat-vpn').textContent     = d.vpn;
    document.getElementById('co-stat-time').textContent    = d.time + 's';
    document.getElementById('co-stat-speed').textContent   = d.throughput + ' KB/s';
    document.getElementById('co-stat-status').textContent  = 'Transferring...';
    document.getElementById('co-stat-status').style.color  = d.color;

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            packet.style.transition = `left ${d.time}s linear`;
            packet.style.left = 'calc(100% + 10px)';
            fill.style.transition = `width ${d.time}s linear`;
            fill.style.width = '100%';
        });
    });

    setTimeout(() => {
        document.getElementById('co-stat-status').textContent = '✅ Complete';
        document.getElementById('co-stat-status').style.color = '#28a745';
    }, d.time * 1000);
}

// Company Transfer Time Chart
const coTransferCtx = document.getElementById('companyTransferChart').getContext('2d');
new Chart(coTransferCtx, {
    type: 'bar',
    data: {
        labels: ['🚀 Startup (WireGuard)', '🏢 SME (GRE + IPSec)', '🏭 Enterprise (Azure Hybrid)'],
        datasets: [
            {
                label: 'Transfer Time (seconds)',
                data: [0.6, 1.4, 2.1],
                backgroundColor: ['rgba(40,167,69,0.7)', 'rgba(102,126,234,0.7)', 'rgba(118,75,162,0.7)'],
                borderColor: ['#28a745', '#667eea', '#764ba2'],
                borderWidth: 2,
                yAxisID: 'y'
            },
            {
                label: 'Throughput (KB/s)',
                data: [283, 121, 81],
                backgroundColor: ['rgba(40,167,69,0.3)', 'rgba(102,126,234,0.3)', 'rgba(118,75,162,0.3)'],
                borderColor: ['#28a745', '#667eea', '#764ba2'],
                borderWidth: 2,
                borderDash: [5,5],
                yAxisID: 'y1'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'AliceInWonderland.txt Transfer — By Company Type & Recommended VPN', font: { size: 15 } },
            legend: { position: 'bottom' }
        },
        scales: {
            y:  { beginAtZero: true, title: { display: true, text: 'Transfer Time (s)' }, position: 'left' },
            y1: { beginAtZero: true, title: { display: true, text: 'Throughput (KB/s)' }, position: 'right', grid: { drawOnChartArea: false } }
        }
    }
});

// Sidebar active section highlight
const sidebarLinks = document.querySelectorAll('.sidebar a');
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => {
        if (window.scrollY >= s.offsetTop - 100) current = s.id;
    });
    sidebarLinks.forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    });
});
