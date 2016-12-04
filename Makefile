output/papers.csv:
	mkdir -p output
	bpython src/download_papers.py
csv: output/papers.csv

working/no_header/papers.csv: output/papers.csv
	mkdir -p working/no_header
	tail +2 $^ > $@

working/no_header/authors.csv: output/authors.csv
	mkdir -p working/no_header
	tail +2 $^ > $@

working/no_header/paper_authors.csv: output/paper_authors.csv
	mkdir -p working/no_header
	tail +2 $^ > $@

output/database.sqlite: working/no_header/papers.csv working/no_header/paper_authors.csv working/no_header/authors.csv
	-rm output/database.sqlite
	sqlite3 -echo $@ < src/import.sql
db: output/database.sqlite

all: csv db

clean:
	rm -rf working
	rm -rf output
