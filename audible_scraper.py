from libraries import *
from part1_URL import *
from part2_find_and_save import *
from part3_check_if import *
from part4_for_lang import *
            
#####################################   MAIN    #####################################
# it works for every site
if __name__=="__main__":
#working
    storing_URL()
    for URL_language in store_URL:
        spanish_url = store_URL[1]
        for_languages(spanish_url)
    
    # find_and_save_data('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test.json')
    # storing_URL()
    # check_if_repeat('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test1.json')
   