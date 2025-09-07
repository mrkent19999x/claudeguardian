# XML-Guard-Core.ps1 - Core engine chính của XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$ConfigPath = ".\Config\config.json",
    [string]$LogPath = ".\Logs\xmlguard.log",
    [switch]$Start,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Status,
    [switch]$Debug
)

# Import modules
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$modulesPath = Join-Path $scriptDir "..\Utils"
Import-Module "$modulesPath\Logger.ps1" -Force -ErrorAction SilentlyContinue
Import-Module "$modulesPath\Config-Manager.ps1" -Force -ErrorAction SilentlyContinue
Import-Module "$modulesPath\Performance-Monitor.ps1" -Force -ErrorAction SilentlyContinue

# Global variables
$global:XMLGuardConfig = $null
$global:XMLGuardRunning = $false
$global:XMLGuardProcesses = @()
$global:XMLGuardStartTime = $null

function Initialize-XMLGuard {
    Write-Log "=== XML GUARD ENTERPRISE CORE v2.0.0 ===" "INFO"
    Write-Log "Khởi tạo hệ thống..." "INFO"
    
    try {
        # Load configuration
        $global:XMLGuardConfig = Get-Config -ConfigPath $ConfigPath
        if (-not $global:XMLGuardConfig) {
            Write-Log "Không thể load config từ $ConfigPath" "ERROR"
            return $false
        }
        
        # Set process priority
        [System.Diagnostics.Process]::GetCurrentProcess().PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
        
        # Initialize performance monitor
        Start-PerformanceMonitor -LogPath $LogPath
        
        # Initialize AI Classifier
        Initialize-AIClassifier
        
        # Initialize File Processor
        Initialize-FileProcessor
        
        # Initialize Watchdog
        Initialize-Watchdog
        
        # Initialize MeshCentral
        Initialize-MeshCentral
        
        $global:XMLGuardStartTime = Get-Date
        $global:XMLGuardRunning = $true
        
        Write-Log "XML Guard Core khởi tạo thành công" "SUCCESS"
        return $true
        
    } catch {
        Write-Log "Lỗi khởi tạo XML Guard Core: $_" "ERROR"
        return $false
    }
}

function Initialize-AIClassifier {
    Write-Log "Khởi tạo AI Classifier..." "INFO"
    
    try {
        $aiClassifierPath = Join-Path $scriptDir "AI-Classifier.ps1"
        if (Test-Path $aiClassifierPath) {
            . $aiClassifierPath
            Write-Log "AI Classifier khởi tạo thành công" "SUCCESS"
        } else {
            Write-Log "Không tìm thấy AI-Classifier.ps1" "WARN"
        }
    } catch {
        Write-Log "Lỗi khởi tạo AI Classifier: $_" "ERROR"
    }
}

function Initialize-FileProcessor {
    Write-Log "Khởi tạo File Processor..." "INFO"
    
    try {
        $fileProcessorPath = Join-Path $scriptDir "File-Processor.ps1"
        if (Test-Path $fileProcessorPath) {
            . $fileProcessorPath
            Write-Log "File Processor khởi tạo thành công" "SUCCESS"
        } else {
            Write-Log "Không tìm thấy File-Processor.ps1" "WARN"
        }
    } catch {
        Write-Log "Lỗi khởi tạo File Processor: $_" "ERROR"
    }
}

function Initialize-Watchdog {
    Write-Log "Khởi tạo Watchdog System..." "INFO"
    
    try {
        $watchdogPath = Join-Path $scriptDir "..\Watchdog\Watchdog-Manager.ps1"
        if (Test-Path $watchdogPath) {
            . $watchdogPath
            Start-WatchdogManager -Config $global:XMLGuardConfig
            Write-Log "Watchdog System khởi tạo thành công" "SUCCESS"
        } else {
            Write-Log "Không tìm thấy Watchdog-Manager.ps1" "WARN"
        }
    } catch {
        Write-Log "Lỗi khởi tạo Watchdog System: $_" "ERROR"
    }
}

function Initialize-MeshCentral {
    Write-Log "Khởi tạo MeshCentral Integration..." "INFO"
    
    try {
        $meshCentralPath = Join-Path $scriptDir "..\MeshCentral\Remote-Manager.ps1"
        if (Test-Path $meshCentralPath) {
            . $meshCentralPath
            Connect-MeshCentral -Config $global:XMLGuardConfig
            Write-Log "MeshCentral Integration khởi tạo thành công" "SUCCESS"
        } else {
            Write-Log "Không tìm thấy Remote-Manager.ps1" "WARN"
        }
    } catch {
        Write-Log "Lỗi khởi tạo MeshCentral Integration: $_" "ERROR"
    }
}

