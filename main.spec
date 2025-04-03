# -*- mode: python -*-
# type: ignore
import os
import pathlib
import sys
import time

import pkg_resources


# os.environ["PYPI_RELEASE"] = "1"

sys.setrecursionlimit(5000)
print("Arguments:", sys.argv)
MODULE_NAME = "chatly"
VERSION = "2.12.0"
QT_FRAMEWORK = os.environ.get("PYINSTALLER_QT_API", "PyQt6")
CONSOLE = os.environ.get("PYINSTALLER_CONSOLE", True)
SPEC_FILE_PATH = pathlib.Path(SPECPATH)
MODULE_PATH = SPEC_FILE_PATH / "src" / MODULE_NAME

BLOCK_CIPHER = None

# check for modules which break the build
installed = {pkg.key for pkg in pkg_resources.working_set}
invalid_modules = ["typing", "pathlib3x", "pathlib"]
for mod in invalid_modules:
    if mod in installed:
        msg = f"{mod} module installed. Remove it."
        raise Exception(msg)  # noqa: TRY002


DATAS = [
    # (str(MODULE_PATH / "plugins"), f"{MODULE_NAME}\\plugins"),
    # (str(MODULE_PATH / "locales"), f"{MODULE_NAME}\\locales"),
    # (str(MODULE_PATH / "resources"), f"{MODULE_NAME}\\resources"),
    # # (str(MODULE_PATH / "Qt5Core.dll"), "PyQt5\\Qt\\bin\\"),
    # (str(MODULE_PATH / "logging.yaml"), f"{MODULE_NAME}\\"),
    # (str(MODULE_PATH / "config_default.yaml"), f"{MODULE_NAME}\\"),
    # (str(SPEC_FILE_PATH / "docs/site"), f"{MODULE_NAME}\\docs"),
    # (str(pathlib.Path(HOMEPATH) / "fastparquet.libs"), "fastparquet.libs"),
]

IMPORTS = [QT_FRAMEWORK]
frameworks = {"PyQt5", "PyQt6", "PySide6"}
frameworks.remove(QT_FRAMEWORK)
excluded_modules = list(frameworks)

if sys.platform.startswith("win"):
    from PyInstaller.utils.win32.versioninfo import (
        FixedFileInfo,
        StringFileInfo,
        StringStruct,
        StringTable,
        VarFileInfo,
        VarStruct,
        VSVersionInfo,
    )

    # For more details about fixed file info 'ffi' see:
    # http://msdn.microsoft.com/en-us/library/ms646997.aspx
    year = time.localtime().tm_year
    company_name = "AIStack"
    product_name = "Chatly"
    version_tuple = tuple(int(i) for i in f"{VERSION}.0".split("."))
    copyright = "© 2025 " + (" - %d " % (year,) if year > 2025 else "") + company_name
    win_version = VSVersionInfo(
        ffi=FixedFileInfo(
            # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
            # Set not needed items to zero 0.
            filevers=version_tuple,
            prodvers=version_tuple,
            # Contains a bitmask that specifies the valid bits 'flags'r
            mask=0x3F,
            # Contains a bitmask that specifies the Boolean attributes of the file.
            flags=0x0,
            # The operating system for which this file was designed.
            # 0x4 - NT and there is no need to change it.
            OS=0x40004,
            # The general type of file.
            # 0x1 - the file is an application.
            fileType=0x1,
            # The function of the file.
            # 0x0 - the function is not defined for this fileType
            subtype=0x0,
            # Creation date and time stamp.
            date=(0, 0),
        ),
        kids=[
            StringFileInfo([
                StringTable(
                    "040904B0",
                    [
                        StringStruct("CompanyName", company_name),
                        StringStruct("FileDescription", product_name),
                        StringStruct("FileVersion", f"{VERSION}.0"),
                        StringStruct("InternalName", MODULE_NAME),
                        StringStruct("LegalCopyright", copyright),
                        StringStruct("OriginalFilename", f"{MODULE_NAME}.exe"),
                        StringStruct("ProductName", product_name),
                        StringStruct("ProductVersion", f"{VERSION}.0"),
                    ],
                )
            ]),
            VarFileInfo([VarStruct("Translation", [1033, 1200])]),
        ],
    )
else:
    win_version = None

a = Analysis(
    [str(SPEC_FILE_PATH / "src" / MODULE_NAME / "__main__.py")],
    pathex=[str(SPEC_FILE_PATH)],
    binaries=[],
    datas=DATAS,
    hiddenimports=IMPORTS,
    hookspath=[str(SPEC_FILE_PATH / "hooks")],
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=BLOCK_CIPHER,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=BLOCK_CIPHER)

exe = EXE(
    pyz,
    a.scripts,
    [],  # this or....
    # Static link the Visual C++ Redistributable DLLs if on Windows
    # a.binaries + [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
    #               ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
    # if sys.platform == 'win32' else a.binaries,
    exclude_binaries=True,
    name=MODULE_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=CONSOLE,
    icon="resources\\icon.ico",
    version=win_version,
)

app = BUNDLE(
    exe,
    name=f"{MODULE_NAME}.app",
    icon=f"{MODULE_NAME}\\resources\\icon.ico",
    bundle_identifier=None,
    info_plist={
        "NSPrincipalClass": "NSApplication",
        "NSAppleScriptEnabled": False,
        "CFBundleDocumentTypes": [
            {
                "CFBundleTypeName": "My File Format",
                "CFBundleTypeIconFile": "MyFileIcon.icns",
                "LSItemContentTypes": ["com.example.myformat"],
                "LSHandlerRank": "Owner",
            }
        ],
    },
)


coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name=MODULE_NAME
)
