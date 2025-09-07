# Build-All.ps1 - Build system hoàn chỉnh cho XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$Mode = "Full",  # Quick, Full, Release
    [string]$OutputPath = ".\Build\Output",
    [string]$Version = "2.0.0",
    [switch]$Clean,
    [switch]$Test,
    [switch]$Package,
    [switch]$Deploy,
    [switch]$Verbose
)

# Global variables
$global:BuildConfig = @{
    Mode = $Mode
    OutputPath = $OutputPath
    Version = $Version
    ProjectName = "XML-Guard-Enterprise"
    BuildStartTime = Get-Date
    BuildSteps = @()
    Errors = @()
    Warnings = @()
}

function Initialize-Build {
    Write-Host "🔨 XML GUARD ENTERPRISE BUILD SYSTEM v2.0.0" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    Write-Host "Mode: $Mode" -ForegroundColor Yellow
    Write-Host "Output: $OutputPath" -ForegroundColor Yellow
    Write-Host "Version: $Version" -ForegroundColor Yellow
    
    # Create output directory
    if (-not (Test-Path $OutputPath)) {
        New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    }
    
    # Clean if requested
    if ($Clean) {
        Write-Host "🧹 Cleaning build directory..." -ForegroundColor Yellow
        if (Test-Path $OutputPath) {
            Remove-Item -Path $OutputPath -Recurse -Force -ErrorAction SilentlyContinue
        }
        New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    }
    
    Write-Host "Build system initialized" -ForegroundColor Green
}

function Add-BuildStep {
    param(
        [string]$Name,
        [string]$Description = "",
        [scriptblock]$ScriptBlock
    )
    
    $step = @{
        Name = $Name
        Description = $Description
        StartTime = Get-Date
        Status = "Running"
        Error = $null
        Duration = $null
    }
    
    $global:BuildConfig.BuildSteps += $step
    
    Write-Host "`n🔧 $Name" -ForegroundColor Yellow
    if ($Description) {
        Write-Host "   $Description" -ForegroundColor Gray
    }
    
    try {
        & $ScriptBlock
        $step.Status = "Completed"
        Write-Host "✅ $Name completed" -ForegroundColor Green
    } catch {
        $step.Status = "Failed"
        $step.Error = $_.Exception.Message
        $global:BuildConfig.Errors += "$Name`: $($_.Exception.Message)"
        Write-Host "❌ $Name failed: $($_.Exception.Message)" -ForegroundColor Red
    } finally {
        $step.Duration = (Get-Date) - $step.StartTime
        Write-Host "   Duration: $([math]::Round($step.Duration.TotalMilliseconds, 2))ms" -ForegroundColor Gray
    }
}

function Step-ValidateProject {
    Add-BuildStep "Validate-Project" "Validate project structure and files" {
        $requiredFiles = @(
            ".\Core\XML-Guard-Core.ps1",
            ".\Core\AI-Classifier.ps1",
            ".\Utils\Logger.ps1",
            ".\Utils\Config-Manager.ps1",
            ".\Tests\Test-Suite.ps1"
        )
        
        $missingFiles = @()
        foreach ($file in $requiredFiles) {
            if (-not (Test-Path $file)) {
                $missingFiles += $file
            }
        }
        
        if ($missingFiles.Count -gt 0) {
            throw "Missing required files: $($missingFiles -join ', ')"
        }
        
        Write-Host "   All required files found" -ForegroundColor Green
    }
}

function Step-RunTests {
    if ($Test) {
        Add-BuildStep "Run-Tests" "Run test suite" {
            $testPath = ".\Tests\Test-Suite.ps1"
            if (Test-Path $testPath) {
                $testOutput = & powershell -ExecutionPolicy Bypass -File $testPath -All
                if ($LASTEXITCODE -ne 0) {
                    throw "Test suite failed with exit code $LASTEXITCODE"
                }
                Write-Host "   Test suite completed successfully" -ForegroundColor Green
            } else {
                throw "Test suite not found: $testPath"
            }
        }
    }
}

function Step-CopyFiles {
    Add-BuildStep "Copy-Files" "Copy project files to output directory" {
        $sourceDirs = @(
            "Core",
            "Utils",
            "Tests",
            "Docs"
        )
        
        foreach ($dir in $sourceDirs) {
            if (Test-Path $dir) {
                $destDir = Join-Path $OutputPath $dir
                if (-not (Test-Path $destDir)) {
                    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                }
                
                Copy-Item -Path "$dir\*" -Destination $destDir -Recurse -Force
                Write-Host "   Copied $dir" -ForegroundColor Green
            }
        }
        
        # Copy root files
        $rootFiles = @(
            "README.md",
            "CHANGELOG.md"
        )
        
        foreach ($file in $rootFiles) {
            if (Test-Path $file) {
                Copy-Item -Path $file -Destination $OutputPath -Force
                Write-Host "   Copied $file" -ForegroundColor Green
            }
        }
    }
}

