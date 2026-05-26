import os
import sys
import re
import importlib

R = "\033[0m"
C = "\033[36m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
M = "\033[35m"

RED_DOT = "\033[38;2;255;50;50m\u25cf\033[0m"
YEL_DOT = "\033[38;2;255;200;50m\u25cf\033[0m"
BLU_DOT = "\033[38;2;50;150;255m\u25cf\033[0m"
GRY_DOT = "\033[38;2;120;120;120m\u25cf\033[0m"


DANGEROUS = {
    "ACCOUNT", "AFFECTS_BATTERY", "BIND_ACCESSIBILITY", "BLUETOOTH_ADMIN",
    "BLUETOOTH_PRIVILEGED", "BODY_SENSORS", "BROADCAST_SMS",
    "CALL_PHONE", "CALL_PRIVILEGED", "CAMERA", "CAPTURE_AUDIO_OUTPUT",
    "CAPTURE_SECURE_VIDEO_OUTPUT", "CAPTURE_VIDEO_OUTPUT",
    "CONTROL_LOCATION_UPDATES", "DELETE_PACKAGES", "DUMP",
    "FACTORY_TEST", "GET_ACCOUNTS", "GET_TASKS", "GLOBAL_SEARCH",
    "INSTALL_LOCATION_PROVIDER", "INSTALL_PACKAGES", "INTERNAL_SYSTEM_WINDOW",
    "KILL_BACKGROUND_PROCESSES", "LOCATION_HARDWARE", "MANAGE_ACCOUNTS",
    "MANAGE_DOCUMENTS", "MASTER_CLEAR", "MEDIA_CONTENT_CONTROL",
    "MODIFY_AUDIO_SETTINGS", "MODIFY_PHONE_STATE", "MOUNT_FORMAT_FILESYSTEMS",
    "MOUNT_UNMOUNT_FILESYSTEMS", "NFC", "PACKAGE_USAGE_STATS",
    "PERSISTENT_ACTIVITY", "PROCESS_OUTGOING_CALLS", "READ_CALENDAR",
    "READ_CALL_LOG", "READ_CELL_BROADCASTS", "READ_CONTACTS",
    "READ_EXTERNAL_STORAGE", "READ_FRAME_BUFFER", "READ_HISTORY_BOOKMARKS",
    "READ_INPUT_STATE", "READ_INSTALL_SESSIONS", "READ_LOGS",
    "READ_PHONE_STATE", "READ_PROFILE", "READ_SMS", "READ_SOCIAL_STREAM",
    "READ_SYNC_SETTINGS", "READ_SYNC_STATS", "READ_USER_DICTIONARY",
    "REBOOT", "RECEIVE_BOOT_COMPLETED", "RECEIVE_MMS", "RECEIVE_SMS",
    "RECEIVE_WAP_PUSH", "RECORD_AUDIO", "REORDER_TASKS",
    "RESTART_PACKAGES", "SEND_RESPOND_VIA_MESSAGE", "SEND_SMS",
    "SET_ACTIVITY_WATCHER", "SET_ALWAYS_FINISH", "SET_ANIMATION_SCALE",
    "SET_DEBUG_APP", "SET_ORIENTATION", "SET_PROCESS_LIMIT",
    "SET_TIME", "SET_TIME_ZONE", "SET_WALLPAPER", "SET_WALLPAPER_HINTS",
    "SIGNAL_PERSISTENT_PROCESSES", "STATUS_BAR", "SUBSCRIBED_FEEDS_READ",
    "SUBSCRIBED_FEEDS_WRITE", "SYSTEM_ALERT_WINDOW", "TRANSMIT_IR",
    "UNINSTALL_SHORTCUT", "UPDATE_DEVICE_STATS", "USE_CREDENTIALS",
    "USE_SIP", "VIBRATE", "WAKE_LOCK", "WRITE_APN_SETTINGS",
    "WRITE_CALENDAR", "WRITE_CALL_LOG", "WRITE_CONTACTS",
    "WRITE_EXTERNAL_STORAGE", "WRITE_GSERVICES", "WRITE_HISTORY_BOOKMARKS",
    "WRITE_INPUT_STATE", "WRITE_PROFILE", "WRITE_SECURE_SETTINGS",
    "WRITE_SETTINGS", "WRITE_SMS", "WRITE_SOCIAL_STREAM",
    "WRITE_SYNC_SETTINGS", "WRITE_USER_DICTIONARY",
}

