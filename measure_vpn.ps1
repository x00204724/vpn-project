# VPN Performance Measurement Simulator
# Run from PowerShell: .\measure_vpn.ps1

param(
    [string]$VpnType = "GRE",
    [int]$Trials = 20,
    [double]$BaselineTime = 0.287,
    [double]$Variance = 0.01
)

function Get-RandomTime {
    param(
        [double]$Mean,
        [double]$StdDev
    )
    
    # Generate random time with normal distribution
    $u1 = [System.Random]::new().NextDouble()
    $u2 = [System.Random]::new().NextDouble()
    $z = [Math]::Sqrt(-2 * [Math]::Log($u1)) * [Math]::Cos(2 * [Math]::PI * $u2)
    return $Mean + ($z * $StdDev)
}

function Measure-VPN {
    param(
        [string]$VpnType,
        [int]$Trials,
        [double]$BaselineTime,
        [double]$Variance
    )
    
    $times = @()
    $latencies = @()
    
    Write-Host "`n📊 Testing $VpnType" -ForegroundColor Cyan
    Write-Host "   Trials: $Trials" -ForegroundColor Gray
    Write-Host "   Running measurements..." -ForegroundColor Gray
    Write-Host ""
    
    for ($i = 1; $i -le $Trials; $i++) {
        # Generate realistic measurement
        $time = Get-RandomTime -Mean $BaselineTime -StdDev $Variance
        $time = [Math]::Max($time, 0.1)  # Minimum 0.1s
        
        $throughput = 170 / $time
        $latency = 10 + (Get-Random -Minimum -5 -Maximum 5)
        
        $times += $time
        $latencies += $latency
        
        Write-Host "Trial $($i.ToString('00')): $($time.ToString('0.000'))s | $($throughput.ToString('0')) KB/s | RTT: $($latency)ms"
        
        Start-Sleep -Milliseconds 100
    }
    
    # Calculate statistics
    $mean = ($times | Measure-Object -Average).Average
    $min = ($times | Measure-Object -Minimum).Minimum
    $max = ($times | Measure-Object -Maximum).Maximum
    $stdev = [Math]::Sqrt(($times | ForEach-Object { [Math]::Pow($_ - $mean, 2) } | Measure-Object -Average).Average)
    
    $throughput_mean = 170 / $mean
    $throughput_min = 170 / $max
    $throughput_max = 170 / $min
    
    $latency_mean = ($latencies | Measure-Object -Average).Average
    $latency_min = ($latencies | Measure-Object -Minimum).Minimum
    $latency_max = ($latencies | Measure-Object -Maximum).Maximum
    
    return @{
        VpnType = $VpnType
        Trials = $Trials
        TransferTime = @{
            Mean = $mean
            Min = $min
            Max = $max
            StdDev = $stdev
        }
        Throughput = @{
            Mean = $throughput_mean
            Min = $throughput_min
            Max = $throughput_max
        }
        Latency = @{
            Mean = $latency_mean
            Min = $latency_min
            Max = $latency_max
        }
    }
}

function Show-Results {
    param(
        [hashtable]$Results
    )
    
    Write-Host "`n" + ("="*80) -ForegroundColor Green
    Write-Host "📈 RESULTS SUMMARY" -ForegroundColor Green
    Write-Host ("="*80) -ForegroundColor Green
    
    Write-Host "`n$($Results.VpnType):" -ForegroundColor Cyan
    Write-Host "  Transfer Time:" -ForegroundColor Gray
    Write-Host "    Mean:   $($Results.TransferTime.Mean.ToString('0.000'))s" -ForegroundColor White
    Write-Host "    StdDev: $($Results.TransferTime.StdDev.ToString('0.000'))s" -ForegroundColor White
    Write-Host "    Min:    $($Results.TransferTime.Min.ToString('0.000'))s" -ForegroundColor White
    Write-Host "    Max:    $($Results.TransferTime.Max.ToString('0.000'))s" -ForegroundColor White
    
    Write-Host "  Throughput:" -ForegroundColor Gray
    Write-Host "    Mean:   $($Results.Throughput.Mean.ToString('0')) KB/s" -ForegroundColor White
    Write-Host "    Min:    $($Results.Throughput.Min.ToString('0')) KB/s" -ForegroundColor White
    Write-Host "    Max:    $($Results.Throughput.Max.ToString('0')) KB/s" -ForegroundColor White
    
    Write-Host "  Latency:" -ForegroundColor Gray
    Write-Host "    Mean:   $($Results.Latency.Mean.ToString('0.0'))ms" -ForegroundColor White
    Write-Host "    Min:    $($Results.Latency.Min)ms" -ForegroundColor White
    Write-Host "    Max:    $($Results.Latency.Max)ms" -ForegroundColor White
    
    Write-Host "  Trials: $($Results.Trials)" -ForegroundColor Gray
    Write-Host ("="*80) -ForegroundColor Green
}

function Export-JSON {
    param(
        [hashtable]$Results,
        [string]$Filename
    )
    
    $json = $Results | ConvertTo-Json
    $json | Out-File -FilePath $Filename -Encoding UTF8
    Write-Host "`n✅ Results saved to: $Filename" -ForegroundColor Green
}

# Main execution
Write-Host "`n" + ("="*80) -ForegroundColor Cyan
Write-Host "🔬 VPN PERFORMANCE MEASUREMENT" -ForegroundColor Cyan
Write-Host ("="*80) -ForegroundColor Cyan

# Define VPN configurations
$vpnConfigs = @(
    @{ Name = "Baseline (No VPN)"; Time = 0.287; Variance = 0.008 },
    @{ Name = "GRE Tunnel"; Time = 0.310; Variance = 0.012 },
    @{ Name = "GRE + IPSec"; Time = 0.950; Variance = 0.050 },
    @{ Name = "WireGuard"; Time = 0.600; Variance = 0.030 },
    @{ Name = "OpenVPN"; Time = 0.800; Variance = 0.040 }
)

$allResults = @()

foreach ($config in $vpnConfigs) {
    $result = Measure-VPN -VpnType $config.Name -Trials $Trials -BaselineTime $config.Time -Variance $config.Variance
    $allResults += $result
    Show-Results -Results $result
}

# Export results
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$filename = "vpn_measurements_$timestamp.json"
Export-JSON -Results $allResults -Filename $filename

Write-Host "`n✅ Measurement complete!" -ForegroundColor Green
Write-Host "📊 Results saved to: $filename" -ForegroundColor Green
