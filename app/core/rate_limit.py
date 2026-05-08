from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize the limiter
# Using get_remote_address as the default identifier (IP-based rate limiting)
limiter = Limiter(key_func=get_remote_address)