NORMAL = {
    "ACCESS_LOCATION_EXTRA_COMMANDS", "ACCESS_NETWORK_STATE",
    "ACCESS_NOTIFICATION_POLICY", "ACCESS_WIFI_STATE",
    "ACCESS_WIMAX_STATE", "BLUETOOTH", "BROADCAST_PACKAGE_REMOVED",
    "BROADCAST_STICKY", "CHANGE_COMPONENT_ENABLED_STATE",
    "CHANGE_CONFIGURATION", "CHANGE_NETWORK_STATE",
    "CHANGE_WIFI_MULTICAST_STATE", "CHANGE_WIFI_STATE",
    "CHANGE_WIMAX_STATE", "CLEAR_APP_CACHE", "CLEAR_APP_USER_DATA",
    "CONFIRM_FULL_BACKUP", "CONNECTIVITY_INTERNAL",
    "DISABLE_KEYGUARD", "DOWNLOAD_CACHE_NON_PURGEABLE",
    "DOWNLOAD_WITHOUT_NOTIFICATION", "EXPAND_STATUS_BAR",
    "FLASHLIGHT", "FORCE_BACK", "GET_ACCOUNTS_PRIVILEGED",
    "GET_PACKAGE_SIZE", "GET_TOP_ACTIVITY_INFO", "INSTALL_SHORTCUT",
    "INTERACT_ACROSS_USERS", "INTERNATIONAL_SMS",
    "MANAGE_USERS", "MEDIA_LOCATION", "NFC_TRANSACTION_EVENT",
    "NOTIFICATION_DURING_SETUP", "OEM_UNLOCK_STATE",
    "PACKAGE_ROLLBACK_AGENT", "PERFORM_CDMA_PROVISIONING",
    "READ_MEDIA_AUDIO", "READ_MEDIA_IMAGES", "READ_MEDIA_VIDEO",
    "READ_NETWORK_USAGE_HISTORY", "READ_PRECISE_PHONE_STATE",
    "READ_SEARCH_INDEXABLES", "READ_VOICEMAIL", "REQUEST_COMPANION_RUN_IN_BACKGROUND",
    "REQUEST_COMPANION_USE_DATA_IN_BACKGROUND", "REQUEST_DELETE_PACKAGES",
    "REQUEST_INSTALL_PACKAGES", "REQUEST_OBSERVE_COMPANION_DEVICE_PRESENCE",
    "REQUEST_PASSWORD_COMPLEXITY", "SCHEDULE_EXACT_ALARM",
    "SEND_DEVICE_CUSTOMIZATION_READY", "SET_WALLPAPER_COMPONENT",
    "START_FOREGROUND_SERVICES_FROM_BACKGROUND", "USE_BIOMETRIC",
    "USE_FINGERPRINT", "USE_FULL_SCREEN_INTENT",
    "USE_ICC_AUTH_WITH_DEVICE_IDENTIFIER", "WIFI_SET_DEVICE_MOBILITY_STATE",
    "WRITE_MEDIA_STORAGE", "WRITE_VOICEMAIL",
}

