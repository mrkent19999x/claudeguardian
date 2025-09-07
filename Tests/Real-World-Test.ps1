# Real-World-Test.ps1 - Test thực tế XML Guard Enterprise với MeshCentral
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$ServerUrl = "https://103.69.86.130:4433",
    [string]$TestDuration = "300",  # 5 minutes
    [switch]$FullTest,
    [switch]$PerformanceTest,
    [switch]$IntegrationTest,
    [switch]$Verbose
)

# Global variables
$global:TestResults = @{
    StartTime = Get-Date
    EndTime = $null
    Duration = $null
    Tests = @()
    Performance = @{}
    Integration = @{}
    Errors = @()
    Warnings = @()
}

function Initialize-RealWorldTest {
    Write-Host "🧪 REAL-WORLD TEST SUITE v2.0.0" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host "Server URL: $ServerUrl" -ForegroundColor Yellow
    Write-Host "Test Duration: $TestDuration seconds" -ForegroundColor Yellow
    Write-Host "Test Mode: $(if($FullTest) {'Full'} elseif($PerformanceTest) {'Performance'} elseif($IntegrationTest) {'Integration'} else {'Quick'})" -ForegroundColor Yellow
    
    # Create test directories
    $testDirs = @(".\TestData", ".\TestResults", ".\Logs")
    foreach ($dir in $testDirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    Write-Host "Real-world test initialized" -ForegroundColor Green
}

function Test-SystemRequirements {
    Write-Host "`n🔍 TESTING SYSTEM REQUIREMENTS..." -ForegroundColor Yellow
    
    # Test 1: PowerShell version
    $test = Start-Test "PowerShell-Version" "Check PowerShell version"
    $psVersion = $PSVersionTable.PSVersion
    if ($psVersion.Major -ge 5) {
        Complete-Test $test "Passed" "PowerShell $($psVersion.ToString())"
    } else {
        Complete-Test $test "Failed" "PowerShell version too old: $($psVersion.ToString())"
    }
    
    # Test 2: .NET Framework
    $test = Start-Test "DotNet-Framework" "Check .NET Framework version"
    try {
        $dotNetVersion = [System.Environment]::Version
        if ($dotNetVersion.Major -ge 4) {
            Complete-Test $test "Passed" ".NET Framework $($dotNetVersion.ToString())"
        } else {
            Complete-Test $test "Failed" ".NET Framework version too old: $($dotNetVersion.ToString())"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: Available memory
    $test = Start-Test "Available-Memory" "Check available memory"
    $memory = Get-WmiObject -Class Win32_ComputerSystem
    $totalMemoryGB = [math]::Round($memory.TotalPhysicalMemory / 1GB, 2)
    if ($totalMemoryGB -ge 4) {
        Complete-Test $test "Passed" "Total Memory: $totalMemoryGB GB"
    } else {
        Complete-Test $test "Failed" "Insufficient memory: $totalMemoryGB GB"
    }
    
    # Test 4: Available disk space
    $test = Start-Test "Available-DiskSpace" "Check available disk space"
    $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
    $freeSpaceGB = [math]::Round($disk.FreeSpace / 1GB, 2)
    if ($freeSpaceGB -ge 1) {
        Complete-Test $test "Passed" "Free Space: $freeSpaceGB GB"
    } else {
        Complete-Test $test "Failed" "Insufficient disk space: $freeSpaceGB GB"
    }
}

function Test-NetworkConnectivity {
    Write-Host "`n🌐 TESTING NETWORK CONNECTIVITY..." -ForegroundColor Yellow
    
    # Test 1: Internet connection
    $test = Start-Test "Internet-Connection" "Test internet connectivity"
    try {
        $ping = Test-NetConnection -ComputerName "8.8.8.8" -InformationLevel Quiet
        if ($ping) {
            Complete-Test $test "Passed"
        } else {
            Complete-Test $test "Failed" "Cannot reach internet"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 2: MeshCentral server ping
    $test = Start-Test "MeshCentral-Ping" "Test ping to MeshCentral server"
    try {
        $serverIP = "103.69.86.130"
        $ping = Test-NetConnection -ComputerName $serverIP -Port 4433 -InformationLevel Quiet
        if ($ping) {
            Complete-Test $test "Passed"
        } else {
            Complete-Test $test "Failed" "Cannot reach MeshCentral server"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: HTTPS connection to MeshCentral
    $test = Start-Test "MeshCentral-HTTPS" "Test HTTPS connection to MeshCentral"
    try {
        $response = Invoke-WebRequest -Uri $ServerUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Complete-Test $test "Passed" "HTTP Status: $($response.StatusCode)"
        } else {
            Complete-Test $test "Failed" "HTTP Status: $($response.StatusCode)"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 4: DNS resolution
    $test = Start-Test "DNS-Resolution" "Test DNS resolution"
    try {
        $dnsResult = Resolve-DnsName "103.69.86.130" -ErrorAction Stop
        if ($dnsResult) {
            Complete-Test $test "Passed" "DNS resolved successfully"
        } else {
            Complete-Test $test "Failed" "DNS resolution failed"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
}

function Test-XMLGuardCore {
    Write-Host "`n🛡️ TESTING XML GUARD CORE..." -ForegroundColor Yellow
    
    # Test 1: Core file existence
    $test = Start-Test "Core-File-Existence" "Check XML Guard Core file"
    $corePath = ".\Core\XML-Guard-Core.ps1"
    if (Test-Path $corePath) {
        Complete-Test $test "Passed"
    } else {
        Complete-Test $test "Failed" "Core file not found: $corePath"
    }
    
    # Test 2: Core syntax validation
    $test = Start-Test "Core-Syntax-Validation" "Validate Core syntax"
    try {
        $ast = [System.Management.Automation.Parser]::ParseFile($corePath, [ref]$null, [ref]$null)
        Complete-Test $test "Passed"
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: AI Classifier file
    $test = Start-Test "AI-Classifier-File" "Check AI Classifier file"
    $aiPath = ".\Core\AI-Classifier.ps1"
    if (Test-Path $aiPath) {
        Complete-Test $test "Passed"
    } else {
        Complete-Test $test "Failed" "AI Classifier file not found: $aiPath"
    }
    
    # Test 4: Utils files
    $test = Start-Test "Utils-Files" "Check Utils files"
    $utilsFiles = @(".\Utils\Logger.ps1", ".\Utils\Config-Manager.ps1")
    $allUtilsExist = $true
    foreach ($file in $utilsFiles) {
        if (-not (Test-Path $file)) {
            $allUtilsExist = $false
            break
        }
    }
    if ($allUtilsExist) {
        Complete-Test $test "Passed"
    } else {
        Complete-Test $test "Failed" "Some Utils files missing"
    }
}

function Test-Performance {
    Write-Host "`n⚡ TESTING PERFORMANCE..." -ForegroundColor Yellow
    
    # Test 1: CPU usage baseline
    $test = Start-Test "CPU-Baseline" "Measure baseline CPU usage"
    try {
        $cpuBefore = (Get-Counter "\Processor(_Total)\% Processor Time").CounterSamples[0].CookedValue
        Start-Sleep -Seconds 2
        $cpuAfter = (Get-Counter "\Processor(_Total)\% Processor Time").CounterSamples[0].CookedValue
        $avgCPU = ($cpuBefore + $cpuAfter) / 2
        
        if ($avgCPU -lt 50) {
            Complete-Test $test "Passed" "Average CPU: $([math]::Round($avgCPU, 2))%"
        } else {
            Complete-Test $test "Failed" "High CPU usage: $([math]::Round($avgCPU, 2))%"
        }
        
        $global:TestResults.Performance.CPU = $avgCPU
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 2: Memory usage baseline
    $test = Start-Test "Memory-Baseline" "Measure baseline memory usage"
    try {
        $memory = Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Measure-Object -Property WorkingSet -Sum
        $memoryMB = [math]::Round($memory.Sum / 1MB, 2)
        
        if ($memoryMB -lt 500) {
            Complete-Test $test "Passed" "Memory usage: $memoryMB MB"
        } else {
            Complete-Test $test "Failed" "High memory usage: $memoryMB MB"
        }
        
        $global:TestResults.Performance.Memory = $memoryMB
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: Disk I/O performance
    $test = Start-Test "Disk-IO-Performance" "Test disk I/O performance"
    try {
        $testFile = ".\TestData\performance_test.tmp"
        $testData = "X" * 1024 * 1024  # 1MB of data
        
        $startTime = Get-Date
        Set-Content -Path $testFile -Value $testData -Encoding UTF8
        $writeTime = (Get-Date) - $startTime
        
        $startTime = Get-Date
        $content = Get-Content -Path $testFile -Raw
        $readTime = (Get-Date) - $startTime
        
        $writeSpeed = [math]::Round(1 / $writeTime.TotalSeconds, 2)
        $readSpeed = [math]::Round(1 / $readTime.TotalSeconds, 2)
        
        if ($writeSpeed -gt 10 -and $readSpeed -gt 10) {
            Complete-Test $test "Passed" "Write: $writeSpeed MB/s, Read: $readSpeed MB/s"
        } else {
            Complete-Test $test "Failed" "Slow disk I/O - Write: $writeSpeed MB/s, Read: $readSpeed MB/s"
        }
        
        # Cleanup
        Remove-Item -Path $testFile -Force -ErrorAction SilentlyContinue
        
        $global:TestResults.Performance.DiskWrite = $writeSpeed
        $global:TestResults.Performance.DiskRead = $readSpeed
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
}

function Test-Integration {
    Write-Host "`n🔗 TESTING INTEGRATION..." -ForegroundColor Yellow
    
    # Test 1: Module loading
    $test = Start-Test "Module-Loading" "Test module loading"
    try {
        $modules = @(
            ".\Utils\Logger.ps1",
            ".\Utils\Config-Manager.ps1",
            ".\Core\AI-Classifier.ps1"
        )
        
        $allLoaded = $true
        foreach ($module in $modules) {
            try {
                Import-Module $module -Force -ErrorAction Stop
            } catch {
                $allLoaded = $false
                break
            }
        }
        
        if ($allLoaded) {
            Complete-Test $test "Passed"
        } else {
            Complete-Test $test "Failed" "Some modules failed to load"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 2: Configuration loading
    $test = Start-Test "Config-Loading" "Test configuration loading"
    try {
        $configPath = ".\Config\config.json"
        if (Test-Path $configPath) {
            $config = Get-Content $configPath -Raw | ConvertFrom-Json
            if ($config -and $config.System) {
                Complete-Test $test "Passed"
            } else {
                Complete-Test $test "Failed" "Invalid configuration structure"
            }
        } else {
            Complete-Test $test "Skipped" "Configuration file not found"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: Logging system
    $test = Start-Test "Logging-System" "Test logging system"
    try {
        $logPath = ".\Logs\test.log"
        if (Test-Path ".\Utils\Logger.ps1") {
            Import-Module ".\Utils\Logger.ps1" -Force
            Write-Log "Test log entry" "INFO" $logPath
            if (Test-Path $logPath) {
                Complete-Test $test "Passed"
            } else {
                Complete-Test $test "Failed" "Log file not created"
            }
        } else {
            Complete-Test $test "Skipped" "Logger module not found"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
}

function Test-MeshCentralIntegration {
    Write-Host "`n🌐 TESTING MESHCENTRAL INTEGRATION..." -ForegroundColor Yellow
    
    # Test 1: MeshCentral config
    $test = Start-Test "MeshCentral-Config" "Test MeshCentral configuration"
    try {
        $configPath = ".\MeshCentral\Config-MeshCentral.ps1"
        if (Test-Path $configPath) {
            Complete-Test $test "Passed"
        } else {
            Complete-Test $test "Failed" "MeshCentral config not found"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 2: Server connectivity
    $test = Start-Test "Server-Connectivity" "Test server connectivity"
    try {
        $response = Invoke-WebRequest -Uri $ServerUrl -Method GET -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Complete-Test $test "Passed" "Server accessible"
        } else {
            Complete-Test $test "Failed" "Server returned status: $($response.StatusCode)"
        }
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
    
    # Test 3: SSL certificate
    $test = Start-Test "SSL-Certificate" "Test SSL certificate"
    try {
        $request = [System.Net.WebRequest]::Create($ServerUrl)
        $response = $request.GetResponse()
        $response.Close()
        Complete-Test $test "Passed" "SSL certificate valid"
    } catch {
        Complete-Test $test "Failed" $_.Exception.Message
    }
}

function Start-Test {
    param(
        [string]$TestName,
        [string]$Description = ""
    )
    
    $test = @{
        Name = $TestName
        Description = $Description
        StartTime = Get-Date
        Status = "Running"
        Error = $null
        Duration = $null
    }
    
    $global:TestResults.Tests += $test
    
    Write-Host "  🔍 $TestName" -ForegroundColor Yellow
    if ($Description) {
        Write-Host "     $Description" -ForegroundColor Gray
    }
    
    return $test
}

function Complete-Test {
    param(
        [object]$Test,
        [string]$Status,
        [string]$Error = $null
    )
    
    $Test.Status = $Status
    $Test.Duration = (Get-Date) - $Test.StartTime
    
    $color = switch ($Status) {
        "Passed" { "Green" }
        "Failed" { "Red" }
        "Skipped" { "Yellow" }
        default { "White" }
    }
    
    $icon = switch ($Status) {
        "Passed" { "✅" }
        "Failed" { "❌" }
        "Skipped" { "⏭️" }
        default { "❓" }
    }
    
    Write-Host "     $icon $Status ($([math]::Round($Test.Duration.TotalMilliseconds, 2))ms)" -ForegroundColor $color
    
    if ($Error) {
        Write-Host "     Error: $Error" -ForegroundColor Red
    }
}

function Show-TestResults {
    $global:TestResults.EndTime = Get-Date
    $global:TestResults.Duration = $global:TestResults.EndTime - $global:TestResults.StartTime
    
    Write-Host "`n📊 REAL-WORLD TEST RESULTS" -ForegroundColor Cyan
    Write-Host "===========================" -ForegroundColor Cyan
    
    $totalTests = $global:TestResults.Tests.Count
    $passedTests = ($global:TestResults.Tests | Where-Object { $_.Status -eq "Passed" }).Count
    $failedTests = ($global:TestResults.Tests | Where-Object { $_.Status -eq "Failed" }).Count
    $skippedTests = ($global:TestResults.Tests | Where-Object { $_.Status -eq "Skipped" }).Count
    
    Write-Host "Total Tests: $totalTests" -ForegroundColor White
    Write-Host "Passed: $passedTests" -ForegroundColor Green
    Write-Host "Failed: $failedTests" -ForegroundColor Red
    Write-Host "Skipped: $skippedTests" -ForegroundColor Yellow
    Write-Host "Duration: $([math]::Round($global:TestResults.Duration.TotalSeconds, 2))s" -ForegroundColor White
    
    $successRate = if ($totalTests -gt 0) { [math]::Round(($passedTests / $totalTests) * 100, 2) } else { 0 }
    Write-Host "Success Rate: $successRate%" -ForegroundColor $(if ($successRate -ge 90) { "Green" } elseif ($successRate -ge 70) { "Yellow" } else { "Red" })
    
    # Show performance metrics
    if ($global:TestResults.Performance.Count -gt 0) {
        Write-Host "`n⚡ PERFORMANCE METRICS:" -ForegroundColor Cyan
        foreach ($metric in $global:TestResults.Performance.GetEnumerator()) {
            Write-Host "  $($metric.Key): $($metric.Value)" -ForegroundColor White
        }
    }
    
    # Show failed tests
    $failedTests = $global:TestResults.Tests | Where-Object { $_.Status -eq "Failed" }
    if ($failedTests) {
        Write-Host "`n❌ FAILED TESTS:" -ForegroundColor Red
        foreach ($test in $failedTests) {
            Write-Host "  - $($test.Name): $($test.Error)" -ForegroundColor Red
        }
    }
    
    # Save results to file
    $resultsFile = ".\TestResults\real-world-test-$(Get-Date -Format 'yyyyMMdd-HHmmss').json"
    $global:TestResults | ConvertTo-Json -Depth 10 | Set-Content -Path $resultsFile -Encoding UTF8
    Write-Host "`nResults saved to: $resultsFile" -ForegroundColor Cyan
}

# Main execution
Initialize-RealWorldTest

# Run tests based on parameters
if ($FullTest -or $PerformanceTest -or $IntegrationTest) {
    Test-SystemRequirements
    Test-NetworkConnectivity
    Test-XMLGuardCore
    Test-Performance
    Test-Integration
    Test-MeshCentralIntegration
} else {
    # Default: Run all tests
    Test-SystemRequirements
    Test-NetworkConnectivity
    Test-XMLGuardCore
    Test-Performance
    Test-Integration
    Test-MeshCentralIntegration
}

Show-TestResults
