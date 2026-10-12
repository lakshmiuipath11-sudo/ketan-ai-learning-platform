"""TinyFish integration placeholder.

Before enabling: implement user authentication, rate limiting, outbound URL
allowlisting, and verify the current TinyFish API endpoint/payload in its docs.
Never expose the API key to browser JavaScript.
"""
import os

def run_tinyfish(url: str, goal: str):
    if not os.getenv('TINYFISH_API_KEY'):
        raise RuntimeError('TINYFISH_API_KEY is missing')
    raise NotImplementedError('Configure verified TinyFish endpoint and safeguards first')
