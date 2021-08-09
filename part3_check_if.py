from libraries import *
from part1_URL import *
from part2_find_and_save import *

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
        
    try:
        with open(json_file, 'r',encoding='utf-8') as f:
            old_json = json.load(f)
    except Exception as e:
        print(e)
        old_json = []

    with open(json_file, 'w',encoding='utf-8') as f:
        json.dump(books + old_json, f, ensure_ascii=False, indent=4)

    print('Saved to .json file')
    print('Checking is done')