SIGNATURE = {
    "ACCESS_CHECKIN_PROPERTIES", "ACCESS_DRM", "ACCESS_MOCK_LOCATION",
    "ACCESS_SURFACE_FLINGER", "ASEC_ACCESS", "ASEC_CREATE",
    "ASEC_DESTROY", "ASEC_MOUNT_UNMOUNT", "ASEC_RENAME",
    "AUTHENTICATE_ACCOUNTS", "BACKUP", "BATTERY_STATS",
    "BIND_APPWIDGET", "BIND_CALL_REDIRECTION_SERVICE",
    "BIND_CARRIER_MESSAGING_SERVICE", "BIND_CARRIER_SERVICES",
    "BIND_CHOOSER_TARGET_SERVICE", "BIND_CONDITION_PROVIDER_SERVICE",
    "BIND_CONNECTION_SERVICE", "BIND_DEVICE_ADMIN",
    "BIND_DIRECTORY_SEARCH", "BIND_DREAM_SERVICE",
    "BIND_INCIDENT_REPORT_SERVICE", "BIND_INPUT_METHOD",
    "BIND_JOB_SERVICE", "BIND_KEYGUARD_APPWIDGET",
    "BIND_MIDI_DEVICE_SERVICE", "BIND_NFC_SERVICE",
    "BIND_NOTIFICATION_LISTENER_SERVICE", "BIND_PRINT_SERVICE",
    "BIND_QUICK_ACCESS_WIDGET", "BIND_REMOTEVIEWS",
    "BIND_SCREENING_SERVICE", "BIND_TELECOM_CONNECTION_SERVICE",
    "BIND_TEXT_SERVICE", "BIND_TV_INPUT", "BIND_VOICE_INTERACTION",
    "BIND_VPN_SERVICE", "BIND_WALLPAPER", "BIND_WIFI_SERVICE",
    "BRICK", "C2D_MESSAGE", "CACHE_CONTENT", "CHANGE_BACKGROUND_DATA_SETTING",
    "CONTROL_KEYGUARD", "COPY_PROTECTED_DATA", "CREATE_USERS",
    "CRYPT_KEEPER", "DELETE_CACHE_FILES", "DEVICE_POWER",
    "DIAGNOSTIC", "DISPATCH_NFC_MESSAGE", "DISTRIBUTED_NETWORK",
    "FOREGROUND_SERVICE", "GET_DETAILED_TASKS", "HARDWARE_TEST",
    "INJECT_EVENTS", "INSTALL_GRANT_RUNTIME_PERMISSION",
    "INTERACT_ACROSS_USERS_FULL", "LOOP_RADIO", "MANAGE_APP_TOKENS",
    "MANAGE_DEVICE_ADMINS", "MANAGE_EXTERNAL_STORAGE",
    "MANAGE_MEDIA", "MANAGE_ONGOING_CALLS", "MANAGE_OWN_CALLS",
    "MANAGE_WIFI_INTERFACES", "MONITOR_INPUT", "MONITOR_KEYBOARD_AND_NAVIGATION",
    "MOVE_PACKAGE", "OBSERVE_GRANT_REVOKE_PERMISSIONS",
    "PACKAGE_ROLLBACK_AGENT", "PACKAGE_VERIFICATION_AGENT",
    "PROCESS_OUTGOING_CALLS", "READ_CLIPBOARD", "READ_CONTENT_PROVIDER",
    "READ_DEVICE_CONFIG", "READ_OEM_UNLOCK_STATE", "READ_OWNER_DATA",
    "READ_PHONE_NUMBERS", "READ_PRIVILEGED_PHONE_STATE",
    "RECEIVE_DATA_ACTIVITY_CHANGE", "RECORD_AUDIO_OUTPUT",
    "REGISTER_CALL_PROVIDER", "REGISTER_SIM_SUBSCRIPTION",
    "REMOTE_AUDIO_PLAYBACK", "REMOVE_DRM_CERTIFICATES",
    "REPLACED_BY_CURRENT", "RETRIEVE_WINDOW_CONTENT",
    "REVOKE_RUNTIME_PERMISSIONS", "RUN_USER_INIT_SCRIPTS",
    "SERIAL_PORT", "SET_KEYBOARD_LAYOUT", "SET_POINTER_SPEED",
    "SET_SCREEN_COMPATIBILITY", "SET_WALLPAPER_DIMAMOUNT",
    "SHUTDOWN", "SMS_FINANCIAL_TRANSACTIONS", "START_ANY_ACTIVITY",
    "START_TASKS_FROM_RECENTS", "STATUS_BAR_SERVICE",
    "STOP_APP_SWITCHES", "STORAGE_INTERNAL", "SUBPERMISSION",
    "SUSPEND_APPS", "TETHER_PRIVILEGED", "TRIGGER_KEYGUARD",
    "TRUST_LISTENER", "TV_INPUT_HARDWARE", "UNLIMITED_TOASTS",
    "UNPARENT", "UPDATE_LOCK", "USER_ACTIVITY",
    "USE_CREDENTIALS", "WATCH_APPOPS", "WIFI_ACCESS_STATE",
    "WIFI_CONFIGURE", "WIFI_DEVICE_OWNER_CONFIGS_LOCKDOWN",
    "WIFI_MANAGED_NETWORKS", "WIFI_UPDATE_USABILITY_SCORE_SCORE",
    "WRITE_CLIPBOARD", "WRITE_CONTENT_PROVIDER",
    "WRITE_DEVICE_CONFIG", "WRITE_OWNER_DATA", "WRITE_SETTINGS_HOMEPAGE",
}


