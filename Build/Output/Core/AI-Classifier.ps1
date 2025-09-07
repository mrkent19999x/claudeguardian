# AI-Classifier.ps1 - AI Classifier thông minh cho XML
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$XMLPath,
    [string]$WhitelistPath = ".\Config\whitelist.json",
    [switch]$Verbose
)

# Global variables
$global:AIClassifierConfig = @{
    WhitelistPath = $WhitelistPath
    Patterns = @{
        MST = @(
            "//MST", "//mst", "//MaSoThue", "//ma_so_thue",
            "//TaxCode", "//TaxpayerID", "//*[local-name()='MST']",
            "//*[local-name()='MaSoThue']", "//*[local-name()='TaxCode']"
        )
        FormCode = @(
            "//MauSo", "//Mau", "//Form", "//FormCode", "//MaToKhai",
            "//*[local-name()='MauSo']", "//*[local-name()='FormCode']"
        )
        Period = @(
            "//KyKKhaiThang", "//*[local-name()='KyKKhaiThang']",
            "//Thang", "//*[local-name()='Thang']", "//ThangBC",
            "//*[local-name()='ThangBC']", "//KyThang", "//*[local-name()='KyThang']"
        )
    }
    KnownForms = @("01/GTGT", "05/KK-TNCN", "03/TNDN", "BC26/AC")
    MSTPattern = '\b\d{10}(?:-\d{3})?\b'
    PeriodPatterns = @{
        MONTH = '^(0?[1-9]|1[0-2])[\/\-](19|20)\d{2}$'
        QUARTER = '^(?:Q|Quy)?\s*([1-4])\s*(?:\/|\-)?\s*((?:19|20)\d{2})$'
        YEAR = '^(19|20)\d{2}$'
    }
}

function Initialize-AIClassifier {
    Write-Log "Khởi tạo AI Classifier..." "INFO"
    
    try {
        # Load whitelist
        if (Test-Path $global:AIClassifierConfig.WhitelistPath) {
            $global:AIClassifierConfig.Whitelist = Get-Content $global:AIClassifierConfig.WhitelistPath -Raw | ConvertFrom-Json
            Write-Log "Đã load whitelist: $($global:AIClassifierConfig.Whitelist.Count) items" "SUCCESS"
        } else {
            Write-Log "Không tìm thấy whitelist: $($global:AIClassifierConfig.WhitelistPath)" "WARN"
            $global:AIClassifierConfig.Whitelist = @()
        }
        
        # Initialize patterns
        $global:AIClassifierConfig.CompiledPatterns = @{
            MST = [regex]$global:AIClassifierConfig.MSTPattern
            Period = @{}
        }
        
        foreach ($type in $global:AIClassifierConfig.PeriodPatterns.Keys) {
            $global:AIClassifierConfig.CompiledPatterns.Period[$type] = [regex]$global:AIClassifierConfig.PeriodPatterns[$type]
        }
        
        Write-Log "AI Classifier khởi tạo thành công" "SUCCESS"
        return $true
        
    } catch {
        Write-Log "Lỗi khởi tạo AI Classifier: $_" "ERROR"
        return $false
    }
}

function Read-XMLSafe {
    param([string]$FilePath)
    
    try {
        if (-not (Test-Path $FilePath)) {
            return $null
        }
        
        $content = Get-Content $FilePath -Encoding UTF8 -ErrorAction Stop
        $xml = [xml]$content
        return $xml
        
    } catch {
        if ($Verbose) {
            Write-Log "Lỗi đọc XML $FilePath : $_" "WARN"
        }
        return $null
    }
}

function Extract-MST {
    param([string]$FilePath)
    
    try {
        $xml = Read-XMLSafe $FilePath
        if (-not $xml) { return $null }
        
        # Tìm trong các trường XML chuẩn
        foreach ($pattern in $global:AIClassifierConfig.Patterns.MST) {
            try {
                $nodes = $xml.SelectNodes($pattern)
                foreach ($node in $nodes) {
                    if ($node.InnerText -and $node.InnerText -match $global:AIClassifierConfig.MSTPattern) {
                        return $node.InnerText.Trim()
                    }
                }
            } catch {
                # Ignore pattern errors
            }
        }
        
        # Fallback: regex trong toàn bộ content
        $content = Get-Content $FilePath -Raw -Encoding UTF8
        $match = $global:AIClassifierConfig.CompiledPatterns.MST.Match($content)
        if ($match.Success) {
            return $match.Value
        }
        
        return $null
        
    } catch {
        if ($Verbose) {
            Write-Log "Lỗi extract MST từ $FilePath : $_" "WARN"
        }
        return $null
    }
}

