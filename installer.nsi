; Human Flourishing Frameworks - Windows Installer
; Build with NSIS (Nullsoft Scriptable Install System)
; Download NSIS: https://nsis.sourceforge.io/Download
;
; To build the EXE:
; 1. Install NSIS from https://nsis.sourceforge.io/Download
; 2. Right-click this file: Compile NSI Scripts
; 3. Or run: makensis.exe installer.nsi
;
; Output: human-flourishing-frameworks-installer.exe

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

; Variables
!define APPNAME "Human Flourishing Frameworks"
!define APPVERSION "1.0.0"
!define APPURL "https://github.com/alex-place/human-flourishing-frameworks"
!define INSTALLERICON "installer-icon.ico"

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Installer Details
Name "${APPNAME} ${APPVERSION}"
OutFile "human-flourishing-frameworks-installer.exe"
InstallDir "$PROFILE\.hff-node"
ShowInstDetails show
ShowUninstDetails show

; Require admin rights
RequestExecutionLevel admin

; Version Info
VIProductVersion "${APPVERSION}.0"
VIAddVersionKey ProductName "${APPNAME}"
VIAddVersionKey CompanyName "Human Flourishing"
VIAddVersionKey FileDescription "Local node installer for decentralized AI fairness monitoring"
VIAddVersionKey FileVersion "${APPVERSION}"
VIAddVersionKey ProductVersion "${APPVERSION}"

Section "Install"
  SetOutPath "$INSTDIR"

  ; Show status
  DetailPrint "Downloading Human Flourishing Frameworks..."

  ; Download repository
  StrCpy $0 "https://github.com/alex-place/human-flourishing-frameworks/archive/refs/heads/master.zip"
  StrCpy $1 "$INSTDIR\hff-repo.zip"

  nsExec::ExecToLog 'powershell -NoProfile -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri ''$0'' -OutFile ''$1''}"'
  Pop $2

  ${If} $2 != 0
    MessageBox MB_ICONSTOP "Failed to download repository. Check your internet connection."
    Abort
  ${EndIf}

  DetailPrint "Extracting files..."

  ; Extract ZIP
  nsExec::ExecToLog 'powershell -NoProfile -Command "Expand-Archive -Path ''$1'' -DestinationPath ''$INSTDIR'' -Force"'

  ; Rename extracted folder
  DetailPrint "Setting up directories..."
  nsExec::ExecToLog 'powershell -NoProfile -Command "Get-ChildItem -Directory ''$INSTDIR\human-flourishing-frameworks-*'' | Select-Object -First 1 | Rename-Item -NewName ''frameworks''"'
  nsExec::ExecToLog 'powershell -NoProfile -Command "Remove-Item ''$1'' -Force"'

  ; Check Python
  DetailPrint "Checking Python installation..."
  nsExec::ExecToStack 'python --version'
  Pop $2

  ${If} $2 != 0
    DetailPrint "Python not found. Installing Python 3.12..."

    ; Download Python
    StrCpy $0 "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    StrCpy $1 "$TEMP\python-installer.exe"

    nsExec::ExecToLog 'powershell -NoProfile -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri ''$0'' -OutFile ''$1''}"'
    Pop $2

    ${If} $2 = 0
      DetailPrint "Running Python installer..."
      nsExec::ExecToLog '$1 /quiet InstallAllUsers=1 PrependPath=1'
      DetailPrint "Python installed successfully"
    ${EndIf}
  ${EndIf}

  ; Create virtual environment
  DetailPrint "Creating Python virtual environment..."
  SetOutPath "$INSTDIR\frameworks"
  nsExec::ExecToLog 'python -m venv venv'

  DetailPrint "Installing dependencies (Flask, NumPy, Requests)..."
  nsExec::ExecToLog '"$INSTDIR\frameworks\venv\Scripts\pip.exe" install -q Flask==2.3.0 numpy==1.24.0 requests==2.31.0'

  ; Create data directory
  CreateDirectory "$INSTDIR\frameworks\data"

  ; Create config file
  DetailPrint "Creating configuration..."
  FileOpen $0 "$INSTDIR\frameworks\.hff-config.json" w
  FileWrite $0 "{$\n"
  FileWrite $0 '  "node_name": "windows-node-${RANDOM}",$\n'
  FileWrite $0 '  "network": "human-flourishing-global",$\n'
  FileWrite $0 '  "api_port": 5000,$\n'
  FileWrite $0 '  "heartbeat_interval": 30,$\n'
  FileWrite $0 '  "sync_enabled": true,$\n'
  FileWrite $0 '  "central_server": "https://human-flourishing-frameworks.herokuapp.com",$\n'
  FileWrite $0 '  "data_dir": "./data",$\n'
  FileWrite $0 '  "mode": "local"$\n'
  FileWrite $0 "}"
  FileClose $0

  ; Create startup batch
  FileOpen $0 "$INSTDIR\frameworks\start-node.cmd" w
  FileWrite $0 "@echo off$\n"
  FileWrite $0 "call venv\Scripts\activate.bat$\n"
  FileWrite $0 "echo.$\n"
  FileWrite $0 "echo ======================================================================$\n"
  FileWrite $0 "echo   HUMAN FLOURISHING FRAMEWORKS - LOCAL NODE$\n"
  FileWrite $0 "echo ======================================================================$\n"
  FileWrite $0 "echo.$\n"
  FileWrite $0 "echo Dashboard: http://localhost:5000$\n"
  FileWrite $0 "echo.$\n"
  FileWrite $0 "echo Starting node...$\n"
  FileWrite $0 "echo.$\n"
  FileWrite $0 "python dashboard_app.py$\n"
  FileWrite $0 "pause"
  FileClose $0

  ; Create shortcuts
  DetailPrint "Creating shortcuts..."
  CreateDirectory "$SMPROGRAMS\${APPNAME}"

  ; Start Menu shortcut
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Start Node.lnk" "$INSTDIR\frameworks\start-node.cmd" "" "$INSTDIR\frameworks\start-node.cmd"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Dashboard.lnk" "http://localhost:5000"

  ; Desktop shortcut
  CreateShortCut "$DESKTOP\Human Flourishing Node.lnk" "$INSTDIR\frameworks\start-node.cmd"

  ; Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  DetailPrint "Installation complete!"
SectionEnd

Section "Uninstall"
  DetailPrint "Removing Human Flourishing Frameworks..."

  ; Remove shortcuts
  RMDir /r "$SMPROGRAMS\${APPNAME}"
  Delete "$DESKTOP\Human Flourishing Node.lnk"

  ; Remove installation
  RMDir /r "$INSTDIR"

  DetailPrint "Uninstall complete!"
SectionEnd

; Desktop context menu (optional)
Section "Install Desktop Shortcut"
  CreateShortCut "$DESKTOP\Human Flourishing Node.lnk" "$INSTDIR\frameworks\start-node.cmd"
SectionEnd
