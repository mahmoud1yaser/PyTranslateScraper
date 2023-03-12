# PyTranslateScraper: Automated Web Scraping and Translation with Python

## Overview

This is a script that extracts HTML content from a webpage and its sub-pages (single depth layer), translates the content to a specified language, and saves the translated content to local HTML files. The script uses the Selenium WebDriver, Beautiful Soup, tqdm, and googletrans Python libraries.

## Files

    - utils.py: a Python module containing utility functions used in the script.
    - main.py: contains the body to run the script.

## Functions

    - set_up_driver(src: str) -> webdriver.Chrome: sets up a Chrome WebDriver instance and loads the specified URL.
    
    - get_soup(driver: webdriver.Chrome) -> BeautifulSoup: creates a BeautifulSoup object from the page source of the WebDriver instance.
    
    - extract_js_files(soup: BeautifulSoup) -> list: extracts the src attribute from all script tags in the HTML and returns them as a list.
    
    - include_js_files(soup: BeautifulSoup, js_files: list) -> None: creates a new script tag with the src attribute for each JS file in the list and appends it to the head tag of the HTML.
    
    - translate_html_file(soup, translated_lang): loops through all tags in the HTML and translates any text content in the specified language.
    
    - save_html_content(soup: BeautifulSoup, dst: str) -> None: replaces any / characters in the destination filename with underscores, converts the BeautifulSoup object to an HTML string, and writes it to a file.
    
    - close_driver(driver: webdriver.Chrome) -> None: quits the WebDriver instance to close the Chrome window and free up resources.
    
    - scrap_translate_webpage(src:str, dst:str, translated_lang:str) -> None: scrapes a webpage, translates its HTML content to the specified language, and saves the translated content to a local HTML file.
    
    - extract_href_links(soup: BeautifulSoup, website_url) -> list: extracts all href links from the page, removes any links containing "https", "http", "mailto", or "/", and returns the remaining links as a list.
    
    - preprocess_anchor_src(src: str, dst: str, website_url:str) -> None: opens the source HTML file, updates all anchor links in the soup to point to a file with a new name (replacing "/" with "_"), saves the updated HTML content to a file with the specified destination, and deletes the source file.
    
    - perform_one_layer_depth_and_get_links(website_url, final_page, translated_lang): extracts the main webpage, translates its content to the specified language, extracts all href links from the page, and preprocesses the anchor links to point to local HTML files.

## Dependencies
- Selenium
  - WebDriver
- Beautiful Soup
- tqdm
- googletrans

Note: check that you have installed the Chrome WebDriver on your system.

## Usage

To use the script, run the perform_one_layer_depth_and_get_links function in `main.py` with the following arguments:

    - website_url (str): the URL of the webpage to scrape.
    - final_page (str): the name of the final processed HTML file.
    - translated_lang (str): the language to translate the HTML content to.

The function will: 
- extract the main webpage.
- translate its content to the specified language.
- extract all href links from the page, preprocess the anchor links to point to local HTML files, and save the updated HTML content to a file with the specified name.
  - to be able to navigate through the pages without backend server.
- extract the processed HTML file and any sub-pages will be saved to the same directory as the script.

## Run
    - pip install <Required Dependecies>
    - python main.py


## Future Work
- Develop a script that is capable of functioning across multiple depth layers (General).
    - This task necessitates significant computational and network resources.
- Revise the script to adhere to the Object-Oriented Programming (OOP) paradigm.
- Implement the script as a Graphical User Interface (GUI) Toolbox for production use.


## Deployed Demo
  - Notes:
    - The website demo comprises five HTML files that can function independently without a backend server, namely `index.html`, `_about_careers.html`, `_contact.html`, `_help.html`, and `_about.html`.
    - The script is capable of scraping a single layer depth. When applied to the index HTML file, it can extract more than 369 external links (HTML files). However, scraping all the links at this depth would lead to the generation of 370 HTML files, which can take several hours to load.
    - Due to limitations in computational and network resources, the script was modified to scrap only five HTML files. Each of these HTML pages takes approximately 3.2 minutes to load.
  - [Website Demo]()
    - navigate through the right-bottom footer links in `index.html`.