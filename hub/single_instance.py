"""실행 파일 경로·버전에 관계없이 Windows 세션당 GUI 하나만 실행한다."""
from __future__ import annotations

import atexit
import ctypes
from ctypes import wintypes
import os


def acquire(app_id: str) -> bool:
    """프로세스 종료까지 뮤텍스를 유지한다. 비정상 종료 때도 Windows가 정리한다."""
    if os.name != "nt":
        return True
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    handle = kernel32.CreateMutexW(None, False, "Local\\SelimTools." + app_id)
    error = ctypes.get_last_error()
    if not handle:
        raise ctypes.WinError(error)
    if error == 183:  # ERROR_ALREADY_EXISTS
        kernel32.CloseHandle(handle)
        return False
    atexit.register(kernel32.CloseHandle, handle)
    return True