function Start-XMLGuard {
    if ($global:XMLGuardRunning) {
        Write-Log "XML Guard đã đang chạy" "WARN"
        return $true
    }
    
    Write-Log "Khởi động XML Guard..." "INFO"
    
    if (Initialize-XMLGuard) {
        Write-Log "XML Guard khởi động thành công" "SUCCESS"
        return $true
    } else {
        Write-Log "Lỗi khởi động XML Guard" "ERROR"
        return $false
    }
}

function Stop-XMLGuard {
    if (-not $global:XMLGuardRunning) {
        Write-Log "XML Guard chưa chạy" "WARN"
        return $true
    }
    
    Write-Log "Dừng XML Guard..." "INFO"
    
    try {
        # Stop all processes
        foreach ($process in $global:XMLGuardProcesses) {
            if ($process -and -not $process.HasExited) {
                $process.Kill()
                Write-Log "Đã dừng process: $($process.ProcessName)" "INFO"
            }
        }
        
        # Stop performance monitor
        Stop-PerformanceMonitor
        
        $global:XMLGuardRunning = $false
        $global:XMLGuardProcesses = @()
        
        Write-Log "XML Guard đã dừng" "SUCCESS"
        return $true
        
    } catch {
        Write-Log "Lỗi dừng XML Guard: $_" "ERROR"
        return $false
    }
}

function Restart-XMLGuard {
    Write-Log "Khởi động lại XML Guard..." "INFO"
    
    Stop-XMLGuard
    Start-Sleep -Seconds 3
    Start-XMLGuard
}

function Get-XMLGuardStatus {
    $status = @{
        Running = $global:XMLGuardRunning
        StartTime = $global:XMLGuardStartTime
        ProcessCount = $global:XMLGuardProcesses.Count
        Config = $global:XMLGuardConfig
    }
    
    if ($global:XMLGuardRunning) {
        $uptime = (Get-Date) - $global:XMLGuardStartTime
        $status.Uptime = $uptime.ToString("dd\.hh\:mm\:ss")
    }
    
    return $status
}

function Show-XMLGuardStatus {
    $status = Get-XMLGuardStatus
    
    Write-Host "`n=== XML GUARD STATUS ===" -ForegroundColor Cyan
    Write-Host "Trạng thái: $(if($status.Running) {'Đang chạy'} else {'Dừng'})" -ForegroundColor $(if($status.Running) {'Green'} else {'Red'})
    
    if ($status.Running) {
        Write-Host "Thời gian chạy: $($status.Uptime)" -ForegroundColor Green
        Write-Host "Số process: $($status.ProcessCount)" -ForegroundColor Green
    }
    
    Write-Host "Config: $($status.Config.ConfigPath)" -ForegroundColor Yellow
    Write-Host "========================`n" -ForegroundColor Cyan
}

# Main execution
if ($Start) {
    Start-XMLGuard
    if ($Debug) {
        Show-XMLGuardStatus
    }
}
elseif ($Stop) {
    Stop-XMLGuard
}
elseif ($Restart) {
    Restart-XMLGuard
}
elseif ($Status) {
    Show-XMLGuardStatus
}
else {
    # Default: Start with status
    Start-XMLGuard
    Show-XMLGuardStatus
}

# Keep running if started
if ($Start -and $global:XMLGuardRunning) {
    Write-Log "XML Guard Core đang chạy... (Nhấn Ctrl+C để dừng)" "INFO"
    
    try {
        while ($global:XMLGuardRunning) {
            # Main loop - check every 30 seconds
            Start-Sleep -Seconds 30
            
            # Health check
            if ($global:XMLGuardRunning) {
                $health = Test-SystemHealth
                if (-not $health) {
                    Write-Log "System health check failed - Restarting..." "WARN"
                    Restart-XMLGuard
                }
            }
        }
    } catch {
        Write-Log "Lỗi trong main loop: $_" "ERROR"
    } finally {
        Stop-XMLGuard
        Write-Log "XML Guard Core đã dừng" "INFO"
    }
}