function Extract-FormCode {
    param([string]$FilePath)
    
    try {
        $xml = Read-XMLSafe $FilePath
        if (-not $xml) { return $null }
        
        # Tìm trong các trường XML chuẩn
        foreach ($pattern in $global:AIClassifierConfig.Patterns.FormCode) {
            try {
                $nodes = $xml.SelectNodes($pattern)
                foreach ($node in $nodes) {
                    if ($node.InnerText -and $node.InnerText.Trim()) {
                        return $node.InnerText.Trim()
                    }
                }
            } catch {
                # Ignore pattern errors
            }
        }
        
        # Fallback: known forms
        $content = Get-Content $FilePath -Raw -Encoding UTF8
        foreach ($form in $global:AIClassifierConfig.KnownForms) {
            if ($content -like "*$form*") {
                return $form
            }
        }
        
        # Fallback: regex pattern
        $match = [regex]::Match($content, '(\d{2}\/[A-Z0-9\-]+)')
        if ($match.Success) {
            return $match.Groups[1].Value
        }
        
        return $null
        
    } catch {
        if ($Verbose) {
            Write-Log "Lỗi extract FormCode từ $FilePath : $_" "WARN"
        }
        return $null
    }
}

function Extract-Period {
    param([string]$FilePath)
    
    try {
        $xml = Read-XMLSafe $FilePath
        if (-not $xml) { return $null }
        
        $content = Get-Content $FilePath -Raw -Encoding UTF8
        
        # Tìm tháng
        foreach ($pattern in $global:AIClassifierConfig.Patterns.Period) {
            try {
                $nodes = $xml.SelectNodes($pattern)
                foreach ($node in $nodes) {
                    if ($node.InnerText -and $node.InnerText -match $global:AIClassifierConfig.PeriodPatterns.MONTH) {
                        $parts = $node.InnerText -split '[\/\-]'
                        $mm = "{0:D2}" -f [int]$parts[0]
                        $yy = $parts[1]
                        return @{ Type = "MONTH"; Value = "$yy-$mm" }
                    }
                }
            } catch {
                # Ignore pattern errors
            }
        }
        
        # Tìm quý
        $quarterMatch = $global:AIClassifierConfig.CompiledPatterns.Period.QUARTER.Match($content)
        if ($quarterMatch.Success) {
            $q = $quarterMatch.Groups[1].Value
            $yy = $quarterMatch.Groups[2].Value
            return @{ Type = "QUARTER"; Value = "$yy-Q$q" }
        }
        
        # Tìm năm
        $yearMatch = $global:AIClassifierConfig.CompiledPatterns.Period.YEAR.Match($content)
        if ($yearMatch.Success) {
            return @{ Type = "YEAR"; Value = $yearMatch.Groups[1].Value }
        }
        
        return $null
        
    } catch {
        if ($Verbose) {
            Write-Log "Lỗi extract Period từ $FilePath : $_" "WARN"
        }
        return $null
    }
}

