import random
from typing import List
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from superagi.lib.logger import logger


searx_hosts = ["https://search.ononoki.org", "https://searx.be", "https://search.us.projectsegfau.lt"]

class SearchResult(BaseModel):
    """
    Represents a single search result from Searx

    Attributes:
        id : The ID of the search result.
        title : The title of the search result.
        link : The link of the search result.
        description : The description of the search result.
        sources : The sources of the search result.
    """
    id: int
    title: str
    link: str
    description: str
    sources: List[str]

    def __str__(self):
        return f"""{self.id}. {self.title} - {self.link}
{self.description}"""

def search(query):
    """
    Gets the raw HTML of a searx search result page

    Args:
        query : The query to search for.
    """
    # Try multiple hosts with better error handling
    for attempt in range(len(searx_hosts)):
        try:
            searx_url = searx_hosts[attempt]
            logger.info(f"Trying Searx host: {searx_url}")

            res = httpx.get(
                searx_url + "/search",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/114.0"},
                timeout=10.0
            )

            if res.status_code == 200:
                logger.info(f"Successfully got results from {searx_url}")
                return res.text
            elif res.status_code == 429:
                logger.warning(f"Rate limited by {searx_url}, trying next host...")
                continue
            else:
                logger.warning(f"Searx host {searx_url} returned {res.status_code}, trying next host...")
                continue

        except Exception as e:
            logger.warning(f"Error with Searx host {searx_url}: {str(e)}")
            continue

    # If all hosts fail, return a helpful error message instead of raising exception
    logger.error("All Searx hosts failed or are rate-limited")
    raise Exception("Search temporarily unavailable. All Searx hosts are rate-limited or unreachable. Please try again later or use a different search method.")

def clean_whitespace(s: str):
    """
    Cleans up whitespace in a string

    Args:
        s : The string to clean up.

    Returns:
        The cleaned up string.
    """
    return " ".join(s.split())


def scrape_results(html):
    """
    Converts raw HTML into a list of SearchResult objects

    Args:
        html : The raw HTML to convert.

    Returns:
        A list of SearchResult objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    result_divs = soup.find_all(attrs={"class": "result"})

    result_list = []
    n = 1
    for result_div in result_divs:
        if result_div is None:
            continue
        # Needed to work on multiple versions of Searx
        header = result_div.find(["h4", "h3"])
        if header is None:
            continue
        link = header.find("a")["href"]
        title = header.text.strip()

        description = clean_whitespace(result_div.find("p").text)

        # Needed to work on multiple versions of Searx
        sources_container = result_div.find(
            attrs={"class": "pull-right"}
        ) or result_div.find(attrs={"class": "engines"})
        source_spans = sources_container.find_all("span")
        sources = []
        for s in source_spans:
            sources.append(s.text.strip())

        result = SearchResult(
            id=n, title=title, link=link, description=description, sources=sources
        )
        result_list.append(result)
        n += 1

    return result_list


def search_results(query):
    '''Returns a text summary of the search results via the SearchResult.__str__ method'''
    return "\n\n".join(list(map(lambda x: str(x), scrape_results(search(query)))))
