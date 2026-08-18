from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: str


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> list[Chunk]:

    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    chunks = []

    current = ""
    chunk_number = 0

    for paragraph in paragraphs:

        
        # finish the current chunk if exceeds target
        if current and len(current) + len(paragraph) > chunk_size:

            chunks.append(
                Chunk(
                    text=current.strip(),
                    source=source,
                    chunk_id=f"{source}-{chunk_number}",
                )
            )

            chunk_number += 1

            # keep the end of the previous chunk
            overlap_text = current[-overlap:]

            current = overlap_text + "\n\n" + paragraph

        else:
            if current:
                current += "\n\n"

            current += paragraph

    if current.strip():
        chunks.append(
            Chunk(
                text=current.strip(),
                source=source,
                chunk_id=f"{source}-{chunk_number}",
            )
        )

    return chunks