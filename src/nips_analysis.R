setwd("/Users/benhamner/Git/nips-papers/output")

library(dplyr)
library(ggplot2)
library(readr)
library(tidyr)

papers <- read_csv("papers.csv")

papers$paper_text_no_refs <- str_c(str_sub(papers$paper_text, 1, floor(str_length(papers$paper_text)/2)), 
                                   sub("references.*", "references", 
                                       str_sub(papers$paper_text, floor(str_length(papers$paper_text)/2)+1,-1),
                                       ignore.case=TRUE))

papers$char_count <- str_length(papers$paper_text)
papers$no_ref_char_count <- str_length(papers$paper_text_no_refs)
papers$body_proportion <- papers$no_ref_char_count/papers$char_count

ggplot(papers, aes(x=papers$body_proportion)) + geom_histogram(bins=100)

ggplot(papers, aes(x=year, y=char_count))+geom_point()

ggplot(papers, aes(x=char_count)) + geom_histogram(bins=100)

grep("references", papers$paper_text, ignore.case=TRUE)

grep("imagenet", papers$paper_text, ignore.case=TRUE)
grep("imagenet", papers$paper_text, ignore.case=TRUE)
grep("cifar", papers$paper_text, ignore.case=TRUE)

papers[grep("kaggle", papers$paper_text, ignore.case=TRUE), "PdfName"]

ggplot(papers %>% group_by(year) %>% summarise(count=n()), aes(x=year, y=count))+geom_point()


ind <- grep("(github.com)", papers$paper_text, ignore.case = TRUE)
print(length(ind))
srclist <- lapply(papers$paper_text[ind], str_extract_all, 
                  "[^[:space:](]*(https?:\\n?//)?github.com/\\n?[^[:space:]/)]+(\\n?/\\n?[^).[:space:]]+)?")
srclist <- unlist(srclist)
srclist <- unlist(lapply(srclist, function(x) gsub("\n|\"|,", "", x)))
print(srclist)



# Filter out references

# Kaggle occurrences over time
# NIPS 2015 papers vs. NIPS 2016 papers classifier?
# deep learning, svm's, 
# trends over time
