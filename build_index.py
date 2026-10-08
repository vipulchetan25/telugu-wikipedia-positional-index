import json
import os
from collections import defaultdict

from preprocess import preprocess


INPUT_FILE = "data/articles.json"
OUTPUT_FILE = "data/positional_index.json"


def main():

    print("Loading articles...")

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        articles = json.load(f)

    print(
        f"Loaded {len(articles)} articles."
    )

    # term → document ID → positions
    index = defaultdict(
        lambda: defaultdict(list)
    )

    total_tokens = 0

    print()
    print(
        "Building positional inverted index..."
    )

    for article in articles:

        doc_id = str(article["id"])
        text = article["text"]

        # Apply complete preprocessing
        tokens = preprocess(text)

        total_tokens += len(tokens)

        # Positions start from 1
        for position, token in enumerate(
            tokens,
            start=1
        ):

            index[token][doc_id].append(
                position
            )

    # Convert defaultdict objects
    # to normal dictionaries
    index = {
        term: dict(postings)
        for term, postings in index.items()
    }

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            index,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("=" * 60)
    print("INDEX BUILDING COMPLETED")
    print("=" * 60)

    print(
        f"Documents       : {len(articles)}"
    )

    print(
        f"Total tokens    : {total_tokens}"
    )

    print(
        f"Unique terms    : {len(index)}"
    )

    print(
        f"Index saved to  : {OUTPUT_FILE}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()