from utils import *

if __name__ == "__main__":
    home_page_url = "https://www.classcentral.com"
    adjusted_page = "index"  # The adjusted page name
    TRANSLATED_LANG = 'hi'  # The language to which the webpage will be translated

    perform_one_layer_depth_and_get_links(home_page_url, adjusted_page, TRANSLATED_LANG)