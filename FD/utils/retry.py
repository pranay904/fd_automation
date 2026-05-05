import time
from FD.utils.logger import logger


def retry_on_failure(page, action, retries=2, reload_on_retry=True):
    """
    Retry an action on failure, with optional page reload between attempts.

    Args:
        page:            Playwright page object
        action:          Callable — the action to execute
        retries:         Total attempts (default 2)
        reload_on_retry: Whether to reload the page before retrying (default True)

    Returns:
        Result of action() if successful

    Raises:
        Last exception if all attempts fail
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            result = action()

            # Check for server-side error responses via JS
            status = page.evaluate("() => window.__lastResponseStatus || 200")
            if status in [400, 404, 500, 502, 503]:
                raise Exception(f"Server returned HTTP {status}")

            logger.info(f"[RETRY] Attempt {attempt} succeeded")
            return result

        except Exception as e:
            last_error = e
            logger.warning(f"[RETRY] Attempt {attempt}/{retries} failed: {e}")

            if attempt < retries:
                if reload_on_retry:
                    try:
                        logger.info("[RETRY] Reloading page before next attempt...")
                        page.reload(wait_until="domcontentloaded")
                        page.wait_for_timeout(1500)
                    except Exception as reload_err:
                        logger.warning(f"[RETRY] Reload failed: {reload_err}")
                else:
                    page.wait_for_timeout(1000)

    raise last_error


def retry_until_true(condition, timeout=10, error_msg="Condition not met"):
    """
    Poll a condition callable until it returns True or timeout is reached.

    Args:
        condition:  Callable returning bool
        timeout:    Max seconds to wait (default 10)
        error_msg:  Message for AssertionError on timeout

    Raises:
        AssertionError if condition never returns True within timeout
    """
    start = time.time()
    while time.time() - start < timeout:
        try:
            if condition():
                return True
        except Exception:
            pass
        time.sleep(0.5)
    raise AssertionError(error_msg)
