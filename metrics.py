import time

POWER = 5  # watts

def measure(func, algo, operation, data, node, data_type="TEXT"):
    start = time.perf_counter()
    result = func(data)
    elapsed = time.perf_counter() - start

    metric = {
        "node": node,
        "algorithm": algo,
        "operation": operation,
        "data_type": data_type,     # ✅ NEW (internal only)
        "message_size": len(data),
        "time_ms": elapsed * 1000,
        "energy_joule": elapsed * POWER
    }

    return result, metric

