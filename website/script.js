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

// File Transfer Comparison Chart
const transferCtx = document.getElementById('transferChart').getContext('2d');
const transferChart = new Chart(transferCtx, {
    type: 'bar',
    data: {
        labels: ['Baseline (No VPN)', 'GRE Only', 'GRE + IPSec', 'WireGuard', 'PriTunnel'],
        datasets: [{
            label: 'File Transfer Time (seconds)',
            data: [0.287, null, null, null, null],
            backgroundColor: [
                'rgba(40, 167, 69, 0.7)',
                'rgba(102, 126, 234, 0.4)',
                'rgba(118, 75, 162, 0.4)',
                'rgba(255, 193, 7, 0.4)',
                'rgba(220, 53, 69, 0.4)'
            ],
            borderColor: [
                '#28a745',
                '#667eea',
                '#764ba2',
                '#ffc107',
                '#dc3545'
            ],
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'AliceInWonderland.txt Transfer Time Across VPN Tunnels',
                font: { size: 16 }
            },
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (ctx) => ctx.raw ? `${ctx.raw}s` : 'Pending'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: { display: true, text: 'Transfer Time (seconds)' }
            }
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
