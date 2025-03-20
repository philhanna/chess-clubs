import requests

def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage from a given URL.
    
    Args:
        url (str): The URL of the webpage to fetch.
    
    Returns:
        str: The HTML content of the requested webpage.
    
    Raises:
        requests.exceptions.RequestException: If the request encounters an error.
    """
    # Set a timeout to avoid indefinitely hanging requests
    response = requests.get(url, timeout=20)
    
    # Raise an error for HTTP responses with status codes 4xx or 5xx
    response.raise_for_status()
    
    return response.text

# Define the module exports
__all__ = [
    'get_page'
]
