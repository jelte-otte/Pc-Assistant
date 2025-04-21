import os
import winreg
import glob
import subprocess
import json
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

load_dotenv()
EXCLUDED_TERMS = [s.strip().lower() for s in os.getenv("EXCLUDED_APPS", "").split(",")]

def is_excluded(app_name):
    for term in EXCLUDED_TERMS:
        score = fuzz.partial_ratio(term, app_name.lower())
        if score >= 80:
            return True
    return False


def get_installed_apps():
    apps = {}
    apps.update(get_registry_apps())
    apps.update(get_start_menu_shortcuts())
    apps.update(get_uwp_apps())

    # Filter uitsluitingen
    filtered_apps = {k: v for k, v in apps.items() if not is_excluded(k)}

    # Opslaan
    os.makedirs("apps", exist_ok=True)
    with open(os.path.join("apps", "installed_apps.json"), "w", encoding="utf-8") as f:
        json.dump(filtered_apps, f, indent=2, ensure_ascii=False)

    print(f"{len(filtered_apps)} apps opgeslagen in installed_apps.json")

def get_registry_apps():
    apps = {}
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
        for key_path in reg_paths:
            try:
                reg_key = winreg.OpenKey(root, key_path)
                for i in range(winreg.QueryInfoKey(reg_key)[0]):
                    try:
                        sub_key_name = winreg.EnumKey(reg_key, i)
                        sub_key = winreg.OpenKey(reg_key, sub_key_name)
                        display_name, _ = winreg.QueryValueEx(sub_key, 'DisplayName')

                        try:
                            display_icon, _ = winreg.QueryValueEx(sub_key, 'DisplayIcon')
                            exe_path = display_icon.split(",")[0].strip('"')
                            if os.path.isfile(exe_path):
                                apps[display_name] = exe_path
                                continue
                        except FileNotFoundError:
                            pass

                        try:
                            install_location, _ = winreg.QueryValueEx(sub_key, 'InstallLocation')
                            if install_location and os.path.isdir(install_location):
                                apps[display_name] = install_location
                        except FileNotFoundError:
                            pass
                    except Exception:
                        continue
            except FileNotFoundError:
                continue
    return apps

def get_start_menu_shortcuts():
    shortcuts = {}
    search_paths = [
        os.path.join(os.environ['APPDATA'], r"Microsoft\Windows\Start Menu\Programs"),
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.join(os.environ['USERPROFILE'], "Desktop")
    ]
    for base in search_paths:
        if os.path.isdir(base):
            for path in glob.glob(base + "/**/*.lnk", recursive=True):
                name = os.path.splitext(os.path.basename(path))[0]
                shortcuts[name] = path
    return shortcuts

def get_uwp_apps():
    uwp_apps = {}
    try:
        output = subprocess.check_output(
            ['powershell', '-Command', '''
            $apps = Get-AppxPackage
            foreach ($app in $apps) {
                $manifest = Get-AppxPackageManifest $app
                foreach ($id in $manifest.Package.Applications.Application.Id) {
                    "$($app.Name) = $($app.PackageFamilyName)!$id"
                }
            }
            '''],
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in output.strip().split('\n'):
            if '=' in line:
                name, aumid = line.strip().split('=', 1)
                uwp_apps[name.strip()] = f"shell:AppsFolder\\{aumid.strip()}"
    except Exception as e:
        print(f"Fout bij het ophalen van UWP-apps: {e}")
    return uwp_apps

if __name__ == "__main__":
    get_installed_apps()
