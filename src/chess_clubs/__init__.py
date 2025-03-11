# Chess clubs
import requests


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a webpage from a given URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the fetched webpage.

    Raises:
        requests.exceptions.RequestException: If the request encounters an HTTP error or timeout.
    """
    response = requests.get(
        url, timeout=20)  # Set a timeout to avoid hanging requests
    response.raise_for_status()  # Raise an error for HTTP error responses (4xx, 5xx)
    return response.text
