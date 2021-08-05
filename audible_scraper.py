from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import json
from requests.models import parse_header_links
import time


#####################################   PART 1    #####################################
#This program downloads sample from audible.com in 12 different languages for all sorting categories

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
#different codes for the same language:
#each list contains five codes for five sorting categories: relevance, newest-arrivals, best-selling, title, running time, average customer review
#WARNING! RELEVANCE HAVE DIFFERENT URL FROM REST
english = ['0H3EQZDPWN4Q8R41J60E', 'M7FMTES4QJ7QY8EW52V4', '6Y9T71Z08PJD05CH7G01', 'NVQKQYD4D68CA430NW8W', '2EPSV8SWE9T22BQE08JN', '5DHR0V8RWK87D2GJXHPB']               # english
spanish = ['JWSC8D69PJC4N0NSC98X', 'R2R3CBJC89H8MHYQKHH2', 'G27XRKVVQPJ9M6H6J63Q', '8HBZDAQ8RV3TPW4BR5SG', 'PW0KDTJCKJVGKAAJQ76R', 'BZMZA8Z0DS98GQFX7GYJ']               # spanish           
german = ['6P5PGXQJ9J3EAVRNG5DB', 'BKHKRPQH937CW74RKTXE', '62FTXJPTBMJPENA6EMPG', 'AVY6ZM4HFWKCQDWWXKB4', '7YASYWEXM3B0BNMFV9YZ', 'W7VVF9TG2YA3M97BWQ9H']                # german                  
french = ['BBMK2J1EZW1YQBK8ER1C', 'W33BMEXSE7E9VZSHPR30', 'QVKHGYGB59S278P1MF5T', 'XCGXVJSKWPHT255TWZ6D', 'GTJQNNXH8FHN9K735BA5', '1TZPMD5KK9046WDHXNR9']                # french                   
italian = ['JBAG8N8N8G07R9P27M3F', 'QXD4964H1AHR3GATHVQB', 'C7J2THTZEXVE6QJZ9HV8', 'ZXD60R2YH15XWFRDFWH1', '2G7D07NERD17J5RVNN5T', '3FAC869K8883W7B9ZNKB']               # italian                 
portuguese = ['AN3N03RHKPJS2KM19T0N', 'HEF1WJVNMTKWJPD1M3CH', 'F4SY7SR79N0YRSJ4Q36A', 'FQ6V65JSGQ7CBQW7G33R', '7BFZHFG0BD2XFQTJ1M39', 'XM72MQ1KWYNVPBNK9YB8']            # portuguese      
japanese = ['1QH6NPF7RSS629BDJ9RW', 'R6XW7JVPZ6G4EZW5T0XT', '87BJWZE7ETFEDTJ9F3YQ', 'EF8GSMZB03GWZ7FX4KVG', 'S97F2RZY9P25BKEQSWMR', 'XPS5AJK4RJMJBTNKAB6X']              # japanese      
danish = ['8AMKHEDRE8TTQ4BJN5JZ', 'KF58B840HH0T83AYJMMM', 'KBHSBME26H5YZT0V8FQW', '35WFARKWG649JG8751HF', 'M4TAV2X6ZFGYEPWXP2W8', 'ZFR83RC3MAQE0AX83NTC']                # danish       
afrikaans = ['QC0WTKBY4F1TJN8EN3KD', '6ESF4P6Y0YAXN0YXT8D1', '0GZ9PYYXH1CRW8K5KZ06', '589FR9S10F514K47HEQY', '66EWKZR2XBP3BSRVV6BP', 'YW64ZS1463W043RGY3WX']             # afrikaans       
mandarin_chinese = ['TZGTSKR5GFK43QERKCAQ', 'PTFTS4EX2A7Y54XA625F', 'B84C6ZWSFRHWXMAK5GES', 'JAVEE5BHZFT3F3GRKZNH', 'YST6RG9FP71FCGPMGMAT', '1T22DAW7EJZPKKVDR71N']      # mandarin_chinese       
russian = ['71E2JT7KGZBDZ3QRJXM6', 'DTZJNS21498RYQDXCMAF', 'X059HPWCBYZ125QGJPYR', 'M8HY87CX67CDR5R6PEX9', 'X02CWRD85E1XFKV74PSE', '1MJCANYPKAD2RMZ3NXMR']               # russian      
swedish = ['EQPN7ZC5MFFMYD73N9P8', '7MM98W9WA0BWYT09NMQ0', 'R0YX9C6EMDWEMNKZ56TG', 'ZJ1ZC2ZWAHGG8SC8K28N', '64YH326D6CN395B7HEHK', 'Y9KZF87W2E9N1DWXN03N']               # swedish

