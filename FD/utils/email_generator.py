import time


def generate_email():
    """
        Generates a unique email using timestamp.
        Example:
        pranayfriendlydiamonds1700000000@gmail.com
        """
    timestamp = int(time.time())
    return f"pranayfriendlydiamonds{timestamp}@gmail.com"
