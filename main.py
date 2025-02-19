import os
import platform
import subprocess
import json
import requests
 
def get_default_browser():
    system = platform.system()

    if system == "Windows":
        return get_default_browser_windows()
    elif system == "Linux":
        return get_default_browser_linux()
    elif system == "Darwin":  # macOS
        return get_default_browser_macos()
    else:
        return None

def get_default_browser_windows():
    try:
        import winreg  # Windows-only module
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        default_browser, _ = winreg.QueryValueEx(key, "ProgId")
        winreg.CloseKey(key)
        
        if "BraveHTML" in default_browser:
            return "brave"
        elif "Chrome" in default_browser:
            return "chrome"
        elif "Firefox" in default_browser:
            return "firefox"
        elif "Edge" in default_browser:
            return "edge"
        elif "Safari" in default_browser:
            return "safari"
        else:
            return default_browser
    except Exception:
        return None

def get_default_browser_linux():
    try:
        result = subprocess.run(["xdg-settings", "get", "default-web-browser"], capture_output=True, text=True)
        browser = result.stdout.strip().lower()

        if "brave" in browser:
            return "brave"
        elif "chrome" in browser:
            return "chrome"
        elif "firefox" in browser:
            return "firefox"
        elif "edge" in browser:
            return "edge"
        elif "safari" in browser:
            return "safari"
        else:
            return browser
    except Exception:
        return None

def get_default_browser_macos():
    try:
        result = subprocess.run(
            ["defaults", "read", "com.apple.LaunchServices/com.apple.launchservices.secure", "LSHandlers"],
            capture_output=True, text=True
        )
        browser = result.stdout.lower()

        if "brave" in browser:
            return "brave"
        elif "chrome" in browser:
            return "chrome"
        elif "firefox" in browser:
            return "firefox"
        elif "safari" in browser:
            return "safari"
        else:
            return browser
    except Exception:
        return None
    
def get_chrome_tabs():
    try:
        response = requests.get("http://localhost:9222/json/list")
        tabs = response.json()
        urls = [tab["url"] for tab in tabs if "url" in tab]
        with open("saved_tabs.txt", "w") as f:
            for url in urls:
                f.write(url + "\n")
    except Exception as e:
        print(f"Error getting Chrome tabs: {e}")

default_browser = get_default_browser()
print(f"Default browser detected: {default_browser}")
get_chrome_tabs()


