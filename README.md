# Telugu Wikipedia Positional Inverted Index

An Information Retrieval system that builds a positional inverted index
from Telugu Wikipedia articles and supports Telugu word and phrase search.

## Dataset

The project uses the Telugu Wikipedia articles dataset provided by Wikimedia.

A subset of 10,000 Telugu Wikipedia articles was extracted from the
Wikipedia XML dump for this implementation.

The original Wikipedia dump is not included in this repository because
of its large size.

## Dataset Statistics

- Documents: 10,000
- Language: Telugu
- Dataset source: Telugu Wikipedia
- Index type: Positional Inverted Index

## Preprocessing

The following preprocessing operations are performed:

1. Wikipedia markup removal
2. Unicode NFC normalization
3. Whitespace normalization
4. Telugu tokenization
5. Telugu stop-word removal

The same preprocessing pipeline is applied to both documents and
user queries.

## Positional Inverted Index

The index stores:

```text
term → document ID → positions
```
