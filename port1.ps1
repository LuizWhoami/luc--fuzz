param($ip)
if(!$ip){
echo "===LuizWhoami==="
echo "Scan_of_ports_open"
echo "===LuizWhoami==="
echo " "
echo "Use: ./scanports.exe 10.0.0.0"
}
else {
foreach ($porta in 1..254){
if (tnc $ip -Port $porta -WarningAction SilentlyContinue -InformationLevel Quiet){
    echo "Opened: $ip : $porta"
}
else{
echo "Close: $ip : $porta"}
}}
