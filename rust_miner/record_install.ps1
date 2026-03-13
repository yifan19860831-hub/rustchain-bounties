# RustChain Miner Installation Recording Script
# This script records the installation process using PowerShell transcript

$outputDir = Join-Path $PSScriptRoot "recordings"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$transcriptFile = Join-Path $outputDir "install_$timestamp.txt"
$castFile = Join-Path $outputDir "install_$timestamp.cast"

Write-Host "Starting installation recording..."
Write-Host "Transcript: $transcriptFile"

# Start transcript
Start-Transcript -Path $transcriptFile

Write-Host "=== RustChain Miner Installation ==="
Write-Host "Started at: $(Get-Date)"
Write-Host ""

# Step 1: Install Rust if not present
Write-Host "Step 1: Checking Rust installation..."
try {
    $rustVersion = rustc --version 2>&1
    Write-Host "Rust already installed: $rustVersion"
} catch {
    Write-Host "Installing Rust..."
    Invoke-RestMethod -Uri "https://sh.rustup.rs" -OutFile "$env:TEMP\rustup-init.ps1"
    # Note: Actual installation requires user interaction
    Write-Host "Please run: Invoke-Expression ((New-Object Net.WebClient).DownloadString('https://sh.rustup.rs'))"
}

# Step 2: Build the miner
Write-Host ""
Write-Host "Step 2: Building RustChain Miner..."
Set-Location $PSScriptRoot
cargo build --release

# Step 3: Create configuration
Write-Host ""
Write-Host "Step 3: Creating configuration..."
if (!(Test-Path "config.toml")) {
    Copy-Item "config.example.toml" "config.toml"
    Write-Host "Created config.toml from example"
}

# Step 4: Show final status
Write-Host ""
Write-Host "=== Installation Complete ==="
Write-Host "Finished at: $(Get-Date)"
Write-Host "Binary location: target\release\rustchain-miner.exe"

# Stop transcript
Stop-Transcript

Write-Host ""
Write-Host "Recording saved to: $transcriptFile"
Write-Host "To convert to GIF, use: https://asciinema.org/ or terminal-to-gif tools"
