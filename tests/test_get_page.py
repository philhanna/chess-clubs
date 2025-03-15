import pytest
import requests
from unittest.mock import patch
from util import get_page

def test_get_page_happy_path():
    url = "https://example.com"
    expected_html = "<html><body><h1>Test Page</h1></body></html>"
    
    with patch("requests.get") as mock_get:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = expected_html.encode("utf-8")
        mock_get.return_value = mock_response
        
        result = get_page(url)
        assert result == expected_html

def test_get_page_http_error():
    url = "https://example.com"
    
    with patch("requests.get") as mock_get:
        mock_response = requests.Response()
        mock_response.status_code = 404
        mock_response._content = b"Not Found"
        mock_get.return_value = mock_response
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found for url")
        
        with pytest.raises(requests.exceptions.HTTPError):
            get_page(url)
            
def test_get_page_timeout():
    url = "https://example.com"
    
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout("The request timed out")
        
        with pytest.raises(requests.exceptions.Timeout):
            get_page(url)

def test_get_page_connection_error():
    url = "https://example.com"
    
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to establish a new connection")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            get_page(url)
