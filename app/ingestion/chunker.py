def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 200,
) -> list[dict]:

    chunks = []

    chunk_index = 0

    for page in pages:

        text = page["text"].strip()

        if not text:
            continue

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                    "page_start": page["page"],
                    "page_end": page["page"],
                }
            )

            chunk_index += 1

            start += chunk_size - overlap

    return chunks