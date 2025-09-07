# watchdog-fixed.ps1 — Watchdog tối ưu, không vòng lặp
param(
  [string[]]$WatchRoots,
  [string]$WhitelistPath = "C:\GotXMLs\whitelist.json",
  [string]$LogPath = "C:\GotXMLs\xml_guard_log.csv",
  [int]$CheckInterval = 30,  # Kiểm tra mỗi 30s thay vì 1s
  [int]$MaxRetries = 3,      # Giới hạn retry
  [int]$CooldownPeriod = 60  # Nghỉ 60s sau khi retry hết
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$guardPath = Join-Path $scriptDir "watch-xml-guard-fixed.ps1"
if (!(Test-Path $guardPath)) { 
    Write-Host "❌ Không tìm thấy: $guardPath"
    exit 1 
}

# Nếu WatchRoots rỗng, để rỗng; guard sẽ tự lấy tất cả ổ đĩa
$rootArgs = @()
if ($WatchRoots -and $WatchRoots.Count -gt 0) {
  foreach ($r in $WatchRoots) { $rootArgs += "-WatchRoots `"$r`"" }
}

function Is-Running {
  try {
    $procs = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue
    foreach ($p in $procs) {
      if ($p.CommandLine -match [Regex]::Escape($guardPath)) { 
        return $true 
      }
    }
    return $false
  } catch { 
    return $false 
  }
}

function Start-GuardProcess {
  try {
    $args = @("-ExecutionPolicy Bypass","-File `"$guardPath`"","-WhitelistPath `"$WhitelistPath`"","-LogPath `"$LogPath`"","-Enforce")
    $args += $rootArgs
    
    # Khởi động với priority thấp
    $process = Start-Process powershell -ArgumentList ($args -join " ") -PassThru -WindowStyle Hidden
    $process.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::BelowNormal
    
    Write-Host "✅ Khởi động XML Guard thành công (PID: $($process.Id))"
    return $true
  } catch {
    Write-Host "❌ Lỗi khởi động XML Guard: $_"
    return $false
  }
}

# MAIN WATCHDOG - Tối ưu
Write-Host "🔄 Watchdog khởi động - Kiểm tra mỗi $CheckInterval giây"
$retryCount = 0
$lastStartTime = Get-Date

while ($true) {
  try {
    if (-not (Is-Running)) {
      $currentTime = Get-Date
      $timeSinceLastStart = ($currentTime - $lastStartTime).TotalSeconds
      
      # Kiểm tra cooldown period
      if ($timeSinceLastStart -lt $CooldownPeriod) {
        Write-Host "⏳ Đang trong cooldown period ($([math]::Round($CooldownPeriod - $timeSinceLastStart))s còn lại)"
        Start-Sleep -Seconds $CheckInterval
        continue
      }
      
      Write-Host "🔄 XML Guard không chạy - Thử khởi động lại... (Lần $($retryCount + 1)/$MaxRetries)"
      
      if (Start-GuardProcess) {
        $retryCount = 0
        $lastStartTime = Get-Date
        Write-Host "✅ XML Guard đã khởi động thành công"
      } else {
        $retryCount++
        if ($retryCount -ge $MaxRetries) {
          Write-Host "❌ Đã thử $MaxRetries lần - Dừng watchdog"
          break
        }
      }
    } else {
      # Reset retry count nếu process đang chạy
      if ($retryCount -gt 0) {
        $retryCount = 0
        Write-Host "✅ XML Guard đang chạy bình thường"
      }
    }
    
    # Sleep thông minh - không ngốn CPU
    Start-Sleep -Seconds $CheckInterval
    
  } catch {
    Write-Host "❌ Lỗi trong watchdog: $_"
    Start-Sleep -Seconds 60  # Nghỉ 1 phút khi có lỗi
  }
}

Write-Host "🛑 Watchdog dừng"
