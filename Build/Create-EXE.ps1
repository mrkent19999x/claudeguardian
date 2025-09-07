# Create-EXE.ps1 - Tạo EXE file cho XML Guard Enterprise
# Phiên bản: v2.0.0 - Enterprise Complete
# Tác giả: AI Assistant (Cipher)

Write-Host "Creating EXE file for XML Guard Enterprise..." -ForegroundColor Cyan

# Create IExpress configuration
$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles
[Strings]
InstallPrompt=XML Guard Enterprise v2.0.0
DisplayLicense=
FinishMessage=XML Guard Enterprise installed successfully!
TargetName=XML-Guard-Enterprise.exe
FriendlyName=XML Guard Enterprise
AppLaunched=XML-Guard-Simple.ps1
PostInstallCmd=
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0="XML-Guard-Simple.ps1"
FILE1="Core\XML-Guard-Core.ps1"
FILE2="Core\AI-Classifier.ps1"
FILE3="Utils\Logger.ps1"
FILE4="Utils\Config-Manager.ps1"
FILE5="Config\config.json"
[SourceFiles]
SourceFiles0=.\Build\Output\
[SourceFiles0]
%FILE0%=
%FILE1%=
%FILE2%=
%FILE3%=
%FILE4%=
%FILE5%=
"@

$sedFile = ".\Build\XML-Guard-Enterprise.sed"
Set-Content -Path $sedFile -Value $sedContent -Encoding UTF8

Write-Host "IExpress configuration created: $sedFile" -ForegroundColor Green

# Create EXE using IExpress
Write-Host "Creating EXE file..." -ForegroundColor Yellow
$iexpressCmd = "iexpress /N `"$sedFile`""
Write-Host "Command: $iexpressCmd" -ForegroundColor Gray

try {
    Invoke-Expression $iexpressCmd
    Write-Host "EXE file created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error creating EXE: $_" -ForegroundColor Red
    Write-Host "Please run IExpress manually:" -ForegroundColor Yellow
    Write-Host "  iexpress /N `"$sedFile`"" -ForegroundColor Gray
}

Write-Host "`nEXE creation completed!" -ForegroundColor Cyan
Write-Host "Check the Build directory for XML-Guard-Enterprise.exe" -ForegroundColor Yellow
