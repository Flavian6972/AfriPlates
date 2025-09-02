# activate.ps1
$venvPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    & $venvPath
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "Error: venv not found at $venvPath"
    Write-Host "Run 'python -m venv .venv' to create it."
}