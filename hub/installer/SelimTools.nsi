Unicode True

!include "MUI2.nsh"
!include "LogicLib.nsh"

!define APP_NAME "Selim Tools"
!ifndef APP_VERSION
    !error "build.ps1이 /DAPP_VERSION=x.y.z 로 버전을 넘겨야 합니다"
!endif
!define APP_PUBLISHER "세림전자"
!define APP_EXE "SelimTools.exe"
!define APP_REG_KEY "Software\SelimTools"
!define UNINSTALL_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\SelimTools"

Name "${APP_NAME} ${APP_VERSION}"
OutFile "..\dist\installer\SelimTools-Setup-${APP_VERSION}.exe"
InstallDir "$LOCALAPPDATA\Programs\${APP_NAME}"
InstallDirRegKey HKCU "${APP_REG_KEY}" "InstallDir"
RequestExecutionLevel user
SetCompressor /SOLID lzma
CRCCheck on
ManifestDPIAware true
BrandingText "${APP_PUBLISHER} · 개발팀 오민상"
Icon "..\assets\icon.ico"
UninstallIcon "..\assets\icon.ico"

VIProductVersion "${APP_VERSION}.0"
VIAddVersionKey /LANG=1042 "ProductName" "${APP_NAME}"
VIAddVersionKey /LANG=1042 "ProductVersion" "${APP_VERSION}"
VIAddVersionKey /LANG=1042 "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=1042 "FileDescription" "${APP_NAME} 설치 프로그램"
VIAddVersionKey /LANG=1042 "FileVersion" "${APP_VERSION}.0"
VIAddVersionKey /LANG=1042 "LegalCopyright" "© 2026 ${APP_PUBLISHER} 개발팀 오민상P"

!define MUI_ICON "..\assets\icon.ico"
!define MUI_UNICON "..\assets\icon.ico"
!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "${APP_NAME} 실행"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Korean"

; 허브는 자기 업데이트 때 이 설치 파일을 /S로 띄우고 곧바로 종료한다.
; 실행 파일 잠금이 풀릴 때까지 최대 30초 기다린 뒤 덮어쓴다.
Function WaitForHubExit
    StrCpy $0 0
    ${DoWhile} ${FileExists} "$INSTDIR\${APP_EXE}"
        ClearErrors
        FileOpen $1 "$INSTDIR\${APP_EXE}" a
        ${IfNot} ${Errors}
            FileClose $1
            ${Break}
        ${EndIf}
        IntOp $0 $0 + 1
        ${If} $0 >= 60
            ${Break}
        ${EndIf}
        Sleep 500
    ${Loop}
FunctionEnd

Section "${APP_NAME}" SEC_MAIN
    SectionIn RO
    SetShellVarContext current
    Call WaitForHubExit
    ; 지난 버전의 라이브러리가 섞이지 않게 비우고 새로 복사한다
    RMDir /r "$INSTDIR\_internal"
    SetOutPath "$INSTDIR"
    File /r "..\dist\SelimTools\*.*"

    WriteUninstaller "$INSTDIR\Uninstall.exe"
    WriteRegStr HKCU "${APP_REG_KEY}" "InstallDir" "$INSTDIR"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayIcon" "$INSTDIR\${APP_EXE}"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKCU "${UNINSTALL_KEY}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoModify" 1
    WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoRepair" 1

    CreateShortcut "$SMPROGRAMS\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    ; 자동 업데이트(/S) 때는 사용자가 지운 바탕화면 바로가기를 되살리지 않는다
    ${IfNot} ${Silent}
        CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
    ${EndIf}
SectionEnd

Function .onInstSuccess
    ; 자동 업데이트 뒤에는 허브를 다시 연다. 대화형 설치는 마침 화면의 "실행"으로 연다
    ${If} ${Silent}
        Exec '"$INSTDIR\${APP_EXE}"'
    ${EndIf}
FunctionEnd

Section "Uninstall"
    SetShellVarContext current
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}.lnk"
    DeleteRegKey HKCU "${UNINSTALL_KEY}"
    DeleteRegKey HKCU "${APP_REG_KEY}"
    ; 허브가 설치한 프로그램과 그 데이터(%LOCALAPPDATA%\SelimTools)는 지우지 않는다
    RMDir /r "$INSTDIR"
SectionEnd
