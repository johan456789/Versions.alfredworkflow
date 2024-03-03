import plistlib
from AppKit import NSWorkspace
from sys import stdout
from sys import argv
from xml.parsers.expat import ExpatError


def binary_plist_to_file_obj(filename):
    "Pipe the binary plist through plutil and return as file object"
    from subprocess import Popen, PIPE
    from StringIO import StringIO

    with open(filename, "rb") as f:
        content = f.read()
    args = ["plutil", "-convert", "xml1", "-o", "-", "--", "-"]
    p = Popen(args, stdin=PIPE, stdout=PIPE)
    out, err = p.communicate(content)
    return StringIO(out)


path = ''

if len(argv) > 1:
    path = argv[1]

if path == '':
    path = NSWorkspace.sharedWorkspace().activeApplication().get('NSApplicationPath')

path += '/Contents/Info.plist'
try:
    with open(path, 'rb') as f:
        info = plistlib.load(f)
except(ExpatError):  # binary plist
    with open(binary_plist_to_file_obj(path), 'rb') as f:
        info = plistlib.load(f)

appName = info.get('CFBundleExecutable')
if 'CFBundleDisplayName' in info:
    appName = info.get('CFBundleDisplayName')
elif 'CFBundleName' in info:
    appName = info.get('CFBundleName')

appVersion = info.get('CFBundleVersion')
appShortVersion = info.get('CFBundleShortVersionString')
if appShortVersion and appVersion:
    if appVersion != appShortVersion:
        appVersion = appShortVersion + ' (' + appVersion + ')'
elif not appVersion and appShortVersion:
    appVersion = appShortVersion

stdout.write(appName + ' v' + appVersion)
