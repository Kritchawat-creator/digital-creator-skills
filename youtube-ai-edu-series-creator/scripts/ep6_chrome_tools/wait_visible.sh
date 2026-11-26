# wait until the screen is unlocked and the meta.ai tab is visible and hydrated; keep the display awake
cd ~/Documents/Kritchawat-Projects/Series/pudding-speaks-english/pudding-ep10
while true; do
  if ioreg -n Root -d1 | grep -q 'IOConsoleLocked" = Yes'; then sleep 20; continue; fi   # EP.9: AppleScript to Chrome hangs while the Mac is locked/asleep
  r=$(python3 tools/cjs.py 645346540 -e "document.hidden+' '+document.querySelectorAll('[contenteditable=true]').length" 2>&1)
  case "$r" in
    "true "*) osascript -e 'tell application "Google Chrome" to set active tab index of window id 645343510 to 3' >/dev/null 2>&1;;
    "false 0") osascript -e 'tell application "Google Chrome" to reload tab id 645346540 of window id 645343510'; sleep 20;;
    "false "*) break;;
  esac
  sleep 15
done
pgrep -x caffeinate >/dev/null || (caffeinate -d -t 50000 >/dev/null 2>&1 &)
echo "VISIBLE $(date +%T)"
