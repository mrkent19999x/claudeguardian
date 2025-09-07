# Logger.ps1 - Hệ thống logging cho XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$Message,
    [string]$Level = "INFO",
    [string]$LogPath = ".\Logs\xmlguard.log",
    [switch]$View,
    [string]$Filter = "*",
    [int]$Lines = 100
)

# Global variables
$global:LoggerConfig = @{
    LogPath = $LogPath
    MaxLogSize = 10MB
    MaxLogFiles = 5
    LogLevels = @{
        "DEBUG" = 0
        "INFO" = 1
        "WARN" = 2
        "ERROR" = 3
        "SUCCESS" = 4
        "IMPORTANT" = 5
    }
    CurrentLevel = 1
    Colors = @{
        "DEBUG" = "Gray"
        "INFO" = "White"
        "WARN" = "Yellow"
        "ERROR" = "Red"
        "SUCCESS" = "Green"
        "IMPORTANT" = "Cyan"
    }
}

function Initialize-Logger {
    param([string]$LogPath = ".\Logs\xmlguard.log")
    
    try {
        $global:LoggerConfig.LogPath = $LogPath
        $logDir = Split-Path $LogPath -Parent
        
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        # Create initial log file if not exists
        if (-not (Test-Path $LogPath)) {
            $header = @"
# XML Guard Enterprise Log
# Started: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ================================================
"@
            Set-Content -Path $LogPath -Value $header -Encoding UTF8
        }
        
        Write-Host "Logger initialized: $LogPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "Error initializing logger: $_" -ForegroundColor Red
        return $false
    }
}

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$LogPath = $global:LoggerConfig.LogPath
    )
    
    try {
        # Check log level
        $messageLevel = $global:LoggerConfig.LogLevels[$Level]
        if ($messageLevel -lt $global:LoggerConfig.CurrentLevel) {
            return
        }
        
        # Format log entry
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $logEntry = "[$timestamp] [$Level] $Message"
        
        # Write to file
        Add-Content -Path $LogPath -Value $logEntry -Encoding UTF8 -ErrorAction SilentlyContinue
        
        # Write to console with color
        $color = $global:LoggerConfig.Colors[$Level]
        if ($color) {
            Write-Host $logEntry -ForegroundColor $color
        } else {
            Write-Host $logEntry
        }
        
        # Rotate log if too large
        Rotate-LogFile -LogPath $LogPath
        
    } catch {
        Write-Host "Error writing log: $_" -ForegroundColor Red
    }
}

