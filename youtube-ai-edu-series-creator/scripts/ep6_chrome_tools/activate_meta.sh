# bring tab 645346540 (meta.ai) to the front of window 645343510 (index looked up each time)
# EP.10 guard: NEVER pull focus while the window's active tab is EP.9's Studio tab 645346567 (parallel run) - wait and log instead
a=$(osascript -e 'tell application "Google Chrome" to return (id of active tab of window id 645343510) as text')
if [ "$a" = "645346567" ]; then echo "$(date +%T) GUARD: Studio tab 645346567 is active (EP.9) - not activating meta.ai" >> build/guard.log; exit 3; fi
i=$(osascript -e 'tell application "Google Chrome"' -e 'set r to 0' -e 'set n to count of tabs of window id 645343510' -e 'repeat with k from 1 to n' -e 'if (id of tab k of window id 645343510) as text is "645346540" then set r to k' -e 'end repeat' -e 'return r' -e 'end tell')
[ "$i" != "0" ] && osascript -e "tell application \"Google Chrome\" to set active tab index of window id 645343510 to $i"
