import requests


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage from a given URL.
    """
    # Set a timeout to avoid hanging requests
    response = requests.get(url, timeout=20)
    # Raise an error for HTTP error responses (4xx, 5xx)
    response.raise_for_status()
    html = response.text
    return html

__all__ = [
    'get_page'
]