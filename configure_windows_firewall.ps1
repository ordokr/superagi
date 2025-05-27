# PowerShell script to configure Windows Firewall for SuperAGI and LM Studio
# Run this script as Administrator on Windows

Write-Host "Configuring Windows Firewall for SuperAGI and LM Studio..." -ForegroundColor Green

# Allow SuperAGI port 3000 (inbound)
Write-Host "Adding firewall rule for SuperAGI port 3000..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "SuperAGI Port 3000" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow -Profile Any

# Allow LM Studio port 1234 (inbound)
Write-Host "Adding firewall rule for LM Studio port 1234..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "LM Studio Port 1234" -Direction Inbound -Protocol TCP -LocalPort 1234 -Action Allow -Profile Any

# Allow WSL subnet access (172.16.0.0/12 covers most WSL configurations)
Write-Host "Adding firewall rule for WSL subnet access..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "WSL Subnet Access" -Direction Inbound -Protocol TCP -RemoteAddress 172.16.0.0/12 -Action Allow -Profile Any

# Allow specific WSL IP range (172.31.0.0/16 for current WSL instance)
Write-Host "Adding firewall rule for current WSL IP range..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "WSL Current Range" -Direction Inbound -Protocol TCP -RemoteAddress 172.31.0.0/16 -Action Allow -Profile Any

# Show current firewall rules for verification
Write-Host "`nCurrent firewall rules for SuperAGI and LM Studio:" -ForegroundColor Green
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*SuperAGI*" -or $_.DisplayName -like "*LM Studio*" -or $_.DisplayName -like "*WSL*"} | Select-Object DisplayName, Direction, Action, Enabled

Write-Host "`nFirewall configuration complete!" -ForegroundColor Green
Write-Host "You can now access SuperAGI from WSL at http://192.168.0.144:3000" -ForegroundColor Cyan
Write-Host "LM Studio should be accessible from WSL at http://192.168.0.144:1234" -ForegroundColor Cyan
