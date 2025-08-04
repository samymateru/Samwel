from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# You can tune these parameters as needed
password_hasher = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=102400, # RAM usage in KiB (e.g., 100MB)
    parallelism=8,      # Threads
    hash_len=32,        # Length of the hash
    salt_len=16         # Salt length
)

def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using Argon2.
    """
    return password_hasher.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """
    Verifies a plain-text password against its hashed version.
    Returns True if matched, False otherwise.
    """
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