function Classify-XML {
    param([string]$FilePath)
    
    try {
        if (-not (Test-Path $FilePath)) {
            return @{ Success = $false; Error = "File không tồn tại" }
        }
        
        $mst = Extract-MST $FilePath
        $formCode = Extract-FormCode $FilePath
        $period = Extract-Period $FilePath
        
        if (-not $mst -or -not $formCode -or -not $period) {
            return @{
                Success = $false
                Error = "Không thể extract đầy đủ thông tin"
                MST = $mst
                FormCode = $formCode
                Period = $period
            }
        }
        
        $classification = @{
            Success = $true
            FilePath = $FilePath
            MST = $mst
            FormCode = $formCode
            Period = $period
            PeriodString = "$($period.Type):$($period.Value)"
            Timestamp = Get-Date
        }
        
        if ($Verbose) {
            Write-Log "Phân loại XML: $FilePath - MST: $mst, Form: $formCode, Period: $($classification.PeriodString)" "INFO"
        }
        
        return $classification
        
    } catch {
        Write-Log "Lỗi phân loại XML $FilePath : $_" "ERROR"
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}

function Match-Whitelist {
    param([hashtable]$Classification)
    
    try {
        if (-not $global:AIClassifierConfig.Whitelist) {
            return @{ Matched = $false; Reason = "Không có whitelist" }
        }
        
        foreach ($item in $global:AIClassifierConfig.Whitelist) {
            $match = $true
            
            # Check MST
            if ($item.mst -and $item.mst -ne $Classification.MST) {
                $match = $false
            }
            
            # Check FormCode
            if ($item.formCode -and $item.formCode -ne $Classification.FormCode) {
                $match = $false
            }
            
            # Check Period
            if ($item.periodType -and $item.periodValue) {
                $expectedPeriod = "$($item.periodType):$($item.periodValue)"
                if ($expectedPeriod -ne $Classification.PeriodString) {
                    $match = $false
                }
            }
            
            if ($match) {
                return @{
                    Matched = $true
                    MatchedItem = $item
                    Reason = "Khớp với whitelist"
                }
            }
        }
        
        return @{ Matched = $false; Reason = "Không khớp với whitelist" }
        
    } catch {
        Write-Log "Lỗi match whitelist: $_" "ERROR"
        return @{ Matched = $false; Reason = "Lỗi xử lý whitelist" }
    }
}

function Process-XMLFile {
    param([string]$FilePath)
    
    try {
        # Classify XML
        $classification = Classify-XML $FilePath
        if (-not $classification.Success) {
            return @{
                Success = $false
                Action = "SKIP"
                Reason = $classification.Error
                Classification = $classification
            }
        }
        
        # Match with whitelist
        $whitelistMatch = Match-Whitelist $classification
        if (-not $whitelistMatch.Matched) {
            return @{
                Success = $true
                Action = "PASS"
                Reason = $whitelistMatch.Reason
                Classification = $classification
            }
        }
        
        # Check if file needs protection
        $needsProtection = Test-FileNeedsProtection -FilePath $FilePath -WhitelistItem $whitelistMatch.MatchedItem
        
        return @{
            Success = $true
            Action = if ($needsProtection) { "PROTECT" } else { "OK" }
            Reason = if ($needsProtection) { "File cần bảo vệ" } else { "File đã đúng" }
            Classification = $classification
            WhitelistMatch = $whitelistMatch
            NeedsProtection = $needsProtection
        }
        
    } catch {
        Write-Log "Lỗi xử lý file $FilePath : $_" "ERROR"
        return @{
            Success = $false
            Action = "ERROR"
            Reason = $_.Exception.Message
        }
    }
}

function Test-FileNeedsProtection {
    param([string]$FilePath, [object]$WhitelistItem)
    
    try {
        if (-not $WhitelistItem.sourcePath -or -not (Test-Path $WhitelistItem.sourcePath)) {
            return $false
        }
        
        # Compare file hashes
        $currentHash = Get-FileHash $FilePath -Algorithm SHA256 -ErrorAction SilentlyContinue
        $sourceHash = Get-FileHash $WhitelistItem.sourcePath -Algorithm SHA256 -ErrorAction SilentlyContinue
        
        if ($currentHash -and $sourceHash -and $currentHash.Hash -eq $sourceHash.Hash) {
            return $false  # Files are identical
        }
        
        return $true  # Files are different, needs protection
        
    } catch {
        Write-Log "Lỗi kiểm tra file protection: $_" "WARN"
        return $false
    }
}

# Initialize when module is loaded
if ($MyInvocation.InvocationName -ne 'Import-Module') {
    Initialize-AIClassifier
}

# Export functions
Export-ModuleMember -Function @(
    'Initialize-AIClassifier',
    'Classify-XML',
    'Process-XMLFile',
    'Extract-MST',
    'Extract-FormCode',
    'Extract-Period',
    'Match-Whitelist'
)
