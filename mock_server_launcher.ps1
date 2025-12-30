# Mock API Server Launcher
# استفاده: .\mock_server_launcher.ps1

$pythonPath = "D:/project/project_payani/2/.venv/Scripts/python.exe"
$projectRoot = "d:\project\project_payani\2"

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Mock API Server Launcher - Unipath Project           ║" -ForegroundColor Cyan
Write-Host "║  Version 1.0                                          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n🔍 Checking Python environment..." -ForegroundColor Yellow

if (Test-Path $pythonPath) {
    Write-Host "✓ Python found: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found at: $pythonPath" -ForegroundColor Red
    Write-Host "Please update the pythonPath variable" -ForegroundColor Red
    exit 1
}

Write-Host "`n📁 Checking project files..." -ForegroundColor Yellow

$requiredFiles = @(
    "mock_server_simple.py",
    "test_api_simple.py",
    "backend/mock_api_db.json",
    "unipath_mobile/lib/config/api_config.dart"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $projectRoot $file
    if (Test-Path $fullPath) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file - NOT FOUND" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`n⚠️  Some files are missing!" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Select option:" -ForegroundColor Cyan
Write-Host "1. Start Mock Server (Local)" -ForegroundColor Yellow
Write-Host "2. Start Mock Server (Public with ngrok)" -ForegroundColor Yellow
Write-Host "3. Run Tests" -ForegroundColor Yellow
Write-Host "4. Start Server + Run Tests" -ForegroundColor Yellow
Write-Host "5. Show Configuration" -ForegroundColor Yellow
Write-Host "6. Exit" -ForegroundColor Yellow

$choice = Read-Host "`nEnter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 Starting Mock Server (Local)..." -ForegroundColor Green
        Write-Host "📡 Server will start on: http://localhost:8001/api`n" -ForegroundColor Cyan
        cd $projectRoot
        & $pythonPath mock_server_simple.py
    }
    
    "2" {
        Write-Host "`n🌐 Starting Mock Server (Public)..." -ForegroundColor Green
        Write-Host "📡 Setting up ngrok tunnel...`n" -ForegroundColor Cyan
        cd $projectRoot
        & $pythonPath mock_server_public.py --ngrok
    }
    
    "3" {
        Write-Host "`n🧪 Running Tests..." -ForegroundColor Green
        cd $projectRoot
        & $pythonPath test_api_simple.py
    }
    
    "4" {
        Write-Host "`n🚀 Starting Mock Server in background..." -ForegroundColor Green
        cd $projectRoot
        
        # Start server in background
        $serverJob = Start-Job -ScriptBlock {
            & "D:/project/project_payani/2/.venv/Scripts/python.exe" mock_server_simple.py
        }
        
        Write-Host "✓ Server started with Job ID: $($serverJob.Id)" -ForegroundColor Green
        
        # Wait for server to start
        Write-Host "`n⏳ Waiting for server to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
        
        # Run tests
        Write-Host "`n🧪 Running Tests...`n" -ForegroundColor Green
        & $pythonPath test_api_simple.py
        
        Write-Host "`n⚠️  Stopping server..." -ForegroundColor Yellow
        Stop-Job -Job $serverJob
        Remove-Job -Job $serverJob
        Write-Host "✓ Server stopped" -ForegroundColor Green
    }
    
    "5" {
        Write-Host "`n📋 Current Configuration:`n" -ForegroundColor Cyan
        Write-Host "Python Path:         $pythonPath" -ForegroundColor Yellow
        Write-Host "Project Root:        $projectRoot" -ForegroundColor Yellow
        Write-Host "Mock Server:         localhost:8001" -ForegroundColor Yellow
        Write-Host "API Base URL:        http://localhost:8001/api" -ForegroundColor Yellow
        Write-Host "Public API:          python mock_server_public.py --ngrok" -ForegroundColor Yellow
        Write-Host "Database File:       backend/mock_api_db.json" -ForegroundColor Yellow
        Write-Host "Config File:         unipath_mobile/lib/config/api_config.dart" -ForegroundColor Yellow
        
        Write-Host "`n📝 To use Public API (ngrok):" -ForegroundColor Cyan
        Write-Host "   1. pip install pyngrok" -ForegroundColor White
        Write-Host "   2. python mock_server_public.py --ngrok" -ForegroundColor White
        Write-Host "   3. Copy URL from output" -ForegroundColor White
        Write-Host "   4. Paste in api_config.dart (publicMockServerUrl)" -ForegroundColor White
    }
    
    "6" {
        Write-Host "`n👋 Goodbye!" -ForegroundColor Green
        exit 0
    }
    
    default {
        Write-Host "`n✗ Invalid option!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✅ Done!" -ForegroundColor Green
