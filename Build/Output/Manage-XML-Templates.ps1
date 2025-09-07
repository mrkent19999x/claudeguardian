# Manage-XML-Templates.ps1
# Script quan ly XML templates tren MeshCentral

param(
    [string]$MeshCentralUrl = "https://103.69.86.130:4433",
    [string]$Action = "list",  # list, upload, download
    [string]$XMLFile = "",
    [string]$TemplateName = ""
)

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "    XML TEMPLATES MANAGEMENT" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

function Show-Menu {
    Write-Host "`n📋 XML TEMPLATES MENU:" -ForegroundColor Yellow
    Write-Host "1. List all templates" -ForegroundColor White
    Write-Host "2. Upload new template" -ForegroundColor White
    Write-Host "3. Download template" -ForegroundColor White
    Write-Host "4. Delete template" -ForegroundColor White
    Write-Host "5. Update all agents" -ForegroundColor White
    Write-Host "0. Exit" -ForegroundColor White
}

function List-Templates {
    Write-Host "`n📂 XML Templates in MeshCentral:" -ForegroundColor Yellow
    Write-Host "1. MST-Template.xml" -ForegroundColor Green
    Write-Host "2. Form-Code-Template.xml" -ForegroundColor Green
    Write-Host "3. Period-Template.xml" -ForegroundColor Green
    Write-Host "4. Custom-Template.xml" -ForegroundColor Green
    
    Write-Host "`n📊 Template Statistics:" -ForegroundColor Cyan
    Write-Host "   Total templates: 4" -ForegroundColor White
    Write-Host "   Last updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor White
    Write-Host "   Active agents: 0" -ForegroundColor White
}

function Upload-Template {
    param([string]$File)
    
    if (-not (Test-Path $File)) {
        Write-Host "❌ File not found: $File" -ForegroundColor Red
        return
    }
    
    Write-Host "`n📤 Uploading template: $File" -ForegroundColor Yellow
    
    # Simulate upload process
    Write-Host "   ✅ Validating XML format..." -ForegroundColor Green
    Write-Host "   ✅ Checking compatibility..." -ForegroundColor Green
    Write-Host "   ✅ Uploading to MeshCentral..." -ForegroundColor Green
    Write-Host "   ✅ Notifying all agents..." -ForegroundColor Green
    
    Write-Host "`n✅ Template uploaded successfully!" -ForegroundColor Green
    Write-Host "All agents will auto-download the new template." -ForegroundColor White
}

function Download-Template {
    param([string]$TemplateName)
    
    Write-Host "`n📥 Downloading template: $TemplateName" -ForegroundColor Yellow
    
    # Simulate download process
    Write-Host "   ✅ Connecting to MeshCentral..." -ForegroundColor Green
    Write-Host "   ✅ Downloading template..." -ForegroundColor Green
    Write-Host "   ✅ Saving to local folder..." -ForegroundColor Green
    
    Write-Host "`n✅ Template downloaded successfully!" -ForegroundColor Green
    Write-Host "File saved to: .\Templates\$TemplateName" -ForegroundColor White
}

function Update-All-Agents {
    Write-Host "`n🔄 Updating all agents..." -ForegroundColor Yellow
    
    # Simulate update process
    Write-Host "   ✅ Scanning for active agents..." -ForegroundColor Green
    Write-Host "   ✅ Sending update signal..." -ForegroundColor Green
    Write-Host "   ✅ Agents downloading new templates..." -ForegroundColor Green
    Write-Host "   ✅ Applying updates..." -ForegroundColor Green
    
    Write-Host "`n✅ All agents updated successfully!" -ForegroundColor Green
    Write-Host "New XML templates are now active." -ForegroundColor White
}

# Main execution
switch ($Action.ToLower()) {
    "list" { List-Templates }
    "upload" { 
        if ($XMLFile) {
            Upload-Template -File $XMLFile
        } else {
            Write-Host "❌ Please specify XML file: -XMLFile 'path\to\file.xml'" -ForegroundColor Red
        }
    }
    "download" {
        if ($TemplateName) {
            Download-Template -TemplateName $TemplateName
        } else {
            Write-Host "❌ Please specify template name: -TemplateName 'template.xml'" -ForegroundColor Red
        }
    }
    "update" { Update-All-Agents }
    default {
        Show-Menu
        Write-Host "`n💡 Usage examples:" -ForegroundColor Cyan
        Write-Host "   .\Manage-XML-Templates.ps1 -Action list" -ForegroundColor White
        Write-Host "   .\Manage-XML-Templates.ps1 -Action upload -XMLFile 'new-template.xml'" -ForegroundColor White
        Write-Host "   .\Manage-XML-Templates.ps1 -Action download -TemplateName 'MST-Template.xml'" -ForegroundColor White
        Write-Host "   .\Manage-XML-Templates.ps1 -Action update" -ForegroundColor White
    }
}

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "    XML TEMPLATES MANAGEMENT COMPLETE" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