function Step-CreateConfig {
    Add-BuildStep "Create-Config" "Create default configuration" {
        $configDir = Join-Path $OutputPath "Config"
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }
        
        $defaultConfig = @{
            System = @{
                Name = "XML Guard Enterprise"
                Version = $Version
                LogLevel = "INFO"
                MaxLogSize = "10MB"
                MaxLogFiles = 5
            }
            Performance = @{
                MaxConcurrentFiles = 5
                FileCheckInterval = 30
                HeartbeatInterval = 120
                SleepInterval = 30
                ProcessPriority = "BelowNormal"
            }
            AI = @{
                WhitelistPath = ".\Config\whitelist.json"
                Patterns = @{
                    MST = @("//MST", "//mst", "//MaSoThue")
                    FormCode = @("//MauSo", "//Form", "//FormCode")
                    Period = @("//KyKKhaiThang", "//Thang", "//Nam")
                }
                KnownForms = @("01/GTGT", "05/KK-TNCN", "03/TNDN", "BC26/AC")
            }
            Watchdog = @{
                Enabled = $true
                CheckInterval = 30
                MaxRetries = 3
                CooldownPeriod = 60
                HealthCheckInterval = 60
            }
            MeshCentral = @{
                Enabled = $true
                ServerUrl = "https://meshcentral.example.com"
                AgentId = ""
                PingInterval = 60
                Timeout = 10
            }
            FileWatcher = @{
                MaxWatchers = 3
                DebounceSeconds = 2
                WatchPaths = @("C:\", "D:\", "E:\")
                FileFilters = @("*.xml")
            }
            Security = @{
                RequireAdmin = $true
                EncryptLogs = $false
                BackupOriginal = $true
                BackupPath = ".\Backups"
            }
        }
        
        $configFile = Join-Path $configDir "config.json"
        $defaultConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $configFile -Encoding UTF8
        Write-Host "   Created default config: $configFile" -ForegroundColor Green
    }
}

function Step-CreateWhitelist {
    Add-BuildStep "Create-Whitelist" "Create sample whitelist" {
        $configDir = Join-Path $OutputPath "Config"
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }
        
        $sampleWhitelist = @(
            @{
                fileNamePattern = "ETAX.*\.xml"
                mst = "1234567890"
                formCode = "01/GTGT"
                periodType = "MONTH"
                periodValue = "2025-01"
                sourcePath = ".\Sample-Data\original.xml"
                sha256 = "sample_hash_here"
            }
        )
        
        $whitelistFile = Join-Path $configDir "whitelist.json"
        $sampleWhitelist | ConvertTo-Json -Depth 10 | Set-Content -Path $whitelistFile -Encoding UTF8
        Write-Host "   Created sample whitelist: $whitelistFile" -ForegroundColor Green
    }
}

function Step-CreateLauncher {
    Add-BuildStep "Create-Launcher" "Create launcher script" {
        $launcherContent = @"
# XML Guard Enterprise Launcher
# Version: $Version
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

param(
    [switch]`$Start,
    [switch]`$Stop,
    [switch]`$Restart,
    [switch]`$Status,
    [switch]`$Debug
)

`$scriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$corePath = Join-Path `$scriptDir "Core\XML-Guard-Core.ps1"

if (Test-Path `$corePath) {
    & `$corePath -Start:`$Start -Stop:`$Stop -Restart:`$Restart -Status:`$Status -Debug:`$Debug
} else {
    Write-Host "Error: Core file not found: `$corePath" -ForegroundColor Red
    exit 1
}
"@
        
        $launcherFile = Join-Path $OutputPath "XML-Guard-Enterprise.ps1"
        Set-Content -Path $launcherFile -Value $launcherContent -Encoding UTF8
        Write-Host "   Created launcher: $launcherFile" -ForegroundColor Green
    }
}

function Step-CreateInstaller {
    if ($Package) {
        Add-BuildStep "Create-Installer" "Create installer package" {
            $installerContent = @"
# XML Guard Enterprise Installer
# Version: $Version

param(
    [string]`$InstallPath = "C:\XML-Guard-Enterprise",
    [switch]`$Silent
)

Write-Host "Installing XML Guard Enterprise v$Version..." -ForegroundColor Green

# Create installation directory
if (-not (Test-Path `$InstallPath)) {
    New-Item -ItemType Directory -Path `$InstallPath -Force | Out-Null
}

# Copy files
Copy-Item -Path ".\*" -Destination `$InstallPath -Recurse -Force

# Create shortcuts
`$desktop = [Environment]::GetFolderPath("Desktop")
`$shortcut = Join-Path `$desktop "XML Guard Enterprise.lnk"
`$wshShell = New-Object -ComObject WScript.Shell
`$shortcutObj = `$wshShell.CreateShortcut(`$shortcut)
`$shortcutObj.TargetPath = "powershell.exe"
`$shortcutObj.Arguments = "-ExecutionPolicy Bypass -File `"`$InstallPath\XML-Guard-Enterprise.ps1`" -Start"
`$shortcutObj.Save()

Write-Host "Installation completed!" -ForegroundColor Green
Write-Host "Installation path: `$InstallPath" -ForegroundColor Yellow
Write-Host "Desktop shortcut created" -ForegroundColor Yellow
"@
            
            $installerFile = Join-Path $OutputPath "Install.ps1"
            Set-Content -Path $installerFile -Value $installerContent -Encoding UTF8
            Write-Host "   Created installer: $installerFile" -ForegroundColor Green
        }
    }
}