#for relevance -> AN3N03RHKPJS2KM19T0N
sorting=['AN3N03RHKPJS2KM19T0N', 'pubdate-desc-rank', 'popularity-rank','title-asc-rank', 'runtime-asc-rank','review-rank']
languages=[english, spanish, german, french, italian, portuguese, japanese, danish, afrikaans, mandarin_chinese, russian, swedish]
languages_code=['18685580011', '18685609011', '18685583011', '18685582011','18685590011','18685603011','18685591011','18685578011','18685571011','18685596011','18685606011','18685610011']

# HOW THE URL IS BUILD?

#FOR REST:
# https://www.audible.com/search?ref=a_search_c1_sort_          -> the same for every page
# 1                                                             -> index of category (is incrementing when choosing next category)
# &pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r=        -> the same for every page
# M7FMTES4QJ7QY8EW52V4                                          -> unique string for each category of sorting and each language (each page has different)
# &feature_six_browse-bin=                                      -> the same for every page
# 18685580011                                                   -> unique code for each language (but the same for every category)
# &sort=                                                        -> the same for every page
# pubdate-desc-rank                                             -> name of the category (same for each language)
# &pageSize=50&page=1                                           -> the same for every page


# goes through every possible combination of URL for all categories and all languages
# saves it to list and prints it
URL_english =[]
URL_spanish =[]
URL_german =[]
URL_french =[]
URL_italian =[]
URL_portuguese =[]
URL_japanese =[]
URL_danish =[]
URL_afrikaans =[]
URL_mandarin_chinese =[]
URL_russian =[]
URL_swedish =[]
#store_URL = [URL_english, URL_spanish, URL_german, URL_french, URL_italian, URL_portuguese, URL_japanese, URL_danish, URL_afrikaans, URL_mandarin_chinese, URL_russian, URL_swedish]
def storing_URL():
    # for language in range(len(languages)): #12 languages
    for var in range(6):
            # for language_code in range(len(languages_code)):
                # print(languages_code[f])
        for sort in range(len(sorting)): #6 categories of sorting
            # print(sorting[p])
            for page_number in range(1,25):
                try:
                    url_english = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[0][var]}&feature_six_browse-bin={languages_code[0]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_english.append(url_english)
                    url_spanish = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[1][var]}&feature_six_browse-bin={languages_code[1]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_spanish.append(url_spanish)
                    url_german = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[2][var]}&feature_six_browse-bin={languages_code[2]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_german.append(url_german)
                    url_french = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[3][var]}&feature_six_browse-bin={languages_code[3]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_french.append(url_french)
                    url_italian = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[4][var]}&feature_six_browse-bin={languages_code[4]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_italian.append(url_italian)
                    url_portuguese = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[5][var]}&feature_six_browse-bin={languages_code[5]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_portuguese.append(url_portuguese)
                    url_japanese = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[6][var]}&feature_six_browse-bin={languages_code[6]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_japanese.append(url_japanese)
                    url_danish = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[7][var]}&feature_six_browse-bin={languages_code[7]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_danish.append(url_danish)
                    url_afrikaans = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[8][var]}&feature_six_browse-bin={languages_code[8]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_afrikaans.append(url_afrikaans)
                    url_mandarin_chinese = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[9][var]}&feature_six_browse-bin={languages_code[9]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_mandarin_chinese.append(url_mandarin_chinese)
                    url_russian = f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[10][var]}&feature_six_browse-bin={languages_code[10]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_russian.append(url_russian)
                    url_swedish= f'https://www.audible.com/search?ref=a_search_c1_sort_{var}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[11][var]}&feature_six_browse-bin={languages_code[11]}&sort={sorting[sort]}&pageSize=50&page={page_number}'
                    URL_swedish.append(url_swedish)
                except Exception as e:
                    print(f"Exception: {e}, variable: {var}, sorting: {sort}")
                    continue
    # for url in range(len(store_URL)):
    #     print(store_URL[url])




#####################################   PART 2  #####################################
#This program finds data from html about audiobooks and saves it to .json file
# also finds links to sample and downloads it if needed

#working
def find_and_save_data(page, json_file_path):
    #providing a user-agent header
    
    html_text1 = requests.get(page).text
    s = BeautifulSoup(html_text1, 'html.parser')
    audiobooks1 = s.find('div', class_ = 'adbl-impression-container')
    titles1 = audiobooks1.findAll('li', class_ = 'bc-list-item productListItem') 
    authors = audiobooks1.findAll('li', class_ = 'bc-list-item authorLabel')
    narrators = audiobooks1.findAll('li', class_ = 'bc-list-item narratorLabel')
    series = audiobooks1.findAll('li', class_ = 'bc-list-item seriesLabel')
    lengths = audiobooks1.findAll('li', class_ = 'bc-list-item runtimeLabel')
    release_dates = audiobooks1.findAll('li', class_ = 'bc-list-item releaseDateLabel')
    languages1 = audiobooks1.findAll('li', class_ = 'bc-list-item languageLabel')
    ratings = audiobooks1.findAll('li', class_ = 'bc-list-item ratingsLabel')
    #site is changing because there are many languages
    titles = s.find('div', class_ = 'adbl-impression-container')
    audiobooks = titles.findAll('li', class_ = """bc-list-item""") 
    samples = titles.findAll('button', class_ = 'bc-button-text')

    #downloading audio
    #this part is commented since I don't want to download all this samples of audio
    for sample in range(len(samples)):
        try:
            print(samples[sample]['data-mp3'])
            # urls = samples[sample]['data-mp3']
            # r = requests.get(urls, allow_redirects=True)
            # for title in range(len(titles1)):
            #     title_sample = titles1[q]['aria-label']
            #     open(f'{title_sample}.mp3', 'wb').write(r.content)
        except:
            continue
#working
    audio_books = []
    for title in range(len(titles1)):
        audiobook = {}
        audiobook['Title'] = titles1[title]['aria-label']
        try:
            audiobook['Link to sample']=samples[title-1]['data-mp3']
        except:
            audiobook['Link to sample']='None'
        try:
            audiobook['By']=authors[title].text.replace("\n", '').replace(' ', '').replace('By:','')
        except:
            audiobook['By']='None'
        try:
            audiobook['Narrated by']=narrators[title-1].text.replace("\n", '').replace(' ', '').replace('Narratedby:','')
        except:
            audiobook['Narrated by']='None'
        try:
            audiobook['Series']=series[title].text.replace("\n", '').replace(' ', '').replace('Series:','')
        except:
            audiobook['Series']='None'
        try:
            audiobook['Length']=lengths[title].text.replace("\n", '').replace(' ', '').replace('Length:','')
        except:
            audiobook['Length']='None'
        try:
            audiobook['Release date']=release_dates[title].text.replace("\n", '').replace(' ', '').replace('Releasedate:','')
        except:
            audiobook['Release date']='None'
        try:
            audiobook['Language']=languages1[title].text.replace("\n", '').replace(' ', '').replace('Language:','')
        except:
            audiobook['Language']='None'
        try:
            audiobook['Ratings']=ratings[title].text.replace("\n", '').replace(' ', '').replace(':',': ').replace('stars','')
        except:
            audiobook['Ratings']='None'
        audio_books.append(audiobook)

    #saving metadata to .json file
    try:
        with open(json_file_path, 'r',encoding='utf-8') as f:
            old_json = json.load(f)
    except Exception as e:
        print(e)
        old_json = []

    with open(json_file_path, 'w',encoding='utf-8') as f:
        json.dump(audio_books + old_json, f, ensure_ascii=False, indent=4)
    print('Saved to .json file')



#####################################   PART 3  #####################################
#This program checks if given file wasn't previously downloaded

def check_if_repeat(webpage, json_file):
    try:
        books = json.load(json_file) #opening file; if it doesn't exist, we create empty list for audiobooks
    except:
        books = []
    
    #creating list with titles
    books_titles = []
    for book in books:
        books_titles.append(book['Title'])

    #we are in 'for q in range(len(titles1))' 
    html_text1 = requests.get(webpage).text
    s = BeautifulSoup(html_text1, 'html.parser')
    audiobooks1 = s.find('div', class_ = 'adbl-impression-container')
    titles1 = audiobooks1.findAll('li', class_ = 'bc-list-item productListItem') 
    authors = audiobooks1.findAll('li', class_ = 'bc-list-item authorLabel')
    narrators = audiobooks1.findAll('li', class_ = 'bc-list-item narratorLabel')
    series = audiobooks1.findAll('li', class_ = 'bc-list-item seriesLabel')
    lengths = audiobooks1.findAll('li', class_ = 'bc-list-item runtimeLabel')
    release_dates = audiobooks1.findAll('li', class_ = 'bc-list-item releaseDateLabel')
    languages1 = audiobooks1.findAll('li', class_ = 'bc-list-item languageLabel')
    ratings = audiobooks1.findAll('li', class_ = 'bc-list-item ratingsLabel')
    samples = audiobooks1.findAll('button', class_ = 'bc-button-text')
    
    for title1 in range(len(titles1)):
        curr_title = titles1[title1]['aria-label']      # reading audiobook title as string
        if curr_title not in books_titles:              # if the movie isn't in the list we've created
            books_titles.append(curr_title)             # we add it to the list with already existing titles
            # now we add new audiobook
            audiobook = {}
            audiobook['Title'] = curr_title
            for title in range(len(samples)):
                try:
                    audiobook['Link to sample']=samples[title-1]['data-mp3']
                except:
                    audiobook['Link to sample']='None'
            audiobook['By']=authors[title1].text.replace("\n", '').replace(' ', '').replace('By:','')
            audiobook['Narrated by']=narrators[title1-1].text.replace("\n", '').replace(' ', '').replace('Narratedby:','')
            try:
                audiobook['Series']=series[title1].text.replace("\n", '').replace(' ', '').replace('Series:','')
            except:
                audiobook['Series']='None'
            audiobook['Length']=lengths[title1].text.replace("\n", '').replace(' ', '').replace('Length:','')
            audiobook['Release date']=release_dates[title1].text.replace("\n", '').replace(' ', '').replace('Releasedate:','')
            audiobook['Language']=languages1[title1].text.replace("\n", '').replace(' ', '').replace('Language:','')
            audiobook['Ratings']=ratings[title1].text.replace("\n", '').replace(' ', '').replace(':',': ').replace('stars','')
            books.append(audiobook)
            
        else:               #if the title exists in the list
            continue        #we skip loop iteration
        
    with open(json_file, 'w',encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)

    print('Saved to .json file')
    print('Checking is done')




#####################################   MAIN    #####################################
# it works for every site
if __name__=="__main__":
#working
    storing_URL()

    for page_english in range(len(URL_english)):
        r_english = requests.get(URL_english[page_english], headers=header)
        find_and_save_data(URL_english[page_english], 'metadata_english.json')
    
    for page_spanish in range(len(URL_spanish)):
        r_spanish = requests.get(URL_spanish[page_spanish], headers=header)
        find_and_save_data(URL_spanish[page_spanish], 'metadata_spanish.json')

    for page_german in range(len(URL_german)):
        r_german = requests.get(URL_german[page_german], headers=header)
        find_and_save_data(URL_german[page_german], 'metadata_german.json')

    for page_french in range(len(URL_french)):
        r_french = requests.get(URL_french[page_french], headers=header)
        find_and_save_data(URL_french[page_french], 'metadata_french.json')

    for page_italian in range(len(URL_italian)):
        r_italian = requests.get(URL_italian[page_italian], headers=header)
        find_and_save_data(URL_italian[page_italian], 'metadata_italian.json')

    for page_portuguese in range(len(URL_portuguese)):
        r_portuguese = requests.get(URL_portuguese[page_portuguese], headers=header)
        find_and_save_data(URL_portuguese[page_portuguese], 'metadata_portuguese.json')

    for page_japanese in range(len(URL_japanese)):
        r_japanese = requests.get(URL_japanese[page_japanese], headers=header)
        find_and_save_data(URL_japanese[page_japanese], 'metadata_japanese.json')

    for page_danish in range(len(URL_danish)):
        r_danish = requests.get(URL_danish[page_danish], headers=header)
        find_and_save_data(URL_danish[page_danish], 'metadata_danish.json')

    for page_afrikaans in range(len(URL_afrikaans)):
        r_afrikaans = requests.get(URL_afrikaans[page_afrikaans], headers=header)
        find_and_save_data(URL_afrikaans[page_afrikaans], 'metadata_afrikaans.json')

    for page_mandarin_chinese in range(len(URL_mandarin_chinese)):
        r_mandarin_chinese = requests.get(URL_mandarin_chinese[page_mandarin_chinese], headers=header)
        find_and_save_data(URL_mandarin_chinese[page_mandarin_chinese], 'metadata_mandarin_chinese.json')

    for page_russian in range(len(URL_russian)):
        r_russian = requests.get(URL_russian[page_russian], headers=header)
        find_and_save_data(URL_russian[page_russian], 'metadata_russian.json')

    for page_swedish in range(len(URL_swedish)):
        r_swedish = requests.get(URL_swedish[page_swedish], headers=header)
        find_and_save_data(URL_swedish[page_swedish], 'metadata_swedish.json')


    # find_and_save_data('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test.json')
    # storing_URL()
    # check_if_repeat('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test1.json')
   