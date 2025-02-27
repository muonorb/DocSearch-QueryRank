import xml.etree.ElementTree as ET
import pandas as pd
import csv

file_path = 'Search Engine/Datasets/cran.all.1400.xml'   
tree = ET.parse(file_path)
root = tree.getroot()

docnos = []
titles = []
authors = []
bibs = []
texts = []

for doc in root.findall('doc'):
    
    docno_element = doc.find('docno')
    docno = docno_element.text.strip() if docno_element is not None and docno_element.text is not None else ''
    
   
    title_element = doc.find('title')
    title = title_element.text.strip() if title_element is not None and title_element.text is not None else ''
    
    
    author_element = doc.find('author')
    author = author_element.text.strip() if author_element is not None and author_element.text is not None else ''
    
    
    bib_element = doc.find('bib')
    bib = bib_element.text.strip() if bib_element is not None and bib_element.text is not None else ''
    
    text_element = doc.find('text')
    text = text_element.text.strip() if text_element is not None and text_element.text is not None else ''
    
    docnos.append(docno)
    titles.append(title)
    authors.append(author)
    bibs.append(bib)
    texts.append(text)

data = {
    'docno': docnos,
    'title': titles,
    'author': authors,
    'bib': bibs,
    'text': texts
}

df = pd.DataFrame(data)

df.to_csv('cran_all.csv', index=False)



file_path = 'Search Engine/Datasets/cran.qry.xml' 
tree = ET.parse(file_path)
root = tree.getroot()

with open('cran_query.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(['num', 'title'])
    
    for top in root.findall('top'):
        num = top.find('num').text.strip()
        title = top.find('title').text.strip().replace('\n', ' ')
        
        csvwriter.writerow([num, title])

