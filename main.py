"""
Main module
"""
import argparse
import logging
import requests
import bs4


URL = "https://www.opcionempleo.cl"


parser = argparse.ArgumentParser(description=f"Scrap {URL}")
parser.add_argument(
    "-pc", "--preserve-commas",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Preserve commas in output file. Warning: This can cause problems in\
        the csv format."
)
args = parser.parse_args()


logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logging.getLogger().setLevel(logging.INFO)




class Scraper:
    def __init__(self, url=URL, queries_route="topqueries", replace_commas=True):
        """Initialize the Scraper class
        
        Arguments
        ---------
        url: str, optional
            The url to scrape. The default is "https://www.opcionempleo.cl".
        queries_route: str, optional
            The path to search within the url. The default is "topqueries".
        replace_commas: bool, optional
            If True, replace commas in query's names and results. The default
            is True.
        """
        self.url = url
        self.queries_route = queries_route
        self.queries_url = f"{self.url}/{self.queries_route}"
        self.replace_commas = replace_commas
        # Set with requests to the moment
        self.made_queries = set()
        self.total_results = 0
        self.total_queries_with_more_than_15_result = 0

    def get_queries(self, page=1):
        """Get the queries results from the url
        
        Arguments
        ---------
        page: int, optional
            The page to get the results from. The default is 1.
        """
        r = requests.get(f"{self.queries_url}/{page}")
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        queries = soup.find(class_="row links").find_all("a")
        queries = ((q.text.lower().strip(), q.get("href")) for q in queries)
        if self.replace_commas:
            queries = ((q[0].replace(',', ' '), q[1]) for q in queries)
        return queries

    def get_results(self, query, query_url):
        """Get the results from the query url
        
        Arguments
        ---------
        query: str
            The query name to get the results from.
        query_url: str
            The url to get the results from.
        """
        r = requests.get(query_url)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        articles = soup.find(class_="jobs")
        if not articles:
            return []
        articles = articles.find_all("article")
        if not self.replace_commas:
            results = [f"{query},{art.a.text.strip()}" for art in articles]
        else:
            titles  = (art.a.text.replace(',',' ') for art in articles)
            results = [f"{query},{title.strip()}" for title in titles]
        return results

    def write_results(self, results, filename="results.csv"):
        """Write the results to a file

        Arguments
        ---------
        results: list
            The results to write in format term,title.
        filename: str, optional
            The filename to append the results to. The default is "results.csv".
        """
        with open(filename, 'a') as f:
            for result in results:
                f.write(f"{result}\n")

    def _log_query(self, query, len_results):
        """Log the query status
        
        Arguments
        ---------
        query: str
            The query to log.
        len_results: int
            The number of results for the query.
        """
        query_info  = f"New query '{query}' with {len_results} results"
        total_info  = f"total: {len(self.made_queries):>5} queries, "
        total_info += f"{self.total_results:>6} results"
        # NOTE: This line is just for testing purposes
        total_info += f", {self.total_queries_with_more_than_15_result:>5} queries with more than 15 results"
        log = f"{query_info:<70} ({total_info})"
        logging.info(log)
    
    def run(self):
        page = 1
        logging.info("Press CTRL+C to stop")
        while True:
            logging.info("Looking page %i...", page)
            queries = self.get_queries(page)
            for query, path in queries:
                # Check if the query has been made
                if query not in self.made_queries:
                    # Get results
                    query_url = f"{self.url}{path}"
                    results = self.get_results(query, query_url)
                    # Write results
                    self.write_results(results)
                    self.made_queries.add(query)
                    self.total_results += len(results)
                    # NOTE: This is just for testing purposes
                    if len(results) > 15:
                        self.total_queries_with_more_than_15_result += 1
                    self._log_query(query, len(results))
            page += 1




if __name__ == "__main__":
    scraper = Scraper(replace_commas=(not args.preserve_commas))
    scraper.run()