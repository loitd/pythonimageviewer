;NSIS Modern User Interface
;Start Menu Folder Selection Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "Python Image Viewer"
  OutFile "piv-setup-1.0-x64.msi"
  Unicode True

  ;Default installation folder
  InstallDir "$LOCALAPPDATA\Python Image Viewer"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Python Image Viewer" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Variables

  Var StartMenuFolder

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_LICENSE "LICENSE"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  
  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Python Image Viewer" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Tran Duc Loi"
  
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
  
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections: https://stackoverflow.com/a/2814451

SectionGroup /e "All" SEC_GROUP

    Section "Python Image Viewer" SEC_PIV
        SectionIn RO
        SetOutPath "$INSTDIR"
        
        ;ADD YOUR OWN FILES HERE...: https://stackoverflow.com/a/36437539
        ;!tempfile filelist
        ;!system '"filelist.bat" ".\dist\piv" "${filelist}"'
        ;!include "${filelist}"
        File /r "dist\piv\*"
        
        ;Store installation folder
        WriteRegStr HKCU "Software\Python Image Viewer" "" $INSTDIR
        
        ;Create uninstaller
        WriteUninstaller "$INSTDIR\Uninstall.exe"
        
        !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
            ;Create shortcuts
            CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
            CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Python Image Viewer.lnk" "$INSTDIR\piv.exe"
            CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
        !insertmacro MUI_STARTMENU_WRITE_END

    SectionEnd

    ;Section "optional" SEC_OPT
    ;SectionEnd

SectionGroupEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SEC_PIV ${LANG_ENGLISH} "PIV - Python Image Viewer"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SEC_PIV} $(DESC_SEC_PIV)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END
 
;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir "$INSTDIR"
  
  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Python Image Viewer.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"
  
  DeleteRegKey /ifempty HKCU "Software\Python Image Viewer"

SectionEnd

