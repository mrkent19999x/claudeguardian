# Simple-Test.ps1 - Test đơn giản XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

Write-Host "QUICK TEST XML GUARD ENTERPRISE v2.0.0" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$total = 0
$passed = 0
$failed = 0

# Test 1: System Requirements
$total++
Write-Host "`nTest 1: System Requirements" -ForegroundColor Yellow
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 5) {
    $passed++
    Write-Host "PASSED - PowerShell $($psVersion.ToString())" -ForegroundColor Green
} else {
    $failed++
    Write-Host "FAILED - PowerShell version too old" -ForegroundColor Red
}

# Test 2: Network Connectivity
$total++
Write-Host "`nTest 2: Network Connectivity" -ForegroundColor Yellow
$internet = Test-NetConnection -ComputerName "8.8.8.8" -InformationLevel Quiet
$meshcentral = Test-NetConnection -ComputerName "103.69.86.130" -Port 4433 -InformationLevel Quiet
if ($internet -and $meshcentral) {
    $passed++
    Write-Host "PASSED - Internet and MeshCentral accessible" -ForegroundColor Green
} else {
    $failed++
    Write-Host "FAILED - Network connectivity issues" -ForegroundColor Red
}

# Test 3: MeshCentral Server
$total++
Write-Host "`nTest 3: MeshCentral Server" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://103.69.86.130:4433" -Method GET -TimeoutSec 10 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $passed++
        Write-Host "PASSED - MeshCentral server accessible" -ForegroundColor Green
    } else {
        $failed++
        Write-Host "FAILED - HTTP Status: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    $failed++
    Write-Host "FAILED - Cannot connect to MeshCentral server" -ForegroundColor Red
}

# Test 4: Core Files
$total++
Write-Host "`nTest 4: Core Files" -ForegroundColor Yellow
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

if ($allExist) {
    $passed++
    Write-Host "PASSED - All core files exist" -ForegroundColor Green
} else {
    $failed++
    Write-Host "FAILED - Some core files missing" -ForegroundColor Red
}

# Test 5: Build Output
$total++
Write-Host "`nTest 5: Build Output" -ForegroundColor Yellow
if (Test-Path ".\Build\Output") {
    $passed++
    Write-Host "PASSED - Build output exists" -ForegroundColor Green
} else {
    $failed++
    Write-Host "FAILED - Build output not found" -ForegroundColor Red
}

# Test 6: Launcher
$total++
Write-Host "`nTest 6: Launcher" -ForegroundColor Yellow
if (Test-Path ".\Build\Output\XML-Guard-Enterprise.ps1") {
    $passed++
    Write-Host "PASSED - Launcher script exists" -ForegroundColor Green
} else {
    $failed++
    Write-Host "FAILED - Launcher script not found" -ForegroundColor Red
}

# Show Results
Write-Host "`nTEST RESULTS" -ForegroundColor Cyan
Write-Host "============" -ForegroundColor Cyan
Write-Host "Total Tests: $total" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red

$successRate = if ($total -gt 0) { [math]::Round(($passed / $total) * 100, 2) } else { 0 }
Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })

# Show system info
Write-Host "`nSYSTEM INFORMATION" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host ".NET Framework: $([System.Environment]::Version)" -ForegroundColor White
Write-Host "OS: $([System.Environment]::OSVersion.VersionString)" -ForegroundColor White
Write-Host "Computer: $([System.Environment]::MachineName)" -ForegroundColor White

# Show network info
Write-Host "`nNETWORK INFORMATION" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host "MeshCentral Server: https://103.69.86.130:4433" -ForegroundColor White
Write-Host "Server IP: 103.69.86.130" -ForegroundColor White
Write-Host "Port: 4433" -ForegroundColor White
Write-Host "Protocol: HTTPS" -ForegroundColor White

# Show file structure
Write-Host "`nPROJECT STRUCTURE" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
if (Test-Path ".\Build\Output") {
    $files = Get-ChildItem -Path ".\Build\Output" -Recurse
    Write-Host "Build Output Files: $($files.Count)" -ForegroundColor White
    foreach ($file in $files) {
        Write-Host "  - $($file.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "Build output not found" -ForegroundColor Red
}

# Show usage instructions
Write-Host "`nUSAGE INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host "1. Navigate to build output:" -ForegroundColor White
Write-Host "   cd .\Build\Output" -ForegroundColor Gray
Write-Host "2. Start XML Guard:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Start" -ForegroundColor Gray
Write-Host "3. Check status:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Status" -ForegroundColor Gray
Write-Host "4. Stop XML Guard:" -ForegroundColor White
Write-Host "   .\XML-Guard-Enterprise.ps1 -Stop" -ForegroundColor Gray

Write-Host "`nQuick test completed!" -ForegroundColor Green
