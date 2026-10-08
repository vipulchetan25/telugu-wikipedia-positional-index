# Telugu Wikipedia Positional Inverted Index and Search Engine

A complete **Information Retrieval (IR) system for Telugu text** built
using a subset of the Telugu Wikipedia corpus.

This project demonstrates how a search engine can efficiently search a
large collection of Telugu Wikipedia articles using an **Inverted
Index** and a **Positional Inverted Index**. It covers the complete
pipeline: article extraction, Wikipedia markup cleaning, Unicode
normalization, Telugu tokenization, stop-word removal, index
construction, word search, phrase search, and a Flask-based web
interface.

------------------------------------------------------------------------

## Table of Contents

-   [1. Project Overview](#1-project-overview)
-   [2. What is Information
    Retrieval?](#2-what-is-information-retrieval)
-   [3. Problem Statement](#3-problem-statement)
-   [4. Why Do We Need an Index?](#4-why-do-we-need-an-index)
-   [5. What is an Inverted Index?](#5-what-is-an-inverted-index)
-   [6. Why is a Normal Inverted Index Not
    Enough?](#6-why-is-a-normal-inverted-index-not-enough)
-   [7. What is a Positional Inverted
    Index?](#7-what-is-a-positional-inverted-index)
-   [8. Why Are Positions Important?](#8-why-are-positions-important)
-   [9. Project Objectives](#9-project-objectives)
-   [10. Dataset](#10-dataset)
-   [11. Why Telugu Wikipedia?](#11-why-telugu-wikipedia)
-   [12. Complete System Architecture](#12-complete-system-architecture)
-   [13. Complete Data Flow](#13-complete-data-flow)
-   [14. Document Extraction](#14-document-extraction)
-   [15. Wikipedia Markup Cleaning](#15-wikipedia-markup-cleaning)
-   [16. Unicode Normalization](#16-unicode-normalization)
-   [17. Tokenization](#17-tokenization)
-   [18. Stop-word Removal](#18-stop-word-removal)
-   [19. Why Query and Document Preprocessing Must
    Match](#19-why-query-and-document-preprocessing-must-match)
-   [20. Building the Positional Inverted
    Index](#20-building-the-positional-inverted-index)
-   [21. Index Structure](#21-index-structure)
-   [22. Single-word Search](#22-single-word-search)
-   [23. Phrase Search](#23-phrase-search)
-   [24. Candidate Document
    Intersection](#24-candidate-document-intersection)
-   [25. Position Matching Algorithm](#25-position-matching-algorithm)
-   [26. Search Example](#26-search-example)
-   [27. Difference Between Inverted and Positional
    Indexes](#27-difference-between-inverted-and-positional-indexes)
-   [28. Web Application](#28-web-application)
-   [29. Project Files](#29-project-files)
-   [30. Technologies Used](#30-technologies-used)
-   [31. Data Structures](#31-data-structures)
-   [32. Complexity](#32-complexity)
-   [33. Dataset and Project
    Statistics](#33-dataset-and-project-statistics)
-   [34. Installation](#34-installation)
-   [35. Running the Complete
    Pipeline](#35-running-the-complete-pipeline)
-   [36. Generated Files](#36-generated-files)
-   [37. GitHub Repository Design](#37-github-repository-design)
-   [38. Limitations](#38-limitations)
-   [39. Future Improvements](#39-future-improvements)
-   [40. IR Concepts Demonstrated](#40-ir-concepts-demonstrated)
-   [41. Learning Outcomes](#41-learning-outcomes)
-   [42. Final Summary](#42-final-summary)
-   [43. Author](#43-author)

------------------------------------------------------------------------

# 1. Project Overview

Imagine that we have thousands of Telugu Wikipedia articles and a user
wants to search for a particular Telugu word.

For example:

``` text
తెలుగు
```

A naive search engine could open every article and check whether the
word exists. If there are 10,000 articles, every query could potentially
require checking thousands of documents.

Information Retrieval systems solve this problem by creating an **index
before the user searches**.

The idea is similar to the index at the back of a textbook:

``` text
Computer ........ 12, 35, 72
Database ........ 18, 42
Network ......... 24, 91
```

An Information Retrieval system uses the same general idea for digital
documents.

For this project, the relationship is:

``` text
Term → Documents
```

This is an **Inverted Index**.

However, phrase searching requires more information. For a query such
as:

``` text
తెలుగు భాష
```

we need to know not only whether both words occur in a document, but
also whether they occur next to each other.

Therefore, this project uses a:

> **Positional Inverted Index**

whose structure is:

``` text
Term → Document ID → Positions
```

------------------------------------------------------------------------

# 2. What is Information Retrieval?

**Information Retrieval (IR)** is the process of finding relevant
information from a collection of documents based on a user's query.

A document collection can contain:

-   Wikipedia articles
-   Web pages
-   Books
-   Research papers
-   News articles
-   Emails
-   Product descriptions
-   Other text documents

In this project, the document collection is:

``` text
Telugu Wikipedia articles
```

A simplified Information Retrieval system works like this:

``` text
Document Collection
        ↓
Document Processing
        ↓
Index Construction
        ↓
User Query
        ↓
Query Processing
        ↓
Retrieval
        ↓
Search Results
```

The important idea is that documents are processed and indexed
**before** users perform searches.

------------------------------------------------------------------------

# 3. Problem Statement

The goal of this project is to answer:

> How can we efficiently search a large collection of Telugu Wikipedia
> articles for individual words and phrases without scanning every
> article for every query?

The project solves this using:

1.  Wikipedia article extraction
2.  Wikipedia markup cleaning
3.  Unicode normalization
4.  Telugu tokenization
5.  Telugu stop-word removal
6.  Inverted indexing
7.  Positional indexing
8.  Phrase searching
9.  A Flask web search interface

------------------------------------------------------------------------

# 4. Why Do We Need an Index?

Suppose there are 10,000 documents and the user searches:

``` text
తెలుగు
```

Without an index, a simple approach would be:

``` text
Check Document 1
Check Document 2
Check Document 3
...
Check Document 10000
```

This becomes expensive as the collection grows.

With an inverted index, we store the answer beforehand:

``` text
తెలుగు → [12, 25, 486, 637, 901, ...]
```

Now the system can directly find the matching documents.

The difference is:

``` text
Without Index:

Query
  ↓
Scan documents
  ↓
Find matches
```

versus:

``` text
With Index:

Query
  ↓
Look up term
  ↓
Retrieve matching documents
```

This is the fundamental motivation for an inverted index.

------------------------------------------------------------------------

# 5. What is an Inverted Index?

An **Inverted Index** is a data structure that maps a term to the
documents in which that term occurs.

Normally, we think about documents containing terms:

``` text
Document 1 → తెలుగు, భాష, భారతదేశం
Document 2 → తెలుగు, సాహిత్యం, భాష
```

An inverted index reverses this relationship:

``` text
తెలుగు → Document 1, Document 2
భాష → Document 1, Document 2
భారతదేశం → Document 1
సాహిత్యం → Document 2
```

Therefore:

``` text
Document → Terms
```

becomes:

``` text
Term → Documents
```

This is why it is called an **inverted** index.

### Example

Suppose:

``` text
Document 1:
తెలుగు భాష భారతదేశంలో మాట్లాడబడుతుంది

Document 2:
తెలుగు సాహిత్యం చాలా ప్రాచీనమైనది
```

The inverted index could be:

``` text
తెలుగు → [1, 2]
భాష → [1]
భారతదేశంలో → [1]
మాట్లాడబడుతుంది → [1]
సాహిత్యం → [2]
ప్రాచీనమైనది → [2]
```

Searching for `తెలుగు` now becomes a direct index lookup.

------------------------------------------------------------------------

# 6. Why is a Normal Inverted Index Not Enough?

Consider the query:

``` text
తెలుగు భాష
```

A normal inverted index can tell us that both terms occur in a document:

``` text
తెలుగు → [1, 2]
భాష → [1, 2]
```

Therefore, both Document 1 and Document 2 contain both terms.

But that does **not** mean both documents contain the phrase:

``` text
తెలుగు భాష
```

Consider:

### Document 1

``` text
తెలుగు భాష భారతదేశంలో మాట్లాడబడుతుంది
```

The two words occur next to each other.

### Document 2

``` text
తెలుగు భారతదేశంలో మాట్లాడే ఒక భాష
```

Both words occur, but they are separated.

A normal inverted index does not store enough information to distinguish
these cases.

It only tells us:

``` text
Does this document contain the term?
```

It does not tell us:

``` text
Where does the term occur?
```

To answer that question, we need term positions.

------------------------------------------------------------------------

# 7. What is a Positional Inverted Index?

A **Positional Inverted Index** extends an inverted index by storing the
positions at which each term occurs in each document.

Normal inverted index:

``` text
Term → Documents
```

Positional inverted index:

``` text
Term → Document → Positions
```

For example:

``` text
తెలుగు
    Document 486 → [1, 13, 143, 151, 158]

భాష
    Document 486 → [2, 14, 144, 152, 159]
```

This tells us:

-   `తెలుగు` occurs in Document 486.
-   It occurs at positions 1, 13, 143, 151, and 158.
-   `భాష` occurs in Document 486.
-   It occurs at positions 2, 14, 144, 152, and 159.

Now the search engine can determine whether the words occur
consecutively.

------------------------------------------------------------------------

# 8. Why Are Positions Important?

Suppose:

``` text
తెలుగు → position 10
భాష   → position 11
```

Then:

``` text
11 = 10 + 1
```

So:

``` text
తెలుగు భాష
```

occurs as a phrase.

But if:

``` text
తెలుగు → position 10
భాష   → position 15
```

then:

``` text
15 ≠ 10 + 1
```

Therefore, the exact phrase does not occur at that location.

This is the core idea of phrase searching in this project.

------------------------------------------------------------------------

# 9. Project Objectives

The main objectives are:

-   Build an Information Retrieval system for Telugu.
-   Work with a real-world regional-language corpus.
-   Process Telugu Unicode text.
-   Extract articles from a Wikipedia dump.
-   Clean Wikipedia-specific markup.
-   Normalize Unicode text.
-   Tokenize Telugu text.
-   Remove common Telugu stop words.
-   Build an inverted index.
-   Extend it into a positional inverted index.
-   Support single-word searching.
-   Support phrase searching.
-   Display term positions.
-   Provide a browser-based search interface.
-   Understand the complete indexing and retrieval pipeline.

------------------------------------------------------------------------

# 10. Dataset

The project uses:

> **Telugu Wikipedia**

The original Telugu Wikipedia article dump is distributed as a large
compressed XML file.

The project extracts a subset of:

``` text
10,000 Telugu Wikipedia articles
```

The original dump is several gigabytes in size and is therefore not
included in the GitHub repository.

The local processing flow is:

``` text
Telugu Wikipedia Dump
        ↓
XML Parsing
        ↓
Article Filtering
        ↓
Text Cleaning
        ↓
10,000 Articles
        ↓
articles.json
```

------------------------------------------------------------------------

# 11. Why Telugu Wikipedia?

This project intentionally uses a regional Indian language rather than
an English corpus.

Telugu introduces practical challenges such as:

-   Unicode text processing
-   Telugu-specific tokenization
-   Telugu stop words
-   Regional-language preprocessing
-   Non-ASCII text handling

This makes the project useful for understanding how Information
Retrieval techniques can be applied to languages other than English.

------------------------------------------------------------------------

# 12. Complete System Architecture

``` text
                 TELUGU WIKIPEDIA DUMP
                          │
                          ▼
                 Article Extraction
                          │
                          ▼
                Wikipedia Markup Cleaning
                          │
                          ▼
                    Article Dataset
                          │
                          ▼
                 Unicode Normalization
                          │
                          ▼
                    Tokenization
                          │
                          ▼
                  Stop-word Removal
                          │
                          ▼
              Positional Index Construction
                          │
                          ▼
                 Positional Index
                          │
                          ▼
                     User Query
                          │
                          ▼
                   Query Processing
                          │
                          ▼
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
         Single Term             Multiple Terms
              │                       │
              ▼                       ▼
      Inverted Index          Positional Search
              │                       │
              └───────────┬───────────┘
                          ▼
                    Search Results
                          │
                          ▼
                     Flask Web UI
```

------------------------------------------------------------------------

# 13. Complete Data Flow

## Phase A --- Indexing

``` text
Wikipedia Dump
      ↓
Extract Articles
      ↓
Clean Wikipedia Markup
      ↓
Store Articles
      ↓
Normalize Unicode
      ↓
Tokenize
      ↓
Remove Stop Words
      ↓
Build Positional Index
      ↓
Save Index
```

## Phase B --- Searching

``` text
User Query
      ↓
Query Preprocessing
      ↓
Tokenization
      ↓
Stop-word Removal
      ↓
Determine Query Type
      ↓
Single Term? ───────→ Inverted Index
      │
      └── Multiple Terms ─→ Positional Index
                                  ↓
                           Position Matching
                                  ↓
                           Matching Documents
                                  ↓
                             Search Results
```

------------------------------------------------------------------------

# 14. Document Extraction

The raw Wikipedia dump contains XML data and is compressed using BZ2.

The file:

``` text
extract_articles.py
```

handles article extraction.

The script:

1.  Opens the compressed Wikipedia dump.
2.  Parses the XML.
3.  Identifies Wikipedia pages.
4.  Checks the namespace.
5.  Keeps normal article pages.
6.  Extracts the article title.
7.  Extracts article text.
8.  Cleans Wikipedia markup.
9.  Keeps the configured number of articles.
10. Saves the articles as JSON.

Output:

``` text
data/articles.json
```

------------------------------------------------------------------------

# 15. Wikipedia Markup Cleaning

Wikipedia source text contains structures that should not directly enter
the search index.

Examples include:

``` text
{{template}}

<ref>citation</ref>

[[Article]]

[[Article|Displayed Text]]

[https://example.com Website]

''italic text''

'''bold text'''
```

The extraction process removes or simplifies:

-   Templates
-   References
-   HTML/XML tags
-   Internal links
-   External links
-   URLs
-   Formatting markers
-   Excess whitespace

### Example

Before cleaning:

``` text
[[తెలుగు భాష]] అనేది {{template}} భారతదేశంలో
ఉపయోగించే భాష. <ref>Some reference</ref>
```

After cleaning:

``` text
తెలుగు భాష అనేది భారతదేశంలో ఉపయోగించే భాష.
```

The cleaned text is then passed to preprocessing.

------------------------------------------------------------------------

# 16. Unicode Normalization

Telugu is represented using Unicode.

Unicode allows computers to represent characters from different writing
systems consistently.

The project uses **NFC normalization**:

``` python
unicodedata.normalize("NFC", text)
```

The purpose is to make equivalent Unicode representations consistent
before tokenization and indexing.

The process is:

``` text
Raw Telugu Text
       ↓
Unicode NFC Normalization
       ↓
Normalized Telugu Text
```

This is important because the project processes a regional language
rather than only ASCII English text.

------------------------------------------------------------------------

# 17. Tokenization

After cleaning and normalization, the text needs to be divided into
individual searchable terms.

This process is called **tokenization**.

For example:

``` text
తెలుగు భాష భారతదేశంలో మాట్లాడబడుతుంది
```

can become:

``` text
[
    "తెలుగు",
    "భాష",
    "భారతదేశంలో",
    "మాట్లాడబడుతుంది"
]
```

The project identifies Telugu text using the Telugu Unicode block:

``` text
U+0C00 – U+0C7F
```

These tokens become the input to the indexing process.

------------------------------------------------------------------------

# 18. Stop-word Removal

Not every token is equally useful for retrieval.

Some words are very common and mainly perform grammatical or functional
roles.

The project maintains a Telugu stop-word set containing common terms
such as:

``` text
అది
అని
ఇది
కోసం
మరియు
కు
తో
లో
నుండి
```

The preprocessing flow is:

``` text
Article
   ↓
Tokenization
   ↓
Tokens
   ↓
Stop-word Filtering
   ↓
Searchable Tokens
```

Removing common stop words can reduce unnecessary index entries and
focus the index on more useful terms.

The current list is a manually defined starter list for this academic
project and can be expanded.

------------------------------------------------------------------------

# 19. Why Query and Document Preprocessing Must Match

The same preprocessing logic must be applied to both documents and
queries.

Otherwise, the terms stored in the index may not match the terms
generated from the user's query.

The project therefore uses:

``` text
preprocess.py
```

for both stages.

During indexing:

``` text
Document
   ↓
preprocess()
   ↓
Tokens
   ↓
Index
```

During searching:

``` text
Query
   ↓
preprocess()
   ↓
Tokens
   ↓
Index Lookup
```

This keeps document and query representations consistent.

------------------------------------------------------------------------

# 20. Building the Positional Inverted Index

The positional index is constructed by:

``` text
build_index.py
```

For every article:

1.  Read the document ID.
2.  Read the article text.
3.  Preprocess the text.
4.  Generate tokens.
5.  Assign a position to every processed token.
6.  Add the term to the index.
7.  Store the document ID.
8.  Append the term position.

Conceptually:

``` text
Document
   ↓
Preprocess
   ↓
Token 1
Token 2
Token 3
Token 4
...
   ↓
Assign Positions
   ↓
Add to Index
```

For example:

``` text
Text:

తెలుగు భాష భారతదేశంలో ఉంది
```

can produce:

``` text
Position 1 → తెలుగు
Position 2 → భాష
Position 3 → భారతదేశంలో
Position 4 → ఉంది
```

The index can then contain:

``` text
తెలుగు → Document 1 → [1]
భాష → Document 1 → [2]
భారతదేశంలో → Document 1 → [3]
```

------------------------------------------------------------------------

# 21. Index Structure

The core data structure is:

``` text
Term
  ↓
Document ID
  ↓
Positions
```

For example:

``` text
{
    "తెలుగు": {
        "486": [1, 13, 143, 151],
        "637": [5, 27, 91]
    }
}
```

This means:

``` text
Term: తెలుగు

Document 486:
    positions = 1, 13, 143, 151

Document 637:
    positions = 5, 27, 91
```

This structure is called a **positional postings list**.

------------------------------------------------------------------------

# 22. Single-word Search

Suppose the user searches:

``` text
తెలుగు
```

The query first goes through preprocessing:

``` text
"తెలుగు"
    ↓
Tokenization
    ↓
["తెలుగు"]
```

Since there is one searchable term, the system performs an
inverted-index lookup.

Conceptually:

``` python
index["తెలుగు"]
```

The result contains the documents in which the term occurs.

For example:

``` text
[
    "12",
    "25",
    "486",
    "637"
]
```

The system then maps those document IDs to article titles.

### Single-word search flow

``` text
Query
  ↓
Preprocessing
  ↓
Single Token
  ↓
Inverted Index Lookup
  ↓
Matching Documents
  ↓
Article Titles
```

------------------------------------------------------------------------

# 23. Phrase Search

Now consider:

``` text
తెలుగు భాష
```

The query becomes:

``` text
[
    "తెలుగు",
    "భాష"
]
```

The system must find documents where the two terms occur consecutively.

The process is:

``` text
Query
  ↓
Preprocessing
  ↓
Multiple Tokens
  ↓
Find Candidate Documents
  ↓
Compare Positions
  ↓
Check Consecutive Occurrence
  ↓
Return Phrase Matches
```

------------------------------------------------------------------------

# 24. Candidate Document Intersection

Suppose:

``` text
తెలుగు → [10, 25, 486, 637]

భాష → [10, 25, 486]
```

The documents containing both terms are:

``` text
[10, 25, 486]
```

This is the **candidate document set**.

There is no reason to perform positional matching on documents that do
not contain all query terms.

Therefore, the system first performs document intersection and then
checks positions.

Conceptually:

``` text
Documents(తెలుగు)
        ∩
Documents(భాష)
        =
Candidate Documents
```

This reduces unnecessary positional comparisons.

------------------------------------------------------------------------

# 25. Position Matching Algorithm

Suppose Document 486 contains:

``` text
తెలుగు → [1, 13, 143, 151]

భాష → [2, 14, 144, 160]
```

For the phrase:

``` text
తెలుగు భాష
```

the algorithm checks whether:

``` text
position(భాష) = position(తెలుగు) + 1
```

The comparisons are:

``` text
1 + 1 = 2      ✓
13 + 1 = 14    ✓
143 + 1 = 144  ✓
151 + 1 = 152  ✗
```

Therefore, the phrase occurs at starting positions:

``` text
1
13
143
```

The document is returned as a phrase match.

------------------------------------------------------------------------

# 26. Search Example

Consider:

``` text
Document 1:

తెలుగు భాష భారతదేశంలో మాట్లాడే ప్రధాన భాషలలో ఒకటి.
```

After preprocessing, suppose the positions are:

``` text
1 → తెలుగు
2 → భాష
3 → భారతదేశంలో
4 → మాట్లాడే
5 → ప్రధాన
6 → భాషలలో
7 → ఒకటి
```

The index contains:

``` text
తెలుగు → Document 1 → [1]

భాష → Document 1 → [2]

భారతదేశంలో → Document 1 → [3]
```

Now search:

``` text
తెలుగు భాష
```

The system checks:

``` text
తెలుగు → position 1
భాష   → position 2
```

Since:

``` text
2 = 1 + 1
```

the phrase is found.

Now consider:

``` text
తెలుగు భారతదేశంలో మాట్లాడే ప్రధాన భాష
```

If:

``` text
తెలుగు → [1]
భాష → [5]
```

then:

``` text
5 ≠ 1 + 1
```

so the exact phrase `తెలుగు భాష` does not occur there.

This example demonstrates why positional information is necessary.

------------------------------------------------------------------------

# 27. Difference Between Inverted and Positional Indexes

  Feature                    Inverted Index   Positional Inverted Index
  -------------------------- ---------------- ---------------------------
  Maps terms to documents    Yes              Yes
  Stores document IDs        Yes              Yes
  Stores term positions      No               Yes
  Supports keyword search    Yes              Yes
  Supports phrase search     Limited          Yes
  Knows term order           No               Yes
  Checks consecutive terms   No               Yes

The essential difference is:

``` text
Inverted Index:

Term → Documents
```

versus:

``` text
Positional Inverted Index:

Term → Documents → Positions
```

------------------------------------------------------------------------

# 28. Web Application

The project includes a Flask-based web interface implemented in:

``` text
app.py
```

Start the application with:

``` bash
python app.py
```

Then open:

``` text
http://127.0.0.1:5000
```

The browser interface allows users to search Telugu words and phrases.

It can display:

-   Search query
-   Search type
-   Number of results
-   Search execution time
-   Article title
-   Document ID
-   Matching positions

Example:

``` text
Query:
తెలుగు భాష

Search Type:
Positional Inverted Index

Results:
47 documents
```

A result can show:

``` text
Article Title

Document ID: 486

Matching positions:

తెలుగు → [1, 13, 143, 151, ...]
భాష → [2, 14, 144, 152, ...]
```

Displaying positions makes the positional indexing concept visible
rather than hiding it behind the search interface.

------------------------------------------------------------------------

# 29. Project Files

## `extract_articles.py`

Responsible for extracting articles from the compressed Telugu Wikipedia
XML dump.

Responsibilities:

-   Open the `.bz2` file
-   Parse XML
-   Identify Wikipedia article pages
-   Ignore non-main namespaces
-   Extract titles
-   Extract article text
-   Clean Wikipedia markup
-   Save the selected articles

Output:

``` text
data/articles.json
```

## `preprocess.py`

Contains the common text preprocessing pipeline.

Responsibilities:

-   Unicode NFC normalization
-   Whitespace normalization
-   Telugu tokenization
-   Telugu stop-word removal

It is used during both indexing and searching.

## `build_index.py`

Builds the positional inverted index.

Responsibilities:

-   Load articles
-   Preprocess text
-   Generate tokens
-   Assign positions
-   Build postings lists
-   Save the index

Output:

``` text
data/positional_index.json
```

## `search.py`

Provides the terminal-based search engine.

Supports:

-   Single-word search
-   Multi-word phrase search
-   Inverted index lookup
-   Positional matching
-   Result display

## `app.py`

Provides the Flask web interface.

Responsibilities:

-   Load articles
-   Load the positional index
-   Accept queries
-   Preprocess queries
-   Select the appropriate search method
-   Retrieve matching documents
-   Display results

## `README.md`

Contains the complete technical documentation for the project.

## `.gitignore`

Prevents large and generated files from being committed to GitHub.

------------------------------------------------------------------------

# 30. Technologies Used

  Technology            Purpose
  --------------------- --------------------------------
  Python                Core implementation
  Flask                 Web-based search interface
  JSON                  Article and index storage
  XML                   Wikipedia dump parsing
  BZ2                   Reading compressed dump
  Regular Expressions   Text cleaning and tokenization
  Unicode               Telugu text processing

------------------------------------------------------------------------

# 31. Data Structures

The most important data structure is the positional index.

Conceptually:

``` text
Index
 │
 ├── Term 1
 │      ├── Document 1
 │      │      └── Positions
 │      └── Document 2
 │             └── Positions
 │
 └── Term 2
        ├── Document 1
        │      └── Positions
        └── Document 5
               └── Positions
```

In Python, this is represented using nested dictionaries and lists.

Example:

``` text
{
    "తెలుగు": {
        "486": [1, 13, 143],
        "637": [5, 27, 91]
    }
}
```

A term can occur multiple times in the same document, which is why the
position information is stored as a list.

------------------------------------------------------------------------

# 32. Complexity

Let:

``` text
D = number of documents
T = total number of processed tokens
V = number of unique terms
P = number of stored positions
```

## Index Construction

Every processed token is visited during indexing.

Therefore, the main indexing work is approximately:

``` text
O(T)
```

The actual runtime also depends on preprocessing and file I/O.

## Single-word Search

A dictionary lookup for a term is approximately:

``` text
O(1)
```

After finding the term, the system retrieves its postings list.
Therefore, practical work also depends on the number of matching
documents.

## Phrase Search

Phrase search requires:

1.  Candidate document intersection.
2.  Position retrieval.
3.  Position comparisons.

Its cost depends on:

-   Number of query terms
-   Number of candidate documents
-   Number of positions in the postings lists

It is still more efficient than scanning the entire document collection
for every query.

------------------------------------------------------------------------

# 33. Dataset and Project Statistics

  Property                                      Value
  ----------------------- ---------------------------
  Language                                     Telugu
  Source                             Telugu Wikipedia
  Articles                                     10,000
  Search Types                          Word + Phrase
  Index                     Positional Inverted Index
  Interface                                     Flask
  Storage                                        JSON
  Text Encoding                                 UTF-8
  Unicode Normalization                           NFC

During development, the 10,000-article collection produced millions of
processed tokens and hundreds of thousands of unique terms.

The exact index statistics can change if the dataset or preprocessing
configuration is modified.

------------------------------------------------------------------------

# 34. Installation

## Step 1 --- Clone the Repository

``` bash
git clone https://github.com/vipulchetan25/telugu-wikipedia-positional-index.git
```

Then:

``` bash
cd telugu-wikipedia-positional-index
```

## Step 2 --- Create a Virtual Environment

On Windows:

``` bash
python -m venv venv
```

Activate it:

``` bash
venv\Scripts\activate
```

## Step 3 --- Install Dependencies

``` bash
pip install flask
```

------------------------------------------------------------------------

# 35. Running the Complete Pipeline

## Step 1 --- Obtain the Telugu Wikipedia Dump

Download the Telugu Wikipedia article dump and place it in the project
root.

Expected local filename:

``` text
tewiki.xml.bz2
```

The dump is not included in GitHub because of its large size.

## Step 2 --- Extract Articles

``` bash
python extract_articles.py
```

This creates:

``` text
data/articles.json
```

## Step 3 --- Build the Positional Index

``` bash
python build_index.py
```

This performs:

``` text
Load Articles
      ↓
Preprocess Text
      ↓
Tokenize
      ↓
Remove Stop Words
      ↓
Assign Positions
      ↓
Build Positional Index
      ↓
Save Index
```

Output:

``` text
data/positional_index.json
```

## Step 4 --- Test the Terminal Search

``` bash
python search.py
```

Try:

``` text
తెలుగు
```

or:

``` text
తెలుగు భాష
```

## Step 5 --- Start the Web Search Engine

``` bash
python app.py
```

Open:

``` text
http://127.0.0.1:5000
```

------------------------------------------------------------------------

# 36. Generated Files

The indexing process creates:

``` text
data/
├── articles.json
└── positional_index.json
```

### `articles.json`

Contains:

-   Document ID
-   Article title
-   Cleaned article text

Conceptually:

``` text
[
    {
        "id": 1,
        "title": "...",
        "text": "..."
    }
]
```

### `positional_index.json`

Contains:

``` text
Term → Document ID → Positions
```

These files are generated locally.

------------------------------------------------------------------------

# 37. GitHub Repository Design

The repository contains the source code and documentation needed to
reproduce the project.

The following files are intentionally excluded:

``` text
tewiki.xml.bz2
data/articles.json
data/positional_index.json
venv/
```

This is handled using `.gitignore`.

Keeping generated and very large files out of GitHub makes the
repository lightweight while preserving the complete reproducible
pipeline.

------------------------------------------------------------------------

# 38. Limitations

This project is primarily an educational implementation of Information
Retrieval.

### 1. Limited Dataset

Only 10,000 articles are currently indexed.

### 2. Basic Stop-word List

The current Telugu stop-word list is a manually defined starter list.

### 3. No Stemming

Related word forms are currently treated as separate terms.

### 4. No Lemmatization

Telugu morphological analysis and lemmatization are not implemented.

### 5. No Relevance Ranking

The current system focuses on retrieval and phrase matching rather than
sophisticated ranking.

### 6. JSON Storage

JSON is useful for demonstrating the data structure, but
production-scale search systems generally use specialized index/storage
systems.

### 7. Basic Wikipedia Cleaning

The current markup-cleaning approach is sufficient for this academic
project but is not a production-grade parser for every possible
Wikipedia construct.

### 8. Processed-token Positions

Positions are assigned after preprocessing. Because stop words are
removed before indexing, positions represent the processed token
sequence rather than exact original word offsets in the raw Wikipedia
article.

------------------------------------------------------------------------

# 39. Future Improvements

## Telugu NLP

Possible improvements include:

-   Comprehensive Telugu stop-word list
-   Telugu stemming
-   Telugu lemmatization
-   Morphological analysis
-   Improved tokenization
-   Better handling of Telugu linguistic variations

## Search Ranking

The current system retrieves matching documents but does not implement
sophisticated relevance ranking.

Possible future ranking models:

### TF-IDF

Uses term frequency and inverse document frequency to estimate how
important a term is to a document.

### BM25

A widely used probabilistic ranking algorithm for Information Retrieval.

Future results could look like:

``` text
1. Article A — Score: 8.42
2. Article B — Score: 7.13
3. Article C — Score: 5.94
```

instead of simply returning matching documents.

## Search Features

Possible additions:

-   Boolean AND
-   Boolean OR
-   NOT queries
-   Wildcard search
-   Fuzzy search
-   Autocomplete
-   Query suggestions
-   Search snippets
-   Term highlighting
-   Ranked search results

## Evaluation

The system could be evaluated using:

``` text
Precision
Recall
F1-score
Mean Average Precision (MAP)
```

A manually prepared test collection could contain:

``` text
Query
Expected Relevant Documents
Retrieved Documents
```

and retrieval quality could then be measured quantitatively.

------------------------------------------------------------------------

# 40. IR Concepts Demonstrated

This project provides practical implementation of:

-   Information Retrieval
-   Document collection
-   Text preprocessing
-   Unicode normalization
-   Tokenization
-   Stop-word removal
-   Inverted indexing
-   Positional indexing
-   Posting lists
-   Candidate document intersection
-   Phrase searching
-   Position-based matching
-   Query processing
-   Search interfaces
-   Regional-language Information Retrieval

The most important concepts are:

``` text
Inverted Index:

Term → Documents
```

and:

``` text
Positional Inverted Index:

Term → Document → Positions
```

------------------------------------------------------------------------

# 41. Learning Outcomes

After studying this project, a reader should understand:

-   What Information Retrieval means.
-   Why search engines need indexes.
-   Why scanning every document for every query is inefficient.
-   What an inverted index is.
-   Why it is called an inverted index.
-   What a positional inverted index is.
-   Why term positions are needed for phrase searching.
-   How Wikipedia data can be converted into a searchable collection.
-   Why preprocessing is important.
-   Why Unicode normalization matters for Telugu.
-   How Telugu tokenization works.
-   Why stop words are removed.
-   How a positional index is constructed.
-   How candidate documents are identified.
-   How positional phrase matching works.
-   Why query and document preprocessing should be consistent.
-   How the Flask interface connects to the retrieval system.
-   How the complete indexing and retrieval pipeline works.

------------------------------------------------------------------------

# 42. Final Summary

The central idea of this project is:

> A large document collection should not be scanned from the beginning
> every time a user performs a search.

Instead, the collection is processed and indexed beforehand.

A normal inverted index stores:

``` text
Term → Documents
```

For example:

``` text
తెలుగు → [10, 25, 486, 637]
```

A positional inverted index adds the locations of those terms:

``` text
Term → Document → Positions
```

For example:

``` text
తెలుగు
    Document 486 → [1, 13, 143, 151]

భాష
    Document 486 → [2, 14, 144, 152]
```

This additional positional information allows the search engine to
determine whether `తెలుగు` and `భాష` occur consecutively.

Therefore, the system supports both:

``` text
Keyword Search
```

and:

``` text
Phrase Search
```

The complete project demonstrates this process using 10,000 Telugu
Wikipedia articles:

``` text
Telugu Wikipedia
      ↓
Article Extraction
      ↓
Wikipedia Markup Cleaning
      ↓
Unicode Normalization
      ↓
Telugu Tokenization
      ↓
Stop-word Removal
      ↓
Positional Inverted Index
      ↓
Query Processing
      ↓
Word / Phrase Retrieval
      ↓
Flask Search Interface
```

This project provides a practical foundation for understanding how
fundamental Information Retrieval systems work and how those concepts
can be applied to a regional Indian language such as Telugu.

------------------------------------------------------------------------

# 43. Author

**Vipul Chetan**

Computer Science and Engineering\
IIIT Sri City

------------------------------------------------------------------------

## Project Highlights

``` text
✓ Information Retrieval System
✓ Telugu Wikipedia Corpus
✓ 10,000 Wikipedia Articles
✓ Regional Language IR
✓ Unicode-Aware Processing
✓ Telugu Tokenization
✓ Telugu Stop-word Removal
✓ Inverted Index
✓ Positional Inverted Index
✓ Position-Based Phrase Search
✓ Candidate Document Intersection
✓ Query Preprocessing
✓ Flask Web Search Interface
✓ Terminal Search Interface
✓ Reproducible Indexing Pipeline
```

------------------------------------------------------------------------

## License

This project is intended for educational and academic purposes.
