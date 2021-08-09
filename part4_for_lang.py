from libraries import *
from part1_URL import *
from part2_find_and_save import *
from part3_check_if import *

# working
def for_languages(language_list):
    for n in range(len(all_languages)):
        name = all_languages[n]    
        for page_language in range(len(language_list)):
            r = requests.get(language_list[page_language], headers=header)
            find_and_save_data(language_list[page_language], f'metadata_{name}{page_language}.json')
            new_path = f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}"
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            Path(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/metadata_{name}{page_language}.json").rename(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/metadata_{name}{page_language}.json")
