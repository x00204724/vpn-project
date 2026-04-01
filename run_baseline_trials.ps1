# Baseline VPN Performance - 20 Trials
# Run this script to measure file transfer times

$results = @()
$filesize = (Get-Item AliceInWonderland.txt).Length

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BASELINE VPN PERFORMANCE TEST - 20 TRIALS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "File: AliceInWonderland.txt" -ForegroundColor Yellow
Write-Host "Size: $filesize bytes (~170 KB)" -ForegroundColor Yellow
Write-Host "URL: http://localhost:8080/AliceInWonderland.txt" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

for ($i = 1; $i -le 20; $i++) {
    $start = Get-Date
    try {
        Invoke-WebRequest http://localhost:8080/AliceInWonderland.txt -OutFile "alice_trial_$i.txt" -ErrorAction Stop | Out-Null
        $end = Get-Date
        $time = ($end - $start).TotalSeconds
        $results += $time
        Write-Host "Trial $($i.ToString().PadLeft(2)): $($time.ToString('F4')) seconds" -ForegroundColor Green
    }
    catch {
        Write-Host "Trial $($i.ToString().PadLeft(2)): FAILED - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "STATISTICAL ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($results.Count -gt 0) {
    $average = ($results | Measure-Object -Average).Average
    $min = ($results | Measure-Object -Minimum).Minimum
    $max = ($results | Measure-Object -Maximum).Maximum
    $stdev = [Math]::Sqrt(($results | ForEach-Object {[Math]::Pow($_ - $average, 2)} | Measure-Object -Average).Average)
    $throughput = $filesize / $average / 1024
    
    Write-Host "Trials Completed: $($results.Count)" -ForegroundColor Yellow
    Write-Host "Average Time:     $($average.ToString('F4')) seconds" -ForegroundColor Yellow
    Write-Host "Min Time:         $($min.ToString('F4')) seconds" -ForegroundColor Yellow
    Write-Host "Max Time:         $($max.ToString('F4')) seconds" -ForegroundColor Yellow
    Write-Host "Std Deviation:    $($stdev.ToString('F4')) seconds" -ForegroundColor Yellow
    Write-Host "Throughput:       $($throughput.ToString('F2')) KB/s" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    # Save results to CSV
    $csv_data = @()
    for ($i = 0; $i -lt $results.Count; $i++) {
        $csv_data += [PSCustomObject]@{
            Trial = $i + 1
            TransferTime_Seconds = $results[$i]
            Throughput_KB_s = [Math]::Round($filesize / $results[$i] / 1024, 2)
        }
    }
    
    $csv_data | Export-Csv -Path "baseline_trials.csv" -NoTypeInformation
    Write-Host "Results saved to: baseline_trials.csv" -ForegroundColor Green
}
else {
    Write-Host "No successful trials!" -ForegroundColor Red
}

Write-Host "`nDone! Take a screenshot of this output." -ForegroundColor Cyan
