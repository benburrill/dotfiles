alias wps='powershell.exe'
alias wpst='wt.exe -w 0 nt -p "Windows PowerShell" -d .'
alias wpss='wt.exe -w 0 sp -p "Windows PowerShell" -d .'

# sud'oh - run commands as root without the pesky inconvenience of
# needing to enter a password.
alias sudoh='wsl.exe -u root'
alias fixclock='sudoh hwclock -s'
function checkclock {
    echo "Win: $(powershell.exe -Command Date -UFormat %c)"
    echo "WSL: $(date +%c)"
}