function Rotate-LogFile {
    param([string]$LogPath = $global:LoggerConfig.LogPath)
    
    try {
        if (-not (Test-Path $LogPath)) {
            return
        }
        
        $logFile = Get-Item $LogPath
        if ($logFile.Length -gt $global:LoggerConfig.MaxLogSize) {
            # Rotate log files
            $logDir = Split-Path $LogPath -Parent
            $logName = [System.IO.Path]::GetFileNameWithoutExtension($LogPath)
            $logExt = [System.IO.Path]::GetExtension($LogPath)
            
            # Move existing logs
            for ($i = $global:LoggerConfig.MaxLogFiles - 1; $i -gt 0; $i--) {
                $oldFile = Join-Path $logDir "$logName.$i$logExt"
                $newFile = Join-Path $logDir "$logName.$($i + 1)$logExt"
                
                if (Test-Path $oldFile) {
                    if ($i -eq $global:LoggerConfig.MaxLogFiles - 1) {
                        Remove-Item $oldFile -Force
                    } else {
                        Move-Item $oldFile $newFile -Force
                    }
                }
            }
            
            # Move current log
            $rotatedFile = Join-Path $logDir "$logName.1$logExt"
            Move-Item $LogPath $rotatedFile -Force
            
            # Create new log file
            $header = @"
# XML Guard Enterprise Log
# Rotated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ================================================
"@
            Set-Content -Path $LogPath -Value $header -Encoding UTF8
            
            Write-Host "Log file rotated: $LogPath" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "Error rotating log file: $_" -ForegroundColor Red
    }
}

function Get-LogEntries {
    param(
        [string]$LogPath = $global:LoggerConfig.LogPath,
        [string]$Filter = "*",
        [int]$Lines = 100,
        [string]$Level = "*"
    )
    
    try {
        if (-not (Test-Path $LogPath)) {
            Write-Host "Log file not found: $LogPath" -ForegroundColor Red
            return
        }
        
        $logEntries = Get-Content $LogPath -ErrorAction SilentlyContinue
        
        if ($Level -ne "*") {
            $logEntries = $logEntries | Where-Object { $_ -match "\[$Level\]" }
        }
        
        if ($Filter -ne "*") {
            $logEntries = $logEntries | Where-Object { $_ -like "*$Filter*" }
        }
        
        $logEntries | Select-Object -Last $Lines | ForEach-Object {
            $color = "White"
            if ($_ -match "\[ERROR\]") { $color = "Red" }
            elseif ($_ -match "\[WARN\]") { $color = "Yellow" }
            elseif ($_ -match "\[SUCCESS\]") { $color = "Green" }
            elseif ($_ -match "\[IMPORTANT\]") { $color = "Cyan" }
            elseif ($_ -match "\[DEBUG\]") { $color = "Gray" }
            
            Write-Host $_ -ForegroundColor $color
        }
        
    } catch {
        Write-Host "Error reading log entries: $_" -ForegroundColor Red
    }
}

function Clear-LogFile {
    param([string]$LogPath = $global:LoggerConfig.LogPath)
    
    try {
        if (Test-Path $LogPath) {
            $header = @"
# XML Guard Enterprise Log
# Cleared: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# ================================================
"@
            Set-Content -Path $LogPath -Value $header -Encoding UTF8
            Write-Host "Log file cleared: $LogPath" -ForegroundColor Green
        }
    } catch {
        Write-Host "Error clearing log file: $_" -ForegroundColor Red
    }
}

function Set-LogLevel {
    param([string]$Level)
    
    if ($global:LoggerConfig.LogLevels.ContainsKey($Level)) {
        $global:LoggerConfig.CurrentLevel = $global:LoggerConfig.LogLevels[$Level]
        Write-Host "Log level set to: $Level" -ForegroundColor Green
    } else {
        Write-Host "Invalid log level: $Level" -ForegroundColor Red
        Write-Host "Available levels: $($global:LoggerConfig.LogLevels.Keys -join ', ')" -ForegroundColor Yellow
    }
}

function Get-LogStats {
    param([string]$LogPath = $global:LoggerConfig.LogPath)
    
    try {
        if (-not (Test-Path $LogPath)) {
            Write-Host "Log file not found: $LogPath" -ForegroundColor Red
            return
        }
        
        $logEntries = Get-Content $LogPath -ErrorAction SilentlyContinue
        $stats = @{}
        
        foreach ($level in $global:LoggerConfig.LogLevels.Keys) {
            $count = ($logEntries | Where-Object { $_ -match "\[$level\]" }).Count
            $stats[$level] = $count
        }
        
        Write-Host "`n=== LOG STATISTICS ===" -ForegroundColor Cyan
        foreach ($level in $stats.Keys) {
            $color = $global:LoggerConfig.Colors[$level]
            Write-Host "$level : $($stats[$level])" -ForegroundColor $color
        }
        Write-Host "=====================`n" -ForegroundColor Cyan
        
    } catch {
        Write-Host "Error getting log stats: $_" -ForegroundColor Red
    }
}

# Main execution
if ($View) {
    Get-LogEntries -LogPath $LogPath -Filter $Filter -Lines $Lines
}
elseif ($Message) {
    Write-Log -Message $Message -Level $Level -LogPath $LogPath
}
else {
    # Initialize logger
    Initialize-Logger -LogPath $LogPath
}

# Export functions
Export-ModuleMember -Function @(
    'Write-Log',
    'Get-LogEntries',
    'Clear-LogFile',
    'Set-LogLevel',
    'Get-LogStats',
    'Initialize-Logger',
    'Rotate-LogFile'
)
