# Quick-Real-Test.ps1 - Test nhanh XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$ServerUrl = "https://103.69.86.130:4433",
    [switch]$Verbose
)

Write-Host "🧪 QUICK REAL-WORLD TEST v2.0.0" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "Server URL: $ServerUrl" -ForegroundColor Yellow

$testResults = @{
    Total = 0
    Passed = 0
    Failed = 0
    StartTime = Get-Date
}

function Test-System {
    param([string]$TestName, [string]$Description, [scriptblock]$TestScript)
    
    $testResults.Total++
    Write-Host "`n🔍 $TestName" -ForegroundColor Yellow
    Write-Host "   $Description" -ForegroundColor Gray
    
    try {
        $result = & $TestScript
        if ($result) {
            $testResults.Passed++
            Write-Host "   ✅ PASSED" -ForegroundColor Green
        } else {
            $testResults.Failed++
            Write-Host "   ❌ FAILED" -ForegroundColor Red
        }
    } catch {
        $testResults.Failed++
        Write-Host "   ❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test 1: System Requirements
Test-System "System-Requirements" "Check PowerShell version and .NET Framework" {
    $psVersion = $PSVersionTable.PSVersion
    $dotNetVersion = [System.Environment]::Version
    return ($psVersion.Major -ge 5 -and $dotNetVersion.Major -ge 4)
}

# Test 2: Network Connectivity
Test-System "Network-Connectivity" "Test internet and MeshCentral server connectivity" {
    $internet = Test-NetConnection -ComputerName "8.8.8.8" -InformationLevel Quiet
    $meshcentral = Test-NetConnection -ComputerName "103.69.86.130" -Port 4433 -InformationLevel Quiet
    return ($internet -and $meshcentral)
}

# Test 3: MeshCentral Server
Test-System "MeshCentral-Server" "Test HTTPS connection to MeshCentral" {
    try {
        $response = Invoke-WebRequest -Uri $ServerUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
        return ($response.StatusCode -eq 200)
    } catch {
        return $false
    }
}

# Test 4: Core Files
Test-System "Core-Files" "Check XML Guard Core files exist" {
    $coreFiles = @(
        ".\Core\XML-Guard-Core.ps1",
        ".\Core\AI-Classifier.ps1",
        ".\Utils\Logger.ps1",
        ".\Utils\Config-Manager.ps1"
    )
    
    $allExist = $true
    foreach ($file in $coreFiles) {
        if (-not (Test-Path $file)) {
            $allExist = $false
            break
        }
    }
    return $allExist
}

# Test 5: Syntax Validation
Test-System "Syntax-Validation" "Validate PowerShell syntax" {
    $corePath = ".\Core\XML-Guard-Core.ps1"
    if (Test-Path $corePath) {
        try {
            $ast = [System.Management.Automation.Parser]::ParseFile($corePath, [ref]$null, [ref]$null)
            return $true
        } catch {
            return $false
        }
    }
    return $false
}

# Test 6: Performance
Test-System "Performance" "Check system performance" {
    $memory = Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Measure-Object -Property WorkingSet -Sum
    $memoryMB = [math]::Round($memory.Sum / 1MB, 2)
    return ($memoryMB -lt 500)
}

# Test 7: Build Output
Test-System "Build-Output" "Check build output exists" {
    $buildPath = ".\Build\Output"
    return (Test-Path $buildPath)
}

# Test 8: Launcher
Test-System "Launcher" "Check launcher script exists" {
    $launcherPath = ".\Build\Output\XML-Guard-Enterprise.ps1"
    return (Test-Path $launcherPath)
}

# Show Results
$endTime = Get-Date
$duration = $endTime - $testResults.StartTime

Write-Host "`n📊 TEST RESULTS" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "Total Tests: $($testResults.Total)" -ForegroundColor White
Write-Host "Passed: $($testResults.Passed)" -ForegroundColor Green
Write-Host "Failed: $($testResults.Failed)" -ForegroundColor Red
Write-Host "Duration: $([math]::Round($duration.TotalSeconds, 2))s" -ForegroundColor White

$successRate = if ($testResults.Total -gt 0) { [math]::Round(($testResults.Passed / $testResults.Total) * 100, 2) } else { 0 }
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

# Show system info
Write-Host "`n💻 SYSTEM INFORMATION" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host "PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host ".NET Framework: $([System.Environment]::Version)" -ForegroundColor White
Write-Host "OS: $([System.Environment]::OSVersion.VersionString)" -ForegroundColor White
Write-Host "Computer: $([System.Environment]::MachineName)" -ForegroundColor White

# Show network info
Write-Host "`n🌐 NETWORK INFORMATION" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "MeshCentral Server: $ServerUrl" -ForegroundColor White
Write-Host "Server IP: 103.69.86.130" -ForegroundColor White
Write-Host "Port: 4433" -ForegroundColor White
Write-Host "Protocol: HTTPS" -ForegroundColor White

# Show file structure
Write-Host "`n📁 PROJECT STRUCTURE" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
if (Test-Path ".\Build\Output") {
    $files = Get-ChildItem -Path ".\Build\Output" -Recurse
    Write-Host "Build Output Files: $($files.Count)" -ForegroundColor White
    foreach ($file in $files) {
        Write-Host "  - $($file.FullName)" -ForegroundColor Gray
    }
} else {
    Write-Host "Build output not found" -ForegroundColor Red
}

# Show usage instructions
Write-Host "`nUSAGE INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host "1. Navigate to build output:" -ForegroundColor White
Write-Host "   cd .\Build\Output" -ForegroundColor Gray
Write-Host "2. Start XML Guard:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Start" -ForegroundColor Gray
Write-Host "3. Check status:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Status" -ForegroundColor Gray
Write-Host "4. Stop XML Guard:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Stop" -ForegroundColor Gray

Write-Host "`n✅ Quick test completed!" -ForegroundColor Green
