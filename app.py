import plistlib
import sys
from AppKit import NSWorkspace

def get_frontmost_app_path():
    """Get the path of the frontmost application."""
    return NSWorkspace.sharedWorkspace().activeApplication().get('NSApplicationPath')

def get_app_info(app_path):
    """Retrieve application information from its Info.plist."""
    info_plist_path = f"{app_path}/Contents/Info.plist"

    try:
        with open(info_plist_path, 'rb') as f:
            return plistlib.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"Error: Info.plist not found for {app_path}\n")
        return None
    except Exception as e:
        sys.stderr.write(f"Error reading plist for {app_path}: {e}\n")
        return None

def format_version(info):
    """Format the application version string."""
    short_version = info.get('CFBundleShortVersionString')
    bundle_version = info.get('CFBundleVersion')

    if short_version and bundle_version and short_version != bundle_version:
        return f"{short_version} ({bundle_version})"
    return short_version or bundle_version or "Unknown"

def get_app_name(info):
    """Get the application's display name."""
    return info.get('CFBundleDisplayName') or info.get('CFBundleName') or info.get('CFBundleExecutable')

def main():
    """Main function to get and print app version info."""
    if len(sys.argv) > 1:
        app_path = sys.argv[1]
    else:
        app_path = get_frontmost_app_path()

    if not app_path:
        sys.stderr.write("Error: Could not determine application path.\n")
        sys.exit(1)

    info = get_app_info(app_path)
    if not info:
        sys.exit(1)

    app_name = get_app_name(info)
    app_version = format_version(info)

    sys.stdout.write(f"{app_name} v{app_version}")

if __name__ == "__main__":
    main()
