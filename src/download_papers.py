from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import re
import requests
import subprocess

def text_from_pdf(pdf_path):
    txt_path = pdf_path.replace("pdfs", "txts").replace(".pdf", ".txt")
    if not os.path.exists(os.path.dirname(txt_path)):
        os.makedirs(os.path.dirname(txt_path))
    if not os.path.exists(txt_path):
        subprocess.call(["pdftotext", pdf_path, txt_path])
    f = open(txt_path, encoding="utf8")
    text = f.read()
    f.close()
    return text

base_url  = "http://papers.nips.cc"

index_urls = {1987: "https://papers.nips.cc/book/neural-information-processing-systems-1987"}
for i in range(1, 33):
    year = i+1987
    index_urls[year] = "http://papers.nips.cc/book/advances-in-neural-information-processing-systems-%d-%d" % (i, year)

nips_authors = set()
papers = list()
paper_authors = list()

for year in sorted(index_urls.keys()):
    index_url = index_urls[year]
    index_html_path = os.path.join("working", "html", str(year)+".html")

    if not os.path.exists(index_html_path):
        r = requests.get(index_url)
        if not os.path.exists(os.path.dirname(index_html_path)):
            os.makedirs(os.path.dirname(index_html_path))
        with open(index_html_path, "wb") as index_html_file:
            index_html_file.write(r.content)
    with open(index_html_path, "rb") as f:
       html_content = f.read()
    soup = BeautifulSoup(html_content, "lxml")
    paper_links = [link for link in soup.find_all('a') if link["href"][:7]=="/paper/"]
    print("%d Papers Found" % len(paper_links))


    temp_path = os.path.join("working", "txt")

    for link in paper_links:
        # import pdb; pdb.set_trace()
        if "visual-sequence-learning-in-hierarchical-prediction-networks-and-primate-visual-cortex" in link['href']: continue
        paper_title = link.contents[0]
        info_link = base_url + link["href"]
        pdf_link = info_link + ".pdf"
        pdf_name = link["href"][7:] + ".pdf"
        pdf_path = os.path.join("working", "pdfs", str(year), pdf_name)
        paper_id = re.findall(r"^(\d+)-", pdf_name)[0]
        print(year, " ", paper_id) #paper_title.encode('ascii', 'namereplace'))
        if not os.path.exists(pdf_path):
            pdf = requests.get(pdf_link)
            if not os.path.exists(os.path.dirname(pdf_path)):
                os.makedirs(os.path.dirname(pdf_path))
            pdf_file = open(pdf_path, "wb")
            pdf_file.write(pdf.content)
            pdf_file.close()

        paper_info_html_path = os.path.join("working", "html", str(year), str(paper_id)+".html")
        if not os.path.exists(paper_info_html_path):
            r = requests.get(info_link)
            if not os.path.exists(os.path.dirname(paper_info_html_path)):
                os.makedirs(os.path.dirname(paper_info_html_path))
            with open(paper_info_html_path, "wb") as f:
                f.write(r.content)
        with open(paper_info_html_path, "rb") as f:
           html_content = f.read()
        paper_soup = BeautifulSoup(html_content, "lxml")
        try: 
            abstract = paper_soup.find('p', attrs={"class": "abstract"}).contents[0]
        except:
            print("Abstract not found %s" % paper_title.encode("ascii", "replace"))
            abstract = ""
        authors = [(re.findall(r"-(\d+)$", author.contents[0]["href"])[0],
                    author.contents[0].contents[0])
                   for author in paper_soup.find_all('li', attrs={"class": "author"})]
        for author in authors:
            nips_authors.add(author)
            paper_authors.append([len(paper_authors)+1, paper_id, author[0]])
        event_types = [h.contents[0][23:] for h in paper_soup.find_all('h3') if h.contents[0][:22]=="Conference Event Type:"]
        if len(event_types) != 1:
            #print(event_types)
            #print([h.contents for h in paper_soup.find_all('h3')].__str__().encode("ascii", "replace"))
            #raise Exception("Bad Event Data")
            event_type = ""
        else:
            event_type = event_types[0]
        with open(pdf_path, "rb") as f:
            if f.read(15)==b"<!DOCTYPE html>":
                print("PDF MISSING")
                continue
        if "visual-sequence-learning-in-hierarchical-prediction-networks-and-primate-visual-cortex" not in link:
            paper_text = text_from_pdf(pdf_path)
            papers.append([paper_id, year, paper_title, event_type, pdf_name, abstract, paper_text])

pd.DataFrame(list(nips_authors), columns=["id","name"]).sort_values(by="id").to_csv("output/authors.csv", index=False)
pd.DataFrame(papers, columns=["id", "year", "title", "event_type", "pdf_name", "abstract", "paper_text"]).sort_values(by="id").to_csv("output/papers.csv", index=False)
pd.DataFrame(paper_authors, columns=["id", "paper_id", "author_id"]).sort_values(by="id").to_csv("output/paper_authors.csv", index=False)
