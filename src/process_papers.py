from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import re
import requests
import subprocess

def text_from_pdf(pdf_path, temp_path):
    if os.path.exists(temp_path):
        os.remove(temp_path)
    subprocess.call(["pdftotext", pdf_path, temp_path])
    f = open(temp_path, encoding="utf8")
    text = f.read()
    f.close()
    os.remove(temp_path)
    return text

papers = list()
temp_path = os.path.join("output", "temp.txt")

for year in range(1987,2017):

    pdf_names = [p for p in os.listdir(os.path.join("output", "pdfs", str(year))) if p.endswith(".pdf")]

    for pdf_name in pdf_names:
        pdf_path = os.path.join("output", "pdfs", str(year), pdf_name)
        print(year, pdf_path, len(papers))
        paper_id = re.findall(r"^(\d+)-", pdf_name)[0]
        with open(pdf_path, "rb") as f:
            if f.read(15)==b"<!DOCTYPE html>":
                print("PDF MISSING")
                continue
        paper_text = text_from_pdf(pdf_path, temp_path)
        papers.append([paper_id, year, pdf_name, paper_text])

pd.DataFrame(papers, columns=["Id", "Year", "PdfName", "PaperText"]).to_csv("output/Papers.csv", index=False)

print("COMPLETED")
