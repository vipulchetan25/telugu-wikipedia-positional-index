import re
import unicodedata


# Common Telugu stop words.
# These words generally carry less information for
# information retrieval.
TELUGU_STOPWORDS = {
    "అది",
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
    "చాలా",
    "గా",
    "ను",
    "ని",
    "న",
    "లు",
}


def normalize_text(text):
    """
    Perform Unicode and whitespace normalization.
    """

    # Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text):
    """
    Normalize the text and extract Telugu tokens.

    Telugu Unicode block:
    U+0C00 - U+0C7F
    """

    text = normalize_text(text)

    tokens = re.findall(
        r"[\u0C00-\u0C7F]+",
        text
    )

    return tokens


def preprocess(text):
    """
    Complete preprocessing pipeline.

    Steps:
    1. Unicode normalization
    2. Whitespace normalization
    3. Telugu tokenization
    4. Stop-word removal
    """

    tokens = tokenize(text)

    processed_tokens = [
        token
        for token in tokens
        if token not in TELUGU_STOPWORDS
    ]

    return processed_tokens