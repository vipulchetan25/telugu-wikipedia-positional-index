import json

from preprocess import preprocess


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


# Document ID → article title
doc_titles = {
    str(article["id"]): article["title"]
    for article in articles
}


def single_word_search(word):
    """
    Search for a single word using
    the inverted index.
    """

    if word not in index:
        return []

    return list(
        index[word].keys()
    )


def and_search(words):
    """
    Return documents containing
    all query words.
    """

    if not words:
        return []

    document_sets = []

    for word in words:

        if word not in index:
            return []

        document_sets.append(
            set(index[word].keys())
        )

    result = document_sets[0]

    for docs in document_sets[1:]:

        result = result.intersection(
            docs
        )

    return list(result)


def phrase_search(words):
    """
    Positional phrase search.

    Example:

    తెలుగు భాష

    If:

    తెలుగు → position 10
    భాష   → position 11

    then the phrase matches.
    """

    if not words:
        return []

    # Every query term must exist
    for word in words:

        if word not in index:
            return []

    # Find documents containing
    # all query terms
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

            results.append(doc_id)

    return results


def display_results(doc_ids):

    if not doc_ids:

        print(
            "\nNo documents found."
        )

        return

    print(
        f"\nFound {len(doc_ids)} document(s):\n"
    )

    # Display maximum 20 results
    for i, doc_id in enumerate(
        doc_ids[:20],
        start=1
    ):

        title = doc_titles.get(
            doc_id,
            "Unknown title"
        )

        print(
            f"{i}. [{doc_id}] {title}"
        )

    if len(doc_ids) > 20:

        print(
            f"\n... and "
            f"{len(doc_ids) - 20} more results."
        )


def main():

    print()
    print("=" * 60)
    print(
        "TELUGU WIKIPEDIA SEARCH ENGINE"
    )
    print("=" * 60)

    print(
        "Enter a Telugu word or phrase."
    )

    print(
        "Type 'exit' to stop."
    )

    while True:

        query = input(
            "\nEnter query: "
        ).strip()

        if query.lower() == "exit":

            print("Goodbye!")

            break

        words = preprocess(query)

        if not words:

            print(
                "No searchable Telugu terms found."
            )

            continue

        print(
            f"Tokens: {words}"
        )

        # Single word
        if len(words) == 1:

            results = single_word_search(
                words[0]
            )

            print(
                "\nSearch type: "
                "Inverted Index"
            )

        # Multiple words
        else:

            results = phrase_search(
                words
            )

            print(
                "\nSearch type: "
                "Positional Inverted Index"
            )

        display_results(results)


if __name__ == "__main__":
    main()