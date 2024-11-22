# Buggy Password Validator
# Help! Write UTs to fix me!

def validate_password(password):
    """
    Validates whether a password is strong based on the following criteria:
    1. At least 8 characters long.
    2. Contains at least one uppercase letter.
    3. Contains at least one lowercase letter.
    4. Contains at least one digit.
    5. Contains at least one special character (!@#$%^&*).
    Returns:
        True if the password meets all criteria, otherwise False.
    """
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*" for char in password):
        return False
    return True