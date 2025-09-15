import subprocess
import sys

def get_os_version_info():
    """Get macOS version and build number using a single call to sw_vers."""
    try:
        # The `sw_vers` command without arguments provides all info at once.
        output = subprocess.check_output(['sw_vers']).decode('utf-8')
        lines = output.strip().split('\n')
        version_info = {}
        for line in lines:
            # The separator is a tab character.
            key, value = line.split(':\t', 1)
            version_info[key.strip()] = value.strip()
        return version_info
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        sys.stderr.write(f"Error getting OS version: {e}\n")
        return None

def main():
    """Main function to get and print formatted OS version info."""
    version_info = get_os_version_info()
    if not version_info:
        sys.exit(1)

    # The product name is consistently "macOS" on modern systems.
    product_name = "macOS"
    version = version_info.get('ProductVersion')
    build = version_info.get('BuildVersion')

    if version and build:
        sys.stdout.write(f"{product_name} {version} ({build})")
    else:
        sys.stderr.write("Error: Could not parse OS version information.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()