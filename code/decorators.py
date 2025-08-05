import sys
import os
import contextlib

@contextlib.contextmanager
def suppress_stderr():
    """Temporarily silences stderr output."""
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr
