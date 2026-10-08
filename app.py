from flask import (
    Flask,
    request,
    render_template_string
)

import json
import time

from preprocess import preprocess


app = Flask(__name__)


INDEX_FILE = "data/positional_index.json"
ARTICLES_FILE = "data/articles.json"


print("Loading positional index...")

with open(
    INDEX_FILE,
    "r",
    encoding="utf-8"
) as f:

    index = json.load(f)


print("Loading articles...")

with open(
    ARTICLES_FILE,
    "r",
    encoding="utf-8"
) as f:

    articles = json.load(f)


# Document ID → article information
documents = {
    str(article["id"]): article
    for article in articles
}


def single_word_search(word):

    if word not in index:
        return []

    return list(
        index[word].keys()
    )


def phrase_search(words):

    if not words:
        return []

    # Every word must exist
    for word in words:

        if word not in index:
            return []

    # Documents containing all terms
    candidate_docs = set(
        index[words[0]].keys()
    )

    for word in words[1:]:

        candidate_docs &= set(
            index[word].keys()
        )

    results = []

    for doc_id in candidate_docs:

        positions = set(
            index[words[0]][doc_id]
        )

        for word in words[1:]:

            next_positions = set(
                index[word][doc_id]
            )

            positions = {
                position + 1
                for position in positions
                if position + 1 in next_positions
            }

            if not positions:
                break

        if positions:

            results.append({
                "doc_id": doc_id,
                "match_positions": sorted(
                    positions
                )
            })

    return results


def get_word_positions(
    doc_id,
    words
):

    result = {}

    for word in words:

        if (
            word in index
            and doc_id in index[word]
        ):

            result[word] = (
                index[word][doc_id][:20]
            )

    return result


HTML = """
<!DOCTYPE html>

<html lang="te">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Telugu Wikipedia Search Engine
</title>


<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    font-family:
        "Nirmala UI",
        "Noto Sans Telugu",
        "Segoe UI",
        Arial,
        sans-serif;

    background: #f5f3ff;

    color: #29243d;
}


.container {

    max-width: 1000px;

    margin: auto;

    padding: 40px 20px;
}


.header {

    text-align: center;

    margin-bottom: 30px;
}


.header h1 {

    margin-bottom: 8px;

    font-size: 32px;
}


.header p {

    color: #6d6780;
}


.search-box {

    background: white;

    padding: 22px;

    border-radius: 16px;

    box-shadow:
        0 5px 20px
        rgba(50, 40, 80, 0.08);
}


form {

    display: flex;

    gap: 10px;
}


input {

    flex: 1;

    padding: 15px;

    font-size: 18px;

    border:
        1px solid #d9d4e8;

    border-radius: 10px;

    outline: none;
}


input:focus {

    border-color: #7c5cff;
}


button {

    padding: 15px 25px;

    border: none;

    border-radius: 10px;

    background: #7c5cff;

    color: white;

    font-size: 16px;

    cursor: pointer;
}


button:hover {

    background: #6748e8;
}


.stats {

    display: flex;

    gap: 15px;

    margin-top: 18px;

    flex-wrap: wrap;
}


.stat {

    background: #f0edff;

    padding: 10px 15px;

    border-radius: 8px;

    font-size: 14px;
}


.results {

    margin-top: 25px;
}


.result {

    background: white;

    margin-bottom: 14px;

    padding: 20px;

    border-radius: 12px;

    box-shadow:
        0 3px 12px
        rgba(50, 40, 80, 0.06);
}


.result h3 {

    margin-top: 0;

    color: #5b42c7;
}


.doc-id {

    color: #777;

    font-size: 13px;
}


.positions {

    margin-top: 12px;

    background: #f7f5ff;

    padding: 10px;

    border-radius: 8px;

    font-size: 14px;
}


.empty {

    background: white;

    padding: 25px;

    border-radius: 12px;

    text-align: center;
}


.badge {

    display: inline-block;

    background: #e8e3ff;

    color: #5942b8;

    padding: 5px 9px;

    border-radius: 6px;

    font-size: 13px;

    margin-bottom: 15px;
}


@media (max-width: 600px) {

    form {

        flex-direction: column;
    }

    button {

        width: 100%;
    }

    .header h1 {

        font-size: 25px;
    }

}

</style>

</head>


<body>

<div class="container">


<div class="header">

<h1>
తెలుగు వికీపీడియా శోధన
</h1>

<p>
Telugu Wikipedia Positional Inverted Index
</p>

</div>


<div class="search-box">


<form method="POST">


<input
    type="text"
    name="query"
    value="{{ query }}"
    placeholder="తెలుగు పదం లేదా పదబంధాన్ని నమోదు చేయండి..."
    autofocus
>


<button type="submit">
Search
</button>


</form>


<div class="stats">


<div class="stat">
📚 Documents: 10,000
</div>


<div class="stat">
🔤 Positional Index
</div>


<div class="stat">
🌐 Language: Telugu
</div>


</div>


</div>


{% if searched %}


<div class="results">


<div class="badge">

{{ search_type }}

</div>


<h2>
Search Results
</h2>


<p>

Query:

<strong>
{{ query }}
</strong>

</p>


<p>

Found

<strong>
{{ result_count }}
</strong>

document(s)

in

<strong>
{{ search_time }}
</strong>

seconds.

</p>


{% if results %}


{% for result in results %}


<div class="result">


<h3>

{{ result.title }}

</h3>


<div class="doc-id">

Document ID:
{{ result.doc_id }}

</div>


{% if result.positions %}


<div class="positions">


<strong>
Matching positions:
</strong>


{% for word, positions
   in result.positions.items() %}


<div>

{{ word }}
→
{{ positions }}

</div>


{% endfor %}


</div>


{% endif %}


</div>


{% endfor %}


{% else %}


<div class="empty">

<h3>
No documents found
</h3>

<p>
Try another Telugu word or phrase.
</p>

</div>


{% endif %}


</div>


{% endif %}


</div>

</body>

</html>
"""


@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    query = ""

    results = []

    searched = False

    search_type = ""

    search_time = 0

    result_count = 0


    if request.method == "POST":

        searched = True

        query = request.form.get(
            "query",
            ""
        ).strip()


        words = preprocess(query)


        start_time = time.perf_counter()


        if len(words) == 1:

            search_type = (
                "Inverted Index"
            )

            doc_ids = (
                single_word_search(
                    words[0]
                )
            )


            for doc_id in doc_ids[:50]:

                positions = {
                    words[0]:
                    index[words[0]][doc_id][:20]
                }


                results.append({

                    "doc_id": doc_id,

                    "title":
                        documents[doc_id]["title"],

                    "positions":
                        positions

                })


            result_count = len(doc_ids)


        elif len(words) > 1:

            search_type = (
                "Positional Inverted Index"
            )


            matches = phrase_search(
                words
            )


            for match in matches[:50]:

                doc_id = match["doc_id"]


                positions = (
                    get_word_positions(
                        doc_id,
                        words
                    )
                )


                results.append({

                    "doc_id": doc_id,

                    "title":
                        documents[doc_id]["title"],

                    "positions":
                        positions

                })


            result_count = len(matches)


        search_time = round(
            time.perf_counter()
            - start_time,
            6
        )


    return render_template_string(

        HTML,

        query=query,

        results=results,

        searched=searched,

        search_type=search_type,

        search_time=search_time,

        result_count=result_count

    )


if __name__ == "__main__":

    print()

    print("=" * 60)

    print(
        "TELUGU WIKIPEDIA SEARCH ENGINE"
    )

    print("=" * 60)

    print()

    print(
        "Open:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    app.run(
        debug=True
    )