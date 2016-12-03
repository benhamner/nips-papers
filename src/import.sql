.separator ","

CREATE TABLE papers (
    id INTEGER PRIMARY KEY,
    year INTEGER,
    title TEXT,
    event_type TEXT,
    pdf_name TEXT,
    abstract TEXT,
    paper_text TEXT);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT);

CREATE TABLE paper_authors (
    id INTEGER PRIMARY KEY,
    paper_id INTEGER,
    author_id INTEGER);

.import "working/no_header/papers.csv" papers
.import "working/no_header/authors.csv" authors
.import "working/no_header/paper_authors.csv" paper_authors

CREATE INDEX paperauthors_paperid_idx ON paper_authors (paper_id);
CREATE INDEX paperauthors_authorid_idx ON paper_authors (author_id);
