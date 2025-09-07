# Config-Manager.ps1 - Quản lý cấu hình cho XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$ConfigPath = ".\Config\config.json",
    [string]$Key,
    [object]$Value,
    [switch]$Get,
    [switch]$Set,
    [switch]$Reset,
    [switch]$Validate
)

# Global variables
$global:ConfigManager = @{
    ConfigPath = $ConfigPath
    Config = $null
    DefaultConfig = @{
        System = @{
            Name = "XML Guard Enterprise"
            Version = "2.0.0"
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
}

function Initialize-ConfigManager {
    param([string]$ConfigPath = ".\Config\config.json")
    
    try {
        $global:ConfigManager.ConfigPath = $ConfigPath
        $configDir = Split-Path $ConfigPath -Parent
        
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }
        
        # Load or create config
        if (Test-Path $ConfigPath) {
            $global:ConfigManager.Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json -Depth 10
        } else {
            $global:ConfigManager.Config = $global:ConfigManager.DefaultConfig
            Save-Config
        }
        
        Write-Host "Config Manager initialized: $ConfigPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error initializing config manager: $_" -ForegroundColor Red
        return $false
    }
}

function Get-Config {
    param([string]$ConfigPath = $global:ConfigManager.ConfigPath)
    
    try {
        if (-not $global:ConfigManager.Config) {
            Initialize-ConfigManager -ConfigPath $ConfigPath
        }
        
        return $global:ConfigManager.Config
        
    } catch {
        Write-Host "Error getting config: $_" -ForegroundColor Red
        return $null
    }
}

function Get-ConfigValue {
    param(
        [string]$Key,
        [string]$ConfigPath = $global:ConfigManager.ConfigPath
    )
    
    try {
        $config = Get-Config -ConfigPath $ConfigPath
        if (-not $config) {
            return $null
        }
        
        $keys = $Key.Split('.')
        $value = $config
        
        foreach ($key in $keys) {
            if ($value -and $value.PSObject.Properties[$key]) {
                $value = $value.$key
            } else {
                return $null
            }
        }
        
        return $value
        
    } catch {
        Write-Host "Error getting config value for key '$Key': $_" -ForegroundColor Red
        return $null
    }
}

function Set-ConfigValue {
    param(
        [string]$Key,
        [object]$Value,
        [string]$ConfigPath = $global:ConfigManager.ConfigPath
    )
    
    try {
        $config = Get-Config -ConfigPath $ConfigPath
        if (-not $config) {
            return $false
        }
        
        $keys = $Key.Split('.')
        $current = $config
        
        for ($i = 0; $i -lt $keys.Count - 1; $i++) {
            $key = $keys[$i]
            if (-not $current.PSObject.Properties[$key]) {
                $current | Add-Member -MemberType NoteProperty -Name $key -Value @{}
            }
            $current = $current.$key
        }
        
        $lastKey = $keys[-1]
        $current.$lastKey = $Value
        
        Save-Config -ConfigPath $ConfigPath
        Write-Host "Config value set: $Key = $Value" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error setting config value for key '$Key': $_" -ForegroundColor Red
        return $false
    }
}

function Save-Config {
    param([string]$ConfigPath = $global:ConfigManager.ConfigPath)
    
    try {
        $configDir = Split-Path $ConfigPath -Parent
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }
        
        $json = $global:ConfigManager.Config | ConvertTo-Json -Depth 10
        Set-Content -Path $ConfigPath -Value $json -Encoding UTF8
        
        Write-Host "Config saved: $ConfigPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error saving config: $_" -ForegroundColor Red
        return $false
    }
}

function Reset-Config {
    param([string]$ConfigPath = $global:ConfigManager.ConfigPath)
    
    try {
        $global:ConfigManager.Config = $global:ConfigManager.DefaultConfig
        Save-Config -ConfigPath $ConfigPath
        Write-Host "Config reset to default: $ConfigPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error resetting config: $_" -ForegroundColor Red
        return $false
    }
}

