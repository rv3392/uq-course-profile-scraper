import urllib.request
import bs4

def get_page_soup(
        page_url: str, 
        request_headers: dict = {'User-Agent':'Course Profile API'}, 
        parser: str = "lxml") -> bs4.BeautifulSoup:
    """Gets the bs4 parsed "soup" ready to be searched.
    
    Parameters:
        page_url (str): The full URL of the page to be loaded
        request_headers (dict): A dict for urllib.request.Request to use
                as headers for the request. By default the user-agent
                is used to represent this API.
        parser (str): The parser is used to parse the webpage into its tags.
                LXML is widely recognised as the highest quality python
                parser.
    
    Returns:
        bs4.BeautifulSoup: An instance of a bs4 object with the loaded 
                page_url. The page is loaded with the provided
                request_headers and parsed by the provided parser.
    """
    page_request = urllib.request.Request(page_url, 
                headers=request_headers)
    page_html = urllib.request.urlopen(page_request).read()
    page = bs4.BeautifulSoup(page_html, features=parser)

    return page