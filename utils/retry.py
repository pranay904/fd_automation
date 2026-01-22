import time

def retry_until_true(condition, timeout=10, error_msg="Condition not met"):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except:
            pass
        time.sleep(0.5)
    raise AssertionError(error_msg)