function Step-CreateDocumentation {
    Add-BuildStep "Create-Documentation" "Create documentation" {
        $docsDir = Join-Path $OutputPath "Docs"
        if (-not (Test-Path $docsDir)) {
            New-Item -ItemType Directory -Path $docsDir -Force | Out-Null
        }
        
        # Create API documentation
        $apiDoc = @"
# XML Guard Enterprise API Reference

## Core Functions

### XML-Guard-Core.ps1
- `Start-XMLGuard` - Start the XML Guard system
- `Stop-XMLGuard` - Stop the XML Guard system
- `Restart-XMLGuard` - Restart the XML Guard system
- `Get-XMLGuardStatus` - Get system status

### AI-Classifier.ps1
- `Classify-XML` - Classify XML file
- `Extract-MST` - Extract MST from XML
- `Extract-FormCode` - Extract Form Code from XML
- `Extract-Period` - Extract Period from XML

### Logger.ps1
- `Write-Log` - Write log entry
- `Get-LogEntries` - Get log entries
- `Clear-LogFile` - Clear log file
- `Set-LogLevel` - Set log level

### Config-Manager.ps1
- `Get-Config` - Get configuration
- `Set-ConfigValue` - Set configuration value
- `Validate-Config` - Validate configuration
- `Reset-Config` - Reset to default configuration

## Usage Examples

### Start XML Guard
```powershell
.\XML-Guard-Enterprise.ps1 -Start
```

### Check Status
```powershell
.\XML-Guard-Enterprise.ps1 -Status
```

### Stop XML Guard
```powershell
.\XML-Guard-Enterprise.ps1 -Stop
```
"@
        
        $apiFile = Join-Path $docsDir "API-Reference.md"
        Set-Content -Path $apiFile -Value $apiDoc -Encoding UTF8
        Write-Host "   Created API documentation: $apiFile" -ForegroundColor Green
    }
}

function Show-BuildResults {
    $endTime = Get-Date
    $totalDuration = $endTime - $global:BuildConfig.BuildStartTime
    
    Write-Host "`n📊 BUILD RESULTS" -ForegroundColor Cyan
    Write-Host "================" -ForegroundColor Cyan
    Write-Host "Total Steps: $($global:BuildConfig.BuildSteps.Count)" -ForegroundColor White
    Write-Host "Completed: $(($global:BuildConfig.BuildSteps | Where-Object { $_.Status -eq 'Completed' }).Count)" -ForegroundColor Green
    Write-Host "Failed: $(($global:BuildConfig.BuildSteps | Where-Object { $_.Status -eq 'Failed' }).Count)" -ForegroundColor Red
    Write-Host "Duration: $([math]::Round($totalDuration.TotalSeconds, 2))s" -ForegroundColor White
    
    if ($global:BuildConfig.Errors.Count -gt 0) {
        Write-Host "`n❌ ERRORS:" -ForegroundColor Red
        foreach ($error in $global:BuildConfig.Errors) {
            Write-Host "  - $error" -ForegroundColor Red
        }
    }
    
    if ($global:BuildConfig.Warnings.Count -gt 0) {
        Write-Host "`n⚠️ WARNINGS:" -ForegroundColor Yellow
        foreach ($warning in $global:BuildConfig.Warnings) {
            Write-Host "  - $warning" -ForegroundColor Yellow
        }
    }
    
    Write-Host "`n📁 OUTPUT:" -ForegroundColor Cyan
    Write-Host "Build output: $OutputPath" -ForegroundColor White
    
    if (Test-Path $OutputPath) {
        $files = Get-ChildItem -Path $OutputPath -Recurse
        Write-Host "Files created: $($files.Count)" -ForegroundColor White
    }
}

# Main execution
Initialize-Build

# Run build steps based on mode
if ($Mode -eq "Quick") {
    Step-ValidateProject
    Step-CopyFiles
    Step-CreateLauncher
} elseif ($Mode -eq "Full") {
    Step-ValidateProject
    Step-RunTests
    Step-CopyFiles
    Step-CreateConfig
    Step-CreateWhitelist
    Step-CreateLauncher
    Step-CreateDocumentation
} elseif ($Mode -eq "Release") {
    Step-ValidateProject
    Step-RunTests
    Step-CopyFiles
    Step-CreateConfig
    Step-CreateWhitelist
    Step-CreateLauncher
    Step-CreateInstaller
    Step-CreateDocumentation
}

Show-BuildResults
