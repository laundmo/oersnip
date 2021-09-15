import os

is_windows = False
if os.name == "nt":
    import win32api
    import win32con
    import win32gui
    import win32process

    win32gui.SystemParametersInfo(
        win32con.SPI_SETFOREGROUNDLOCKTIMEOUT,
        0,
        win32con.SPIF_SENDWININICHANGE | win32con.SPIF_UPDATEINIFILE,
    )
    is_windows = True


def force_focus_windows(win_id):
    """Unhides the windows window with the winID passed in"""
    if is_windows:
        fgwin = win32gui.GetForegroundWindow()
        fg = win32process.GetWindowThreadProcessId(fgwin)[0]
        current = win32api.GetCurrentThreadId()
        if current != fg:
            win32process.AttachThreadInput(fg, current, True)
            win32gui.SetForegroundWindow()
            win32process.AttachThreadInput(fg, win32api.GetCurrentThreadId(), False)
