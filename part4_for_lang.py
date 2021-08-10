from libraries import *
from part1_URL import *
from part2_find_and_save import *
from part3_check_if import *

#####################################   PART 4    #####################################

# working for languages in order
def for_languages(language_list):
    for n in range(len(all_languages)):
        name = all_languages[n]    
        for page_language in range(len(language_list)):
            r = requests.get(language_list[page_language], headers=header)
            list_titles, list_samples = find_and_save_data(language_list[page_language], f'metadata_{name}{page_language}.json')
            new_path = f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}"
            sample_path = f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/sample_{name}/"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            os.makedirs(sample_path)
        else:
            pass
        for title in range(len(list_titles)):
            try:
                url = list_samples[title]
                r = requests.get(url, allow_redirects=True)
                title_sample = list_titles[title]
                open(f'{title_sample}.mp3', 'wb').write(r.content)
                #changing the directory
                Path(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/{title_sample}.mp3").rename(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/sample_{name}/{title_sample}.mp3")
            except Exception as e:
                print(f"Error with downloading sample. Problem: {e}")
                continue
            Path(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/metadata_{name}{page_language}.json").rename(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/metadata_{name}{page_language}.json")
    if os.path.isfile(f'metadata_{name}0.json'):
        os.remove(f'metadata_{name}0.json')





# working for specific language
def for_specific_language(language_list, n):
    name = all_languages[n]    
    for page_language in range(len(language_list)):
        r = requests.get(language_list[page_language], headers=header)
        list_titles, list_samples = find_and_save_data(language_list[page_language], f'metadata_{name}{page_language}.json')
        new_path = f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}"
        sample_path = f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/sample_{name}/"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            os.makedirs(sample_path)
        else:
            pass
        for title in range(len(list_titles)):
            try:
                url = list_samples[title]
                r = requests.get(url, allow_redirects=True)
                title_sample = list_titles[title]
                open(f'{title_sample}.mp3', 'wb').write(r.content)
                #changing the directory
                Path(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/{title_sample}.mp3").rename(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/sample_{name}/{title_sample}.mp3")
            except Exception as e:
                print(f"Error with downloading sample. Problem: {e}")
                continue
        Path(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/metadata_{name}{page_language}.json").rename(f"C:/Users/alase/OneDrive/Pulpit/Praktyki/audible_scraper/metadata_{name}/metadata_{name}{page_language}.json")
    if os.path.isfile(f'metadata_{name}0.json'):
        os.remove(f'metadata_{name}0.json')
# downloading sample