function Validate-Config {
    param([string]$ConfigPath = $global:ConfigManager.ConfigPath)
    
    try {
        $config = Get-Config -ConfigPath $ConfigPath
        if (-not $config) {
            Write-Host "Config validation failed: Cannot load config" -ForegroundColor Red
            return $false
        }
        
        $errors = @()
        
        # Validate required sections
        $requiredSections = @("System", "Performance", "AI", "Watchdog", "MeshCentral", "FileWatcher", "Security")
        foreach ($section in $requiredSections) {
            if (-not $config.PSObject.Properties[$section]) {
                $errors += "Missing required section: $section"
            }
        }
        
        # Validate System section
        if ($config.System) {
            if (-not $config.System.Name) { $errors += "System.Name is required" }
            if (-not $config.System.Version) { $errors += "System.Version is required" }
            if (-not $config.System.LogLevel) { $errors += "System.LogLevel is required" }
        }
        
        # Validate Performance section
        if ($config.Performance) {
            if ($config.Performance.MaxConcurrentFiles -lt 1) { $errors += "Performance.MaxConcurrentFiles must be >= 1" }
            if ($config.Performance.FileCheckInterval -lt 1) { $errors += "Performance.FileCheckInterval must be >= 1" }
            if ($config.Performance.HeartbeatInterval -lt 1) { $errors += "Performance.HeartbeatInterval must be >= 1" }
        }
        
        # Validate AI section
        if ($config.AI) {
            if (-not $config.AI.WhitelistPath) { $errors += "AI.WhitelistPath is required" }
            if (-not $config.AI.Patterns) { $errors += "AI.Patterns is required" }
        }
        
        # Validate Watchdog section
        if ($config.Watchdog) {
            if ($config.Watchdog.CheckInterval -lt 1) { $errors += "Watchdog.CheckInterval must be >= 1" }
            if ($config.Watchdog.MaxRetries -lt 1) { $errors += "Watchdog.MaxRetries must be >= 1" }
        }
        
        # Validate MeshCentral section
        if ($config.MeshCentral) {
            if ($config.MeshCentral.Enabled -and -not $config.MeshCentral.ServerUrl) { 
                $errors += "MeshCentral.ServerUrl is required when enabled" 
            }
        }
        
        # Validate FileWatcher section
        if ($config.FileWatcher) {
            if ($config.FileWatcher.MaxWatchers -lt 1) { $errors += "FileWatcher.MaxWatchers must be >= 1" }
            if (-not $config.FileWatcher.WatchPaths -or $config.FileWatcher.WatchPaths.Count -eq 0) { 
                $errors += "FileWatcher.WatchPaths is required" 
            }
        }
        
        if ($errors.Count -gt 0) {
            Write-Host "Config validation failed:" -ForegroundColor Red
            foreach ($error in $errors) {
                Write-Host "  - $error" -ForegroundColor Red
            }
            return $false
        }
        
        Write-Host "Config validation passed" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error validating config: $_" -ForegroundColor Red
        return $false
    }
}

function Show-Config {
    param([string]$ConfigPath = $global:ConfigManager.ConfigPath)
    
    try {
        $config = Get-Config -ConfigPath $ConfigPath
        if (-not $config) {
            Write-Host "Cannot load config" -ForegroundColor Red
            return
        }
        
        Write-Host "`n=== XML GUARD CONFIGURATION ===" -ForegroundColor Cyan
        Write-Host "Config Path: $ConfigPath" -ForegroundColor Yellow
        Write-Host "System: $($config.System.Name) v$($config.System.Version)" -ForegroundColor Green
        Write-Host "Log Level: $($config.System.LogLevel)" -ForegroundColor Green
        Write-Host "Performance: MaxFiles=$($config.Performance.MaxConcurrentFiles), CheckInterval=$($config.Performance.FileCheckInterval)s" -ForegroundColor Green
        Write-Host "Watchdog: Enabled=$($config.Watchdog.Enabled), CheckInterval=$($config.Watchdog.CheckInterval)s" -ForegroundColor Green
        Write-Host "MeshCentral: Enabled=$($config.MeshCentral.Enabled), Server=$($config.MeshCentral.ServerUrl)" -ForegroundColor Green
        Write-Host "FileWatcher: MaxWatchers=$($config.FileWatcher.MaxWatchers), WatchPaths=$($config.FileWatcher.WatchPaths.Count)" -ForegroundColor Green
        Write-Host "Security: RequireAdmin=$($config.Security.RequireAdmin), BackupOriginal=$($config.Security.BackupOriginal)" -ForegroundColor Green
        Write-Host "===============================`n" -ForegroundColor Cyan
        
    } catch {
        Write-Host "Error showing config: $_" -ForegroundColor Red
    }
}

# Main execution
if ($Get -and $Key) {
    $value = Get-ConfigValue -Key $Key -ConfigPath $ConfigPath
    if ($value -ne $null) {
        Write-Host $value
    } else {
        Write-Host "Config key not found: $Key" -ForegroundColor Red
    }
}
elseif ($Set -and $Key -and $Value) {
    Set-ConfigValue -Key $Key -Value $Value -ConfigPath $ConfigPath
}
elseif ($Reset) {
    Reset-Config -ConfigPath $ConfigPath
}
elseif ($Validate) {
    Validate-Config -ConfigPath $ConfigPath
}
else {
    # Initialize config manager
    Initialize-ConfigManager -ConfigPath $ConfigPath
    Show-Config -ConfigPath $ConfigPath
}

# Export functions
Export-ModuleMember -Function @(
    'Get-Config',
    'Get-ConfigValue',
    'Set-ConfigValue',
    'Save-Config',
    'Reset-Config',
    'Validate-Config',
    'Show-Config',
    'Initialize-ConfigManager'
)