def classify_permission(perm_name):
    short = perm_name.split(".")[-1].upper() if "." in perm_name else perm_name.upper()
    if short in DANGEROUS:
        return "dangerous", RED_DOT
    if short in SIGNATURE:
        return "signature", BLU_DOT
    if short in NORMAL:
        return "normal", YEL_DOT
    return "unknown", GRY_DOT


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def center_text(text, base=None):
    width = base or len(text)
    cols = os.get_terminal_size().columns
    pad = max(0, (cols - width) // 2)
    return " " * pad + text


def print_banner():
    colors = ["\033[38;2;90;90;90m", "\033[38;2;120;120;120m", "\033[38;2;170;170;170m", "\033[38;2;220;220;220m"]
    texts = [
        "                       ▄          ",
        "█▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀█ █▀▀█ █    █ █▀▀▀",
        "█  █ █  █ █▀▀▀ █  █ █  █ █▀▀▀ ▀█  █▀ ▀▀▀█",
        "▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀  ▀ ▀▀▀▀ ▀▀▀▀   ▀▀   ▀▀▀▀",
    ]
    max_w = max(len(l) for l in texts)
    reset = "\033[0m"
    for i, line in enumerate(texts):
        print(center_text(f"{colors[i]}{line}{reset}", base=max_w))
    print(center_text(f"\033[38;2;255;255;255m     APK ANALYZER | www.opendevs.lat{reset}", base=42))
    print()


def wait_for_enter():
    print(center_text("Presiona Enter para seleccionar archivo APK"))
    print(center_text("\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"))
    input(center_text("\u276f ", base=41))


def pick_apk_gui():
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QPalette, QColor

    BG = "#03090f"
    BG2 = "#111416"
    BG3 = "#242731"
    ACCENT = "#ff4343"
    TEXT = "#ffffff"
    TEXT2 = "#a0a0a0"
    BORDER = "#2a2d35"

    selected = [""]

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        font = QFont("Segoe UI", 10)
        app.setFont(font)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(BG))
        palette.setColor(QPalette.WindowText, QColor(TEXT))
        palette.setColor(QPalette.Base, QColor(BG2))
        palette.setColor(QPalette.Text, QColor(TEXT))
        palette.setColor(QPalette.Button, QColor(BG3))
        palette.setColor(QPalette.ButtonText, QColor(TEXT))
        palette.setColor(QPalette.Highlight, QColor(ACCENT))
        app.setPalette(palette)

    window = QWidget()
    window.setWindowTitle("APK Analyzer - Seleccionar archivo")
    window.setFixedSize(500, 200)
    window.setStyleSheet(f"""
        QWidget {{
            background-color: {BG};
            color: {TEXT};
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(12)

    title = QLabel("Selecciona un archivo APK")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {ACCENT};")
    layout.addWidget(title)

    path_row = QHBoxLayout()
    path_input = QLineEdit()
    path_input.setReadOnly(True)
    path_input.setPlaceholderText("Ningun archivo seleccionado...")
    path_input.setStyleSheet(f"""
        QLineEdit {{
            background: {BG3};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
            color: {TEXT};
        }}
    """)
    path_row.addWidget(path_input)

    browse_btn = QPushButton("Examinar")
    browse_btn.setFixedWidth(90)
    browse_btn.setStyleSheet(f"""
        QPushButton {{
            background: {BG3};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
        }}
        QPushButton:hover {{
            border-color: {ACCENT};
        }}
    """)
    path_row.addWidget(browse_btn)
    layout.addLayout(path_row)

    btn_row = QHBoxLayout()
    btn_row.addStretch()

    analyze_btn = QPushButton("Analizar APK")
    analyze_btn.setFixedWidth(200)
    analyze_btn.setEnabled(False)
    analyze_btn.setStyleSheet(f"""
        QPushButton {{
            background: {ACCENT};
            color: {TEXT};
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background: #e63c3c;
        }}
        QPushButton:disabled {{
            background: {BG3};
            color: {TEXT2};
        }}
    """)
    btn_row.addWidget(analyze_btn)
    btn_row.addStretch()
    layout.addLayout(btn_row)

    window.setLayout(layout)

    def on_browse():
        path, _ = QFileDialog.getOpenFileName(window, "Seleccionar APK", "", "APK files (*.apk);;All files (*)")
        if path:
            path_input.setText(path)
            analyze_btn.setEnabled(True)

    def on_analyze():
        selected[0] = path_input.text()
        window.close()

    browse_btn.clicked.connect(on_browse)
    analyze_btn.clicked.connect(on_analyze)

    window.show()
    app.exec()

    return selected[0]


def analyze_apk(apk_path):
    from androguard.misc import AnalyzeAPK

    print(f"\n  {C}[*]{R} Analizando APK...\n")

    a, d, dx = AnalyzeAPK(apk_path)

    permissions = a.get_permissions()
    pkg = a.get_package()
    app_name = a.get_app_name()
    version = a.get_androidversion_name()

    clear_screen()
    print_banner()

    print(f"  {M}\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500{R}")
    print(f"  {M}\u2502{R}  App:      {C}{app_name}{R}")
    print(f"  {M}\u2502{R}  Paquete:  {app_name} {C}({pkg}){R}")
    print(f"  {M}\u2502{R}  Version:  {version}")
    print(f"  {M}\u2502{R}  Permisos: {len(permissions)} declarados")
    print(f"  {M}\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500{R}")
    print()

    if not permissions:
        print(f"  {Y}[!]{R} No se declararon permisos en el manifest.\n")
        return

    short_ok = permissions

    dangerous_count = 0
    normal_count = 0
    signature_count = 0
    unknown_count = 0

    for perm in permissions:
        sev, dot = classify_permission(perm)
        pname = perm.split(".")[-1] if "." in perm else perm
        print(f"    {dot}  {pname}")
        if sev == "dangerous":
            dangerous_count += 1
        elif sev == "normal":
            normal_count += 1
        elif sev == "signature":
            signature_count += 1
        else:
            unknown_count += 1

    print()
    print(f"  {M}\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500{R}")
    print(f"  {M}\u2502{R}  Resumen de clasificacion")
    print(f"  {M}\u2502{R}")
    print(f"  {M}\u2502{R}    {RED_DOT}  Peligrosos:      {dangerous_count}")
    print(f"  {M}\u2502{R}    {YEL_DOT}  Normales:       {normal_count}")
    print(f"  {M}\u2502{R}    {BLU_DOT}  Firma:           {signature_count}")
    print(f"  {M}\u2502{R}    {GRY_DOT}  Desconocidos:   {unknown_count}")
    print(f"  {M}\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500{R}")


def main():
    while True:
        clear_screen()
        print_banner()
        wait_for_enter()

        apk_path = pick_apk_gui()
        if not apk_path or not os.path.isfile(apk_path):
            clear_screen()
            print_banner()
            print(f"\n  {Y}[!]{R} No se selecciono ningun archivo valido.\n")
            input("  Presiona Enter para continuar...")
            continue

        try:
            analyze_apk(apk_path)
        except Exception as e:
            clear_screen()
            print_banner()
            print(f"\n  {Y}[!]{R} Error al analizar APK: {e}\n")

        print()
        again = input("  \u00bfAnalizar otro APK? (s/n): ").strip().lower()
        if again != "s":
            print("\n  \u00a1Hasta luego!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Cancelado por el usuario. \u00a1Hasta luego!")
        sys.exit(0)
