import hashlib
import os
import time
from pathlib import Path
from types import TracebackType
from typing import Optional, Type


class CheckoutLockTimeout(Exception):
    pass


class _WouldBlock(Exception):
    pass


try:
    import fcntl

    def _lock_fd(fd: int) -> None:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, IOError):
            raise _WouldBlock()

    def _unlock_fd(fd: int) -> None:
        fcntl.flock(fd, fcntl.LOCK_UN)

except ImportError:
    import msvcrt

    def _lock_fd(fd: int) -> None:
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        except (OSError, IOError):
            raise _WouldBlock()

    def _unlock_fd(fd: int) -> None:
        try:
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        except (OSError, IOError):
            pass


class CheckoutLock:
    def __init__(self, profile_key: str, mode: str, timeout: float = 120.0, poll_interval: float = 0.1) -> None:
        self.timeout: float = timeout
        self.poll_interval: float = poll_interval
        self._fd: Optional[int] = None

        home = os.getenv('PYBRITIVE_HOME_DIR', str(Path.home()))
        lock_dir = Path(home) / '.britive' / 'locks'
        lock_dir.mkdir(parents=True, exist_ok=True)

        lock_name = hashlib.sha256(f'{mode}:{profile_key}'.lower().encode('utf-8')).hexdigest()[:16]
        self.lock_path: str = str(lock_dir / f'{lock_name}.lock')

    def acquire(self) -> None:
        self._fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                _lock_fd(self._fd)
                return
            except _WouldBlock:
                if time.monotonic() >= deadline:
                    os.close(self._fd)
                    self._fd = None
                    raise CheckoutLockTimeout(
                        f'Timed out after {self.timeout}s waiting for checkout lock'
                    )
                time.sleep(self.poll_interval)

    def release(self) -> None:
        if self._fd is not None:
            try:
                _unlock_fd(self._fd)
            finally:
                os.close(self._fd)
                self._fd = None

    def __enter__(self) -> 'CheckoutLock':
        self.acquire()
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> bool:
        self.release()
        return False
