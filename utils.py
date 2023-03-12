import os
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
from googletrans import Translator


def set_up_driver(src: str) -> webdriver.Chrome:
    # Create ChromeOptions object and add headless mode argument
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Create Chrome WebDriver instance with specified options and load the URL
    driver = webdriver.Chrome(options=options)
    driver.get(src)

    return driver


def get_soup(driver: webdriver.Chrome) -> BeautifulSoup:
    # Create BeautifulSoup object from the page source of the WebDriver instance
    soup = BeautifulSoup(driver.page_source, "html.parser")

    return soup


def extract_js_files(soup: BeautifulSoup) -> list:
    # Extract the 'src' attribute from all 'script' tags in the HTML and return as a list
    js_files = [js.get("src") for js in soup.find_all("script") if js.get("src")]

    return js_files


def include_js_files(soup: BeautifulSoup, js_files: list) -> None:
    # Create a new 'script' tag with the 'src' attribute for each JS file in the list
    # and append it to the 'head' tag of the HTML
    for js in js_files:
        script_tag = soup.new_tag("script", src=js)
        soup.head.append(script_tag)


def translate_html_file(soup, translated_lang):
    # Create Translator object from the 'googletrans' library
    translator = Translator()

    # Loop through all tags in the HTML and translate any text content in the specified language
    for tag in soup.recursiveChildGenerator():
        if tag.name not in ['style', 'script'] and hasattr(tag, 'text') and tag.string:
            translated = translator.translate(text=tag.text, dest=translated_lang).text
            tag.string.replace_with(translated)

    return soup


def save_html_content(soup: BeautifulSoup, dst: str) -> None:
    # Replace any '/' characters in the destination filename with underscores
    dst = dst.replace('/', '_')

    # Convert the BeautifulSoup object to an HTML string and write it to a file
    html_string = str(soup)
    with open(f"{dst}.html", "w", encoding="utf-8") as file:
        file.write(html_string)


def close_driver(driver: webdriver.Chrome) -> None:
    # Quit the WebDriver instance to close the Chrome window and free up resources
    driver.quit()


def scrap_translate_webpage(src:str, dst:str, translated_lang:str) -> None:
    # Set up Chrome WebDriver instance and load the source URL
    driver = set_up_driver(src)

    # Create BeautifulSoup object from the WebDriver's page source
    soup = get_soup(driver)

    # Extract all JavaScript files in the page and add them to the soup
    js_files = extract_js_files(soup)
    include_js_files(soup, js_files)

    # Translate the HTML content using the specified language and update the soup
    soup_tarns = translate_html_file(soup, translated_lang)

    # Save the translated HTML content to a file with the specified destination
    save_html_content(soup_tarns, dst)

    # Close the Chrome WebDriver instance
    close_driver(driver)


def extract_href_links(soup: BeautifulSoup, website_url) -> list:
    # Extract all href links from the page, remove any links containing "https", "http", "mailto", or "/"
    href_links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
    href_links = [link.replace(website_url, "") for link in href_links]
    href_links = [elem for elem in href_links if elem != '/']
    href_links = [item for item in href_links if not any(substring in item for substring in ['https', 'http', 'mailto'])]

    return href_links


def preprocess_anchor_src(src: str, dst: str, website_url:str) -> None:
    # Open the source HTML file and create a BeautifulSoup object
    with open(f'{src}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Update all anchor links in the soup to point to a file with a new name, replacing "/" with "_"
    for anchor in soup.find_all('a'):
        href = anchor.get('href')
        href = href.replace(website_url, "")
        if href and not any(substring in href for substring in ['https', 'http', 'mailto']) and href != '/':
            href = href.replace('/', '_')
            href += '.html'
            anchor['href'] = href

    # Save the updated HTML content to a file with the specified destination and delete the source file
    updated_html_content = str(soup)
    with open(f'{dst}.html', 'w', encoding='utf-8') as file:
        file.write(updated_html_content)
    os.remove(f'{src}.html')


def perform_one_layer_depth_and_get_links(website_url, final_page, translated_lang):
    PROCESSED_PAGE = "test" # The processed page name

    # Extract the main webpage and translate it
    scrap_translate_webpage(website_url, PROCESSED_PAGE, translated_lang)

    # Extract all the href links for the main webpage
    with open(f'{PROCESSED_PAGE}.html', "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        href_links = extract_href_links(soup, website_url)

    # Scrape all external nodes
    for page in tqdm(href_links):
        src = website_url+page
        scrap_translate_webpage(src, page, translated_lang)

    # Adjust external nodes' href links relative to the main node
    preprocess_anchor_src(PROCESSED_PAGE, final_page, website_url)
