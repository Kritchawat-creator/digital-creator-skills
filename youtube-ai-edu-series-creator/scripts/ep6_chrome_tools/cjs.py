#!/usr/bin/env python3
"""Run JS in a Chrome tab via AppleScript.  cjs.py <tab-id|url-substring> <js-file|-e code>
Prints the result. Async: the JS can set window.__r and you poll with -e 'window.__r'."""
import subprocess, sys, json
def osa(script):
    try: p = subprocess.run(["osascript", "-"], input=script, capture_output=True, text=True, timeout=45)
    except subprocess.TimeoutExpired: raise SystemExit("osascript timeout")
    if p.returncode: raise SystemExit(p.stderr.strip())
    return p.stdout.rstrip("\n")
def find_tab(key):
    s = '''set out to ""
tell application "Google Chrome"
 repeat with w from 1 to count of windows
  repeat with t from 1 to count of tabs of window w
   set out to out & (id of window w) & "\t" & t & "\t" & (id of tab t of window w) & "\t" & (URL of tab t of window w) & linefeed
  end repeat
 end repeat
end tell
return out'''
    for line in osa(s).splitlines():
        w, t, i, u = line.split("\t", 3)
        if key == i or (not key.isdigit() and key in u):
            return int(w), int(i)
    raise SystemExit("tab not found: " + key)
def run(key, code):
    w, t = find_tab(key)
    esc = code.replace("\\", "\\\\").replace('"', '\\"')
    return osa(f'tell application "Google Chrome" to execute (tab id {t} of window id {w}) javascript "{esc}"')
if __name__ == "__main__":
    key = sys.argv[1]
    code = sys.argv[3] if sys.argv[2] == "-e" else open(sys.argv[2]).read()
    print(run(key, code))
