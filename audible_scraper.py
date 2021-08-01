from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import pafy
import json
from requests.models import parse_header_links
import sys
import time

#####################################   PART 1    #####################################
#This program downloads sample from audible.com in 12 different languages for all sorting categories
                  
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


sorting=['relevance', 'pubdate-desc-rank', 'popularity-rank','title-asc-rank', 'runtime-asc-rank','review-rank']
languages=[english, spanish, german, french, italian, portuguese, japanese, danish, afrikaans, mandarin_chinese, russian, swedish]
languages_code=['18685580011', '18685609011', '18685583011', '18685582011','18685590011','18685603011','18685591011','18685578011','18685571011','18685596011','18685606011','18685610011']

# HOW THE URL IS BUILD?

# FOR REVELANCE:
# https://www.audible.com/search?ref=a_search_l1_feature_six_browse-bin_0&pf_rd_p=daf0f1c8-2865-4989-87fb-15115ba5a6d2&pf_rd_r= -> the same for every page
# 0H3EQZDPWN4Q8R41J60E          -> unique string for each category of sorting and each language (each page has different)
# &feature_six_browse-bin=      -> the same for every page
# 18685580011                   -> unique code for each language (but the same for every category)
# &pageSize=50                  -> the same for every page

#FOR REST:
# https://www.audible.com/search?ref=a_search_c1_sort_          -> the same for every page
# 1                                                             -> index of category (is incrementing when choosing next category)
# &pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r=        -> the same for every page
# M7FMTES4QJ7QY8EW52V4                                          -> unique string for each category of sorting and each language (each page has different)
# &feature_six_browse-bin=                                      -> the same for every page
# 18685580011                                                   -> unique code for each language (but the same for every category)
# &sort=                                                        -> the same for every page
# pubdate-desc-rank                                             -> name of the category (same for each language)
# &pageSize=50                                                  -> the same for every page


#should be working
store_URL =[]
store_URL_relevance =[]
for x in range(len(languages)):
    try:
        for p in range(len(sorting)):
            sorting[p]=languages[x][p]
            for t in range(0, 6):
                for r in range(1,6): #we must omit first string since its revelance string
                    relevance_url = f'https://www.audible.com/search?ref=a_search_l1_feature_six_browse-bin_0&pf_rd_p=daf0f1c8-2865-4989-87fb-15115ba5a6d2&pf_rd_r={languages[x][0]}&feature_six_browse-bin={languages_code[x]}&pageSize=50'
                    url = f'https://www.audible.com/search?ref=a_search_c1_sort_{t}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[x][r]}&feature_six_browse-bin={languages_code[x]}&sort={sorting[p]}&pageSize=50'
                    time.sleep(0.2)
                    store_URL.append(url)
                    store_URL_relevance.append(relevance_url)
    except:
        print("Sorry, there is something wrong. Check the parameters of languages in list.")
        continue



#####################################   PART 2  #####################################
#This program finds data from html about audiobooks and saves it to .json file
# also finds links to sample and downloads it if needed

#working
def find_and_save_data(page, json_file_path):
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
    for n in range(len(samples)):
        try:
            print(samples[n]['data-mp3'])
            # url = samples[n]['data-mp3']
            # url_sample = pafy.new(url)
            # audio_sample = url_sample.get_audio_sample()
            # audio_sample.download()
        except:
            continue
#working
    audio_books = []
    for q in range(len(titles1)):
        #print(titles1[q]['aria-label'])
        audiobook = {}
        audiobook['Title'] = titles1[q]['aria-label']
        audiobook['Link to sample']=samples[n]['data-mp3']
        #print(authors[q].text.replace("\n", '').replace(' ', ''))
        audiobook['By']=authors[q].text.replace("\n", '').replace(' ', '').replace('By:','')
        #print(narrators[q-1].text.replace("\n", '').replace(' ', ''))
        audiobook['Narrated by']=narrators[q-1].text.replace("\n", '').replace(' ', '').replace('Narratedby:','')
        try:
            #print(series[q].text.replace("\n", '').replace(' ', ''))
            audiobook['Series']=series[q].text.replace("\n", '').replace(' ', '').replace('Series:','')
        except:
            #print('Series None')
            audiobook['Series']='None'
        #print(lengths[q].text.replace("\n", '').replace(' ', ''))
        audiobook['Length']=lengths[q].text.replace("\n", '').replace(' ', '').replace('Length:','')
        #print(release_dates[q].text.replace("\n", '').replace(' ', ''))
        audiobook['Release date']=release_dates[q].text.replace("\n", '').replace(' ', '').replace('Releasedate:','')
        #print(languages1[q].text.replace("\n", '').replace(' ', ''))
        audiobook['Language']=languages1[q].text.replace("\n", '').replace(' ', '').replace('Language:','')
        #print(ratings[q].text.replace("\n", '').replace(' ', ''))
        audiobook['Ratings']=ratings[q].text.replace("\n", '').replace(' ', '').replace(':',': ').replace('stars','')
        #print('\n')
        audio_books.append(audiobook)

        #saving metadata to .json file
        with open(json_file_path, 'w',encoding='utf-8') as f:
            json.dump(audio_books, f, ensure_ascii=False, indent=4)
            print('Saved to .json file')

#####################################   PART 3  #####################################
#This program checks if given file wasn't previously downloaded
#not done
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
    
    for q in range(len(titles1)):
        curr_title = titles1[q]['aria-label']       # reading audiobook title as string
        if curr_title not in books_titles:          # if the movie isn't in the list we've created
            books_titles.append(curr_title)         # we add it to the list with already existing titles
            # now we add new audiobook
            audiobook = {}
            audiobook['Title'] = curr_title
            audiobook['By']=authors[q].text.replace("\n", '').replace(' ', '').replace('By:','')
            audiobook['Narrated by']=narrators[q-1].text.replace("\n", '').replace(' ', '').replace('Narratedby:','')
            try:
                audiobook['Series']=series[q].text.replace("\n", '').replace(' ', '').replace('Series:','')
            except:
                audiobook['Series']='None'
            audiobook['Length']=lengths[q].text.replace("\n", '').replace(' ', '').replace('Length:','')
            audiobook['Release date']=release_dates[q].text.replace("\n", '').replace(' ', '').replace('Releasedate:','')
            audiobook['Language']=languages1[q].text.replace("\n", '').replace(' ', '').replace('Language:','')
            audiobook['Ratings']=ratings[q].text.replace("\n", '').replace(' ', '').replace(':',': ').replace('stars','')
            books.append(audiobook)
            print('Checking is done')
        else:               #if the title exists in the list
            continue        #we skip loop iteration






#####################################   MAIN    #####################################
#it works for every site
# if __name__=="__main__":
#     for y in range(len(store_URL)):
#         try:
#             #print_and_download_audiobooks(store_URL[y])        -> should be working (if not -> check store_URL list starting from line 60)
#             #find_and_save_data(store_URL[y])                   -> should be working (if not -> check store_URL list starting from line 60)
#             print('Should be printed')
#             pass
#         except:
#             print('Something went wrong')
#             continue

#working
find_and_save_data('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test1.json')

#thank God it's working so I hope the rest is also working
#sample_site=f'https://www.audible.com/search?ref=a_search_c1_sort_{1}&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r={languages[2][3]}&feature_six_browse-bin={languages_code[2]}&sort={sorting[4]}&pageSize=50'
#print(sample_site)


# check_if_repeat('https://www.audible.com/search?sort=popularity-rank&pageSize=50&ipRedirectOverride=true&overrideBaseCountry=true', 'test1.json')

