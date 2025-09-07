# Simple-Build.ps1 - Build script đơn giản cho XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$OutputPath = ".\Build\Output",
    [string]$Version = "2.0.0",
    [switch]$Clean
)

Write-Host "🔨 XML GUARD ENTERPRISE SIMPLE BUILD v2.0.0" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# Create output directory
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    Write-Host "✅ Created output directory: $OutputPath" -ForegroundColor Green
}

# Clean if requested
if ($Clean) {
    Write-Host "🧹 Cleaning build directory..." -ForegroundColor Yellow
    if (Test-Path $OutputPath) {
        Remove-Item -Path $OutputPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
    Write-Host "✅ Cleaned build directory" -ForegroundColor Green
}

# Copy Core files
Write-Host "`n📁 Copying Core files..." -ForegroundColor Yellow
$coreDir = Join-Path $OutputPath "Core"
if (-not (Test-Path $coreDir)) {
    New-Item -ItemType Directory -Path $coreDir -Force | Out-Null
}

$coreFiles = @(
    ".\Core\XML-Guard-Core.ps1",
    ".\Core\AI-Classifier.ps1"
)

foreach ($file in $coreFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $coreDir -Force
        Write-Host "  ✅ Copied $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Not found: $file" -ForegroundColor Red
    }
}

# Copy Utils files
Write-Host "`n📁 Copying Utils files..." -ForegroundColor Yellow
$utilsDir = Join-Path $OutputPath "Utils"
if (-not (Test-Path $utilsDir)) {
    New-Item -ItemType Directory -Path $utilsDir -Force | Out-Null
}

$utilsFiles = @(
    ".\Utils\Logger.ps1",
    ".\Utils\Config-Manager.ps1"
)

foreach ($file in $utilsFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $utilsDir -Force
        Write-Host "  ✅ Copied $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Not found: $file" -ForegroundColor Red
    }
}

# Copy Tests files
Write-Host "`n📁 Copying Tests files..." -ForegroundColor Yellow
$testsDir = Join-Path $OutputPath "Tests"
if (-not (Test-Path $testsDir)) {
    New-Item -ItemType Directory -Path $testsDir -Force | Out-Null
}

$testsFiles = @(
    ".\Tests\Test-Suite.ps1"
)

foreach ($file in $testsFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $testsDir -Force
        Write-Host "  ✅ Copied $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Not found: $file" -ForegroundColor Red
    }
}

# Create Config directory
Write-Host "`n📁 Creating Config directory..." -ForegroundColor Yellow
$configDir = Join-Path $OutputPath "Config"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Create default config
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
Write-Host "  ✅ Created default config: config.json" -ForegroundColor Green

# Create sample whitelist
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
Write-Host "  ✅ Created sample whitelist: whitelist.json" -ForegroundColor Green

# Create launcher script
Write-Host "`n📁 Creating launcher script..." -ForegroundColor Yellow
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
Write-Host "  ✅ Created launcher: XML-Guard-Enterprise.ps1" -ForegroundColor Green

# Copy README
Write-Host "`n📁 Copying documentation..." -ForegroundColor Yellow
$readmeFiles = @(
    ".\README.md"
)

foreach ($file in $readmeFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $OutputPath -Force
        Write-Host "  ✅ Copied $(Split-Path $file -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Not found: $file" -ForegroundColor Red
    }
}

# Show results
Write-Host "`n📊 BUILD COMPLETED" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "Output Path: $OutputPath" -ForegroundColor White
Write-Host "Version: $Version" -ForegroundColor White

if (Test-Path $OutputPath) {
    $files = Get-ChildItem -Path $OutputPath -Recurse
    Write-Host "Files created: $($files.Count)" -ForegroundColor White
}

Write-Host "`n💡 USAGE:" -ForegroundColor Yellow
Write-Host "1. Navigate to: $OutputPath" -ForegroundColor White
Write-Host "2. Run: .\XML-Guard-Enterprise.ps1 -Start" -ForegroundColor White
Write-Host "3. Check status: .\XML-Guard-Enterprise.ps1 -Status" -ForegroundColor White
Write-Host "4. Stop: .\XML-Guard-Enterprise.ps1 -Stop" -ForegroundColor White

Write-Host "`n✅ Build completed successfully!" -ForegroundColor Green
