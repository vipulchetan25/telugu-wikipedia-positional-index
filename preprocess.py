import re
import unicodedata


# Common Telugu stop words.
# These words usually carry little value for information retrieval.
TELUGU_STOPWORDS = {
    "అది",
    "అది కూడా",
    "అయితే",
    "అందుకు",
    "అందులో",
    "అక్కడ",
    "అక్కడి",
    "అని",
    "అనేది",
    "అనేవి",
    "అన్న",
    "అన్ని",
    "అవును",
    "ఇది",
    "ఇది కూడా",
    "ఇక్కడ",
    "ఇక్కడి",
    "ఇలా",
    "ఇవి",
    "ఉంది",
    "ఉన్న",
    "ఉన్నారు",
    "ఎందుకు",
    "ఎక్కడ",
    "ఎక్కడి",
    "ఏది",
    "ఏమి",
    "ఏమిటి",
    "కాదు",
    "కావచ్చు",
    "కోసం",
    "కు",
    "తో",
    "దాని",
    "దీనిని",
    "దీనికి",
    "నుండి",
    "మరి",
    "మరియు",
    "మాత్రమే",
    "పై",
    "లో",
    "వద్ద",
    "వంటి",
    "వల్ల",
    "సహా",
    "కూడా",
    "చాలా",
    "గా",
    "ను",
    "ని",
    "న",
    "లు",
    "గా",
    "కు",
    "తో",
    "లో",
}


def normalize_text(text):
    """
    Normalize Unicode and whitespace.
    """

    # Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)

    # Replace different whitespace characters
    # with normal spaces.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """
    Normalize text and extract Telugu tokens.
    """

    text = normalize_text(text)

    # Telugu Unicode block: U+0C00 - U+0C7F
    tokens = re.findall(r"[\u0C00-\u0C7F]+", text)

    return tokens


def preprocess(text):
    """
    Complete preprocessing pipeline.

    Returns:
        List of normalized Telugu tokens
        with stop words removed.
    """

    tokens = tokenize(text)

    processed_tokens = [
        token
        for token in tokens
        if token not in TELUGU_STOPWORDS
    ]

    return processed_tokens