import sys

try:
    from app_functions.open_app import find_best_match, load_apps
except Exception as e:
    print(f"Import error: {e}")
    sys.stdout.flush()
    sys.exit(2)

print("Python script gestart")
sys.stdout.flush()

def check_for_dangerous_apps():
    try:
        apps = load_apps()
        
        if not apps:
            print("No apps loaded")
            sys.stdout.flush()
            return

        dangerous_apps = find_best_match(apps, "Nvidia App")
        if dangerous_apps:
            print(f"Found dangerous app: {dangerous_apps}")
        else:
            print("No dangerous apps found")

    except Exception as e:
        print(f"Runtime error: {e}")
        sys.stdout.flush()
        sys.exit(2)

    sys.stdout.flush()

if __name__ == "__main__":
    check_for_dangerous_apps()
