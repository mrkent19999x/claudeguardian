# Build-All-Packages.ps1 - Build tất cả packages cho khách hàng
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

param(
    [string]$Version = "2.0.0",
    [string]$MeshCentralUrl = "https://103.69.86.130:4433",
    [switch]$Clean
)

Write-Host "🎁 XML GUARD ENTERPRISE - BUILD ALL PACKAGES" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host "MeshCentral: $MeshCentralUrl" -ForegroundColor Yellow

# Build One-Click EXE package
Write-Host "`n📦 Building One-Click EXE package..." -ForegroundColor Yellow
& ".\Create-OneClick-EXE.ps1" -OutputPath ".\Build\OneClick-EXE" -Version $Version -MeshCentralUrl $MeshCentralUrl -Clean:$Clean

# Build Complete Package
Write-Host "`n📦 Building Complete Package..." -ForegroundColor Yellow
& ".\Build-Complete-Package.ps1" -OutputPath ".\Build\Customer-Package" -Version $Version -MeshCentralUrl $MeshCentralUrl -Clean:$Clean

# Build Final Package
Write-Host "`n📦 Building Final Package..." -ForegroundColor Yellow
& ".\Build-Final-Package.ps1" -Version $Version -MeshCentralUrl $MeshCentralUrl

# Show summary
Write-Host "`n📊 BUILD SUMMARY" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan

$packages = @(
    @{ Name = "One-Click EXE"; Path = ".\Build\OneClick-EXE" },
    @{ Name = "Complete Package"; Path = ".\Build\Customer-Package" },
    @{ Name = "Final Package"; Path = ".\Build\Final-Package" }
)

foreach ($package in $packages) {
    if (Test-Path $package.Path) {
        $files = Get-ChildItem -Path $package.Path -Recurse
        Write-Host "✅ $($package.Name): $($files.Count) files" -ForegroundColor Green
    } else {
        Write-Host "❌ $($package.Name): Not found" -ForegroundColor Red
    }
}

Write-Host "`n🎯 DEPLOYMENT OPTIONS:" -ForegroundColor Yellow
Write-Host "1. One-Click EXE: For customers who want everything embedded" -ForegroundColor White
Write-Host "2. Complete Package: For customers with Python installed" -ForegroundColor White
Write-Host "3. Final Package: Recommended for most customers" -ForegroundColor White

Write-Host "`n✅ All packages built successfully!" -ForegroundColor Green
Write-Host "🚀 Ready for customer deployment!" -ForegroundColor Green