import winreg
import requests
<<<<<<< HEAD
 
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
=======
import subprocess
import time

SAVE_FILE = "saved_tabs.txt"
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
>>>>>>> 6e42465 (works now but not well)

def get_default_browser_windows():
    """Gets the default browser on Windows, specifically checking for Brave or other Chromium browsers."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        default_browser, _ = winreg.QueryValueEx(key, "ProgId")
        winreg.CloseKey(key)
        
        if "BraveHTML" in default_browser:
            return "brave"
        elif "Chrome" in default_browser:
            return "chrome"
        elif "Edge" in default_browser:
            return "edge"
        else:
            return None
    except Exception:
        return None

def get_chrome_tabs():
    """Retrieves open tabs from Brave (or another Chromium browser) using the debugging API."""
    try:
        response = requests.get("http://localhost:9222/json/list")
        tabs = response.json()
        urls = [tab["url"] for tab in tabs if "url" in tab]
        
        with open("saved_tabs.txt", "w") as f:
            for url in urls:
                f.write(url + "\n")
    except Exception as e:
        print(f"Error getting tabs: {e}")

def reopen_saved_tabs():
    """Reads saved tab URLs and reopens them in Brave, ignoring extensions and scripts."""
    try:
        with open(SAVE_FILE, "r") as f:
            urls = [line.strip() for line in f.readlines()]
        
        # Filter out unwanted URLs
        urls = [url for url in urls if not url.startswith("chrome-extension://") and not url.endswith(".js")]

        for url in urls:
            subprocess.Popen([BRAVE_PATH, "--remote-debugging-port=9222", url])  # Open each URL in a new tab
        
        print(f"Reopened {len(urls)} tabs.")
    
    except Exception as e:
        print(f"Error reopening tabs: {e}")

def clear_saved_tabs():
    """Clears the contents of the saved tabs file."""
    try:
        with open(SAVE_FILE, "w") as f:
            f.write("")  # Overwrites the file with an empty string
        
        print("Saved tabs cleared.")
    
    except Exception as e:
        print(f"Error clearing saved tabs: {e}")

def close_brave():
    """Closes Brave browser if it is running."""
    try:
        subprocess.run(["taskkill", "/IM", "brave.exe", "/F"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Brave browser closed.")
    except subprocess.CalledProcessError:
        print("Brave is not running.")

def main():
    browser = get_default_browser_windows()
    if browser == "brave":
        print("Brave browser detected.")
    elif browser in ["chrome", "edge"]:
        print(f"{browser.capitalize()} browser detected.")
    else:
        print("Brave or a Chromium-based browser is not set as the default.")

    if not any(line.strip() for line in open(SAVE_FILE, "r")):
        get_chrome_tabs()
        close_brave()
    else: 
        reopen_saved_tabs()
        clear_saved_tabs()


if __name__ == "__main__":
    main()
