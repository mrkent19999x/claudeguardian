# Upload-to-MeshCentral.ps1
# Script upload package len MeshCentral server

param(
    [string]$MeshCentralUrl = "https://103.69.86.130:4433",
    [string]$PackageFile = "XML-Guard-Enterprise-v2.0.zip",
    [string]$Username = "",
    [string]$Password = ""
)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "    UPLOAD PACKAGE TO MESHCENTRAL" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if package exists
if (-not (Test-Path $PackageFile)) {
    Write-Host "❌ Package file not found: $PackageFile" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Package found: $PackageFile" -ForegroundColor Green

# Get file size
$fileSize = (Get-Item $PackageFile).Length / 1MB
Write-Host "📦 File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Yellow

# Test MeshCentral connection
Write-Host "`n🔗 Testing MeshCentral connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $MeshCentralUrl -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "✅ MeshCentral connection: OK" -ForegroundColor Green
} catch {
    Write-Host "❌ MeshCentral connection failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Please check:" -ForegroundColor Yellow
    Write-Host "   - MeshCentral server is running" -ForegroundColor White
    Write-Host "   - URL is correct: $MeshCentralUrl" -ForegroundColor White
    Write-Host "   - Firewall allows connection" -ForegroundColor White
    exit 1
}

Write-Host "`n📤 Upload instructions:" -ForegroundColor Cyan
Write-Host "1. Open MeshCentral: $MeshCentralUrl" -ForegroundColor White
Write-Host "2. Login with your credentials" -ForegroundColor White
Write-Host "3. Go to 'Files' section" -ForegroundColor White
Write-Host "4. Create folder 'XML-Guard-Package'" -ForegroundColor White
Write-Host "5. Upload file: $PackageFile" -ForegroundColor White
Write-Host "6. Share download link with customers" -ForegroundColor White

Write-Host "`n📋 Customer instructions:" -ForegroundColor Cyan
Write-Host "1. Download package from MeshCentral" -ForegroundColor White
Write-Host "2. Extract to any folder" -ForegroundColor White
Write-Host "3. Run: Setup-Enterprise.bat" -ForegroundColor White
Write-Host "4. System will auto-configure" -ForegroundColor White

Write-Host "`n✅ Upload preparation complete!" -ForegroundColor Green
Write-Host "Package ready for distribution to enterprises." -ForegroundColor White
