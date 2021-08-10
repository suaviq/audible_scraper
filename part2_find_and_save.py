from libraries import *
from part1_URL import *

#####################################   PART 2  #####################################
#This program finds data from html about audiobooks and saves it to .json file
# also finds links to sample and downloads it if needed

#working

def find_and_save_data(url, json_file_path):
    list_samples = []
    list_titles = []
    page = ''
    while page == '':
        try:
            page = requests.get(url).text
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    s = BeautifulSoup(page, 'html.parser')
    try:
        audiobooks1 = s.find('div', class_ = 'adbl-impression-container')
        time.sleep(1)
    except:
        print('Error with finding a tag adbl-impression-container')

    try:
        titles1 = audiobooks1.findAll('li', class_ = 'bc-list-item productListItem')
        time.sleep(1) 
    except:
        print('Error with finding a tag bc-list-item productListItem -> title')

    try:
        authors = audiobooks1.findAll('li', class_ = 'bc-list-item authorLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item authorLabel -> author')

    try:
        narrators = audiobooks1.findAll('li', class_ = 'bc-list-item narratorLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item narratorLabel -> narrators')

    try:
        series = audiobooks1.findAll('li', class_ = 'bc-list-item seriesLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item seriesLabel -> series')

    try:
        lengths = audiobooks1.findAll('li', class_ = 'bc-list-item runtimeLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item runtimeLabel -> length')

    try:
        release_dates = audiobooks1.findAll('li', class_ = 'bc-list-item releaseDateLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item releaseDateLabel -> release date')
        
    try:
        languages1 = audiobooks1.findAll('li', class_ = 'bc-list-item languageLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item languageLabel -> language')

    try:
        ratings = audiobooks1.findAll('li', class_ = 'bc-list-item ratingsLabel')
        time.sleep(1)
    except:
        print('Error with finding a tag bc-list-item ratingsLabel -> ratings')

    try:
        samples = audiobooks1.findAll('button', class_ = 'bc-button-text')
        time.sleep(2)
    except:
        print('Error with finding a tag bc-button-text -> sample')
# print('https://samples.audible.com/bk/peng/005907/bk_peng_005907_sample.mp3')
# url = 'https://samples.audible.com/bk/peng/005907/bk_peng_005907_sample.mp3'
# r = requests.get(url, allow_redirects=True)
# title_sample = 'test'
# open(f'{title_sample}.mp3', 'wb').write(r.content)
    

#working
    audio_books = []

    for title in range(len(titles1)):
        audiobook = {}
        audiobook['Title'] = titles1[title]['aria-label']
        list_titles.append(titles1[title]['aria-label'])
        try:
            audiobook['Link to sample']=samples[title]['data-mp3']
            list_samples.append(samples[title]['data-mp3'])
            print(samples[title]['data-mp3'])
        except:
            audiobook['Link to sample']='None'
        try:
            audiobook['By']=authors[title].text.replace("\n", '').replace(' ', '').replace('By:','')
        except:
            audiobook['By']='None'
        try:
            audiobook['Narrated by']=narrators[title].text.replace("\n", '').replace(' ', '').replace('Narratedby:','')
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
    # try:
    #     with open(json_file_path, 'r',encoding='utf-8') as f:
    #         old_json = json.load(f)
    # except Exception as e:
    #     print(e)
    #     # old_json = []
    # audio_books + old_json

        with open(json_file_path, 'w',encoding='utf-8') as f:
            json.dump(audio_books, f, ensure_ascii=False, indent=4)

    print('Saved to .json file')

    return list_titles, list_samples
