import psutil

def resource_snapshot() -> dict:
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "available_memory_mb": round(psutil.virtual_memory().available / 1024 / 1024, 2),
    }
