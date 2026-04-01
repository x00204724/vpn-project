// Navigation - Show/Hide Sections
const sidebarLinks = document.querySelectorAll('.sidebar a');
const sections = document.querySelectorAll('section[id]');

// Dark Mode Toggle
function initDarkMode() {
    const isDark = localStorage.getItem('darkMode') === 'true';
    if (isDark) {
        document.body.classList.add('dark-mode');
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
}

// Search Functionality
function initSearch() {
    const searchBox = document.querySelector('.search-box input');
    const searchResults = document.querySelector('.search-results');
    
    if (!searchBox) return;
    
    const searchableItems = [
        { title: 'Overview', id: 'overview' },
        { title: 'Topology', id: 'topology' },
        { title: 'Methodology & Iterations', id: 'methodology' },
        { title: 'RTT Results', id: 'results' },
        { title: 'File Transfer', id: 'file-transfer' },
        { title: 'Wireshark Analysis', id: 'wireshark' },
        { title: 'VPN Calculator', id: 'calculator' },
        { title: 'Company Comparison', id: 'company-comparison' },
        { title: 'VPN Comparison', id: 'comparison' },
        { title: 'Azure Integration', id: 'azure' },
        { title: 'FAQ', id: 'faq' },
        { title: 'Compliance', id: 'compliance' },
        { title: 'Cost Calculator', id: 'cost-calculator' },
        { title: 'Troubleshooting', id: 'troubleshooting' },
        { title: 'Conclusion', id: 'conclusion' },
        { title: 'Deliverables', id: 'deliverables' }
    ];
    
    searchBox.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        searchResults.innerHTML = '';
        
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        
        const matches = searchableItems.filter(item => 
            item.title.toLowerCase().includes(query)
        );
        
        if (matches.length === 0) {
            searchResults.classList.remove('active');
            return;
        }
        
        matches.forEach(match => {
            const div = document.createElement('div');
            div.className = 'search-result-item';
            div.textContent = match.title;
            div.onclick = () => {
                const link = document.querySelector(`a[href="#${match.id}"]`);
                if (link) link.click();
                searchBox.value = '';
                searchResults.classList.remove('active');
            };
            searchResults.appendChild(div);
        });
        
        searchResults.classList.add('active');
    });
    
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-box') && !e.target.closest('.search-results')) {
            searchResults.classList.remove('active');
        }
    });
}

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
    initDarkMode();
    initSearch();
});

// Create dark mode toggle button
if (!document.querySelector('.dark-mode-toggle')) {
    const toggle = document.createElement('button');
    toggle.className = 'dark-mode-toggle';
    toggle.innerHTML = '🌙';
    toggle.title = 'Toggle Dark Mode';
    toggle.onclick = toggleDarkMode;
    document.body.appendChild(toggle);
}

// Create search box
if (!document.querySelector('.search-box')) {
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-box';
    searchContainer.innerHTML = '<input type="text" placeholder="Search sections...">';
    document.body.appendChild(searchContainer);
    
    const searchResults = document.createElement('div');
    searchResults.className = 'search-results';
    document.body.appendChild(searchResults);
}

sidebarLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        
        // Hide all sections
        sections.forEach(s => s.classList.remove('active'));
        
        // Show target section
        const target = document.getElementById(targetId);
        if (target) {
            target.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // Update active link
        sidebarLinks.forEach(a => a.classList.remove('active'));
        link.classList.add('active');
    });
});

// Show overview section by default
if (sections.length > 0) {
    sections[0].classList.add('active');
    sidebarLinks[1].classList.add('active');
}

// RTT Chart - Real Data from Testing
const rttCtx = document.getElementById('rttChart');
if (rttCtx) {
    const rttChart = new Chart(rttCtx.getContext('2d'), {
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
}

// Shared tunnel config — matches animation exactly
const tunnels = {
    labels:  ['Baseline (No VPN)', 'GRE Tunnel', 'GRE + IPSec', 'WireGuard', 'PriTunnel'],
    colors:  ['#28a745', '#667eea', '#764ba2', '#ffc107', '#e74c3c'],
    times:   [0.287, 0.95, 1.4, 0.6, 0.8],
    throughput: [592, 179, 121, 283, 213]
};

const bgColors = tunnels.colors.map(c => c + 'b3');

// File Transfer Time Chart
const transferCtx = document.getElementById('transferChart');
if (transferCtx) {
    new Chart(transferCtx.getContext('2d'), {
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
}

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
const companyCtx = document.getElementById('companyChart');
if (companyCtx) {
    new Chart(companyCtx.getContext('2d'), {
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
}

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
const coTransferCtx = document.getElementById('companyTransferChart');
if (coTransferCtx) {
    new Chart(coTransferCtx.getContext('2d'), {
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
}

// VPN Performance Calculator
function runCalculator() {
    const fileSize = parseFloat(document.getElementById('fileSize').value) || 170;
    const baseLatency = parseFloat(document.getElementById('baseLatency').value) || 10;
    const bandwidth = parseFloat(document.getElementById('bandwidth').value) || 100;
    const cpuOverhead = parseFloat(document.getElementById('cpuOverhead').value) || 5;
    
    // VPN profiles with overhead multipliers
    const vpns = [
        { name: 'Baseline (No VPN)', encryption: 'None', overhead: 1.0, latencyAdd: 0, cpuFactor: 0 },
        { name: 'GRE', encryption: 'None', overhead: 1.05, latencyAdd: 2, cpuFactor: 0.2 },
        { name: 'GRE + IPSec', encryption: 'AES-256', overhead: 1.35, latencyAdd: 5, cpuFactor: 1.0 },
        { name: 'WireGuard', encryption: 'ChaCha20', overhead: 1.10, latencyAdd: 3, cpuFactor: 0.5 },
        { name: 'OpenVPN', encryption: 'AES-256', overhead: 1.25, latencyAdd: 4, cpuFactor: 0.8 },
        { name: 'Azure Hybrid VPN', encryption: 'AES-256', overhead: 1.40, latencyAdd: 50, cpuFactor: 1.2 }
    ];
    
    const table = document.getElementById('calcTable');
    table.innerHTML = '';
    
    const results = [];
    
    vpns.forEach(vpn => {
        // Calculate effective throughput
        const effectiveBandwidth = bandwidth / vpn.overhead;
        const throughput = (effectiveBandwidth * 1000) / 8; // Convert Mbps to KB/s
        
        // Calculate latency
        const effectiveLatency = baseLatency + vpn.latencyAdd + (cpuOverhead * vpn.cpuFactor);
        
        // Calculate transfer time (file size / throughput + latency)
        const transferTime = (fileSize / throughput) + (effectiveLatency / 1000);
        
        // Calculate efficiency (baseline throughput / actual throughput)
        const baselineThroughput = (bandwidth * 1000) / 8;
        const efficiency = ((baselineThroughput / throughput) * 100).toFixed(1);
        
        results.push({
            name: vpn.name,
            encryption: vpn.encryption,
            overhead: (vpn.overhead * 100).toFixed(0) + '%',
            latency: effectiveLatency.toFixed(1),
            throughput: throughput.toFixed(0),
            transferTime: transferTime.toFixed(2),
            efficiency: efficiency
        });
        
        const row = `
            <tr>
                <td><strong>${vpn.name}</strong></td>
                <td>${vpn.encryption}</td>
                <td>${(vpn.overhead * 100).toFixed(0)}%</td>
                <td>${effectiveLatency.toFixed(1)}</td>
                <td>${throughput.toFixed(0)}</td>
                <td>${transferTime.toFixed(2)}</td>
                <td class="${efficiency < 80 ? 'rating-low' : efficiency < 95 ? 'rating-medium' : 'rating-high'}">${efficiency}%</td>
            </tr>
        `;
        table.innerHTML += row;
    });
    
    document.getElementById('calcResults').style.display = 'block';
    
    // Update charts
    updateCalculatorCharts(results, vpns);
}

function updateCalculatorCharts(results, vpns) {
    const names = results.map(r => r.name);
    const latencies = results.map(r => parseFloat(r.latency));
    const throughputs = results.map(r => parseFloat(r.throughput));
    const transferTimes = results.map(r => parseFloat(r.transferTime));
    
    const colors = ['#28a745', '#667eea', '#764ba2', '#ffc107', '#e74c3c', '#17a2b8'];
    const bgColors = colors.map(c => c + '80');
    
    // Latency Chart
    const latencyCtx = document.getElementById('calcLatencyChart');
    if (latencyCtx && latencyCtx.chart) latencyCtx.chart.destroy();
    if (latencyCtx) {
        latencyCtx.chart = new Chart(latencyCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Latency (ms)',
                    data: latencies,
                    backgroundColor: bgColors,
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Latency Comparison', font: { size: 14 } },
                    legend: { display: false }
                },
                scales: { y: { beginAtZero: true, title: { display: true, text: 'ms' } } }
            }
        });
    }
    
    // Throughput Chart
    const throughputCtx = document.getElementById('calcThroughputChart');
    if (throughputCtx && throughputCtx.chart) throughputCtx.chart.destroy();
    if (throughputCtx) {
        throughputCtx.chart = new Chart(throughputCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Throughput (KB/s)',
                    data: throughputs,
                    backgroundColor: bgColors,
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Throughput Comparison', font: { size: 14 } },
                    legend: { display: false }
                },
                scales: { y: { beginAtZero: true, title: { display: true, text: 'KB/s' } } }
            }
        });
    }
    
    // Transfer Time Chart
    const transferCtx = document.getElementById('calcTransferChart');
    if (transferCtx && transferCtx.chart) transferCtx.chart.destroy();
    if (transferCtx) {
        transferCtx.chart = new Chart(transferCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: names,
                datasets: [{
                    label: 'Transfer Time (seconds)',
                    data: transferTimes,
                    backgroundColor: bgColors,
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'File Transfer Time', font: { size: 14 } },
                    legend: { display: false }
                },
                scales: { y: { beginAtZero: true, title: { display: true, text: 'seconds' } } }
            }
        });
    }
}
