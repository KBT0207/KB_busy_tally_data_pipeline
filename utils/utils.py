import psutil


def is_process_running(process_name):
    for process in psutil.process_iter():
        if process.name().lower() == process_name.lower():
            return True
    return False

# Usage example:
