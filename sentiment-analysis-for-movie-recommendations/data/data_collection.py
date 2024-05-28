import csv
from bs4 import BeautifulSoup
from selenium_stealth import stealth
import undetected_chromedriver as uc
import urllib.error
import traceback

# Constants for IMDb URL and output CSV filename
IMDB_URL = "https://www.imdb.com/search/title/?genres=Musical&explore=genres&title_type=movie&ref_=ft_movie_14"
CSV_FILENAME = "./data_sets/output.csv"


class Data:
    def __init__(self):
        self.driver = None

    def initialize_driver(self):
        """
        Initializing Chrome WebDriver with specific options and stealth configurations.
        """
        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")

        # Initializing Chrome WebDriver
        self.driver = uc.Chrome(options=options)

        # Applying stealth configurations
        stealth(self.driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
                webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

    def scrape_imdb(self, url):
        """
        Implementing IMDb scraping logic.
        """
        try:
            self.url = url
            self.driver.set_page_load_timeout(60)
            self.driver.get(self.url)
            self.soup = BeautifulSoup(self.driver.page_source, "lxml")
            self.collected_data = []

            # Scraping data from movie links
            for link,i in enumerate(self.soup.select("a.ipc-title-link-wrapper"))[:30]:
                href_value = link["href"]
                self.driver.get(f"https://www.imdb.com{href_value}")
                self.another_soup = BeautifulSoup(
                    self.driver.page_source, "lxml")
                self.retrieved_data = {"Title": self.another_soup.find(
                    "h1", {'data-testid': 'hero__pageTitle'}).find('span', {'class': 'hero__primary-text'}).text.strip()}

                user_reviews_link_tag = self.another_soup.find(
                    'a', string="User reviews")
                if user_reviews_link_tag:
                    user_reviews_link = user_reviews_link_tag['href']
                    self.driver.get(f"https://www.imdb.com{user_reviews_link}")
                    self.reviews_soup = BeautifulSoup(
                        self.driver.page_source, 'lxml')
                    reviews_set = self.reviews_soup.select('a.title')
                    reviews = [review.text.strip()
                               for review in reviews_set[:300]]
                    self.retrieved_data['User Reviews'] = reviews
                else:
                    reviews = [""]
                    
                if i == 29:
                    break

                self.collected_data.append(self.retrieved_data)

            return self.collected_data

        except urllib.error.HTTPError as http_error:
            print(f"HTTPError: {http_error}")
            print(f"URL causing the error: {self.url}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            if self.driver:
                self.driver.quit()

    def to_csv(self, data_structure, filename):
        """
        Converting the gathered data to CSV.
        """
        if not data_structure:
            return

        # Extracting field names from the first dictionary in data_structure
        csv_column = data_structure[0].keys()

        # Adding 'User Reviews' to field names if not present
        if 'User Reviews' not in csv_column:
            csv_column = list(csv_column) + ['User Reviews']

        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=csv_column)
            csv_writer.writeheader()
            csv_writer.writerows(data_structure)

        return f"CSV file '{filename}' created successfully."


def execute_data_gathering():
    """
    Orchestrating the IMDb data gathering and CSV conversion process.
    """
    scraper_object = Data()
    try:
        # Initializing Chrome WebDriver
        scraper_object.initialize_driver()

        # Scraping IMDb data
        scraped_data = scraper_object.scrape_imdb(IMDB_URL)

        if scraped_data:
            # Storing as CSV
            result_message = scraper_object.to_csv(scraped_data, CSV_FILENAME)
            print(result_message)
        else:
            print("No data scraped.")

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred in the main function: {e}")
    finally:
        # Ensuring that the WebDriver is closed
        if scraper_object.driver:
            scraper_object.driver.quit()


if __name__ == "__main__":
    # Executing the data gathering process
    execute_data_gathering()
