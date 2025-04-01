!define APP_NAME "DataCook"
!define MODULE_NAME "processanalyzer"
!define COMP_NAME "University of Wuppertal"
!define WEB_SITE "https://www.risk-management.uni-wuppertal.de/"
!define VERSION "2.12.0"
!define COPYRIGHT "Philipp Temminghoff  © 2019"
!define DESCRIPTION "Data analysis tool"
!define INSTALLER_NAME "${MODULE_NAME}-installer.exe"
!define MAIN_APP_EXE "${MODULE_NAME}.exe"
!define LICENSE_TXT "LICENSE"
!define INSTALL_TYPE "SetShellVarContext current"
!define REG_ROOT "HKCU"
!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
!define APP_DIR "$INSTDIR\${MODULE_NAME}"
!define APP_ICON "${MODULE_NAME}/resources/icon.ico"
!define HEADER_IMAGE "${MODULE_NAME}/resources/installer_header.jpg"

######################################################################

VIProductVersion  "${VERSION}.0"
VIAddVersionKey "ProductName"  "${APP_NAME}"
VIAddVersionKey "CompanyName"  "${COMP_NAME}"
VIAddVersionKey "LegalCopyright"  "${COPYRIGHT}"
VIAddVersionKey "FileDescription"  "${DESCRIPTION}"
VIAddVersionKey "FileVersion"  "${VERSION}.0"

######################################################################

SetCompressor ZLIB
Name "${APP_NAME}"
Caption "${APP_NAME}"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME}"
XPStyle on
InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
InstallDir "$PROGRAMFILES64\${APP_NAME}"

######################################################################

!include "MUI2.nsh"

!define MUI_ICON "${APP_ICON}"
!define MUI_HEADERIMAGE_BITMAP "${HEADER_IMAGE}"
; !define MUI_COMPONENTSPAGE_TEXT_TOP "Choose components"
!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${LICENSE_TXT}"
; !insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

!ifdef REG_START_MENU
!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "${APP_NAME}"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REG_ROOT}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${UNINSTALL_PATH}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${REG_START_MENU}"
!insertmacro MUI_PAGE_STARTMENU Application $SM_Folder
!endif

!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_RUN "${APP_DIR}\${MAIN_APP_EXE}"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_SHOWREADME "${APP_DIR}\${MODULE_NAME}\docs\index.html"

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM

!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "German"

Function .onInit

  !insertmacro MUI_LANGDLL_DISPLAY

FunctionEnd

; The "" makes the section hidden.
Section "" SecUninstallPrevious

    Call UninstallPrevious

SectionEnd

Function UninstallPrevious

    ; Check for uninstaller.
    ReadRegStr $R0 "${REG_ROOT}" "${REG_APP_PATH}" ""

    ${If} $R0 == ""
        Goto Done
    ${EndIf}

    DetailPrint "Detected installation at $R0."
    DetailPrint "Removing previous installation."

    ; Run the uninstaller silently.
    ExecWait '"$R0\uninstall.exe" /S _?=$R0'

    Done:

FunctionEnd



######################################################################

Section -MainProgram
${INSTALL_TYPE}
SetOverwrite ifnewer
SetOutPath "$INSTDIR"
File /nonfatal /a /r dist\*.* ; the payload of this installer is described in an externally generated list of files

SectionEnd

######################################################################

Section -Icons_Reg
SetOutPath "$INSTDIR"
WriteUninstaller "$INSTDIR\uninstall.exe"

!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
CreateDirectory "$SMPROGRAMS\$SM_Folder"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk" "${APP_DIR}\${MAIN_APP_EXE}"
WriteIniStr "$INSTDIR\${APP_NAME} website.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\$SM_Folder\${APP_NAME} Website.lnk" "$INSTDIR\${APP_NAME} website.url"
!insertmacro MUI_STARTMENU_WRITE_END
!endif

!ifndef REG_START_MENU
CreateDirectory "$SMPROGRAMS\${APP_NAME}"
CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "${APP_DIR}\${MAIN_APP_EXE}"
WriteIniStr "$INSTDIR\${APP_NAME} website.url" "InternetShortcut" "URL" "${WEB_SITE}"
CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME} Website.lnk" "$INSTDIR\${APP_NAME} website.url"
!endif

CreateShortCut "$INSTDIR\${APP_NAME}.lnk" "${APP_DIR}\${MAIN_APP_EXE}"

WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayName" "${APP_NAME}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "UninstallString" "$INSTDIR\uninstall.exe"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayIcon" "${APP_DIR}\${MAIN_APP_EXE}"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "DisplayVersion" "${VERSION}.0"
WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "Publisher" "${COMP_NAME}"

WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}"  "URLInfoAbout" "${WEB_SITE}"

SectionEnd

######################################################################

Section Uninstall
${INSTALL_TYPE}

RmDir /r "${APP_DIR}"
Delete "$INSTDIR\uninstall.exe"
Delete "$INSTDIR\${APP_NAME} website.url"
Delete "$INSTDIR\${APP_NAME}.lnk"

RmDir "$INSTDIR"


!ifdef REG_START_MENU
!insertmacro MUI_STARTMENU_GETFOLDER "Application" $SM_Folder
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME}.lnk"
Delete "$SMPROGRAMS\$SM_Folder\${APP_NAME} Website.lnk"
RmDir "$SMPROGRAMS\$SM_Folder"
!endif

!ifndef REG_START_MENU
Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME} Website.lnk"
RmDir "$SMPROGRAMS\${APP_NAME}"
!endif

DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd

######################################################################
