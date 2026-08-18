from pathlib import Path

from pypdf import PdfReader

from .chunking import Chunk, chunk_text


def read_file(path: Path) -> str:

    if path.suffix.lower() in [".txt", ".md"]:
        return path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".pdf":

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)

    raise ValueError(
        f"Unsupported file type: {path.suffix}"
    )


def ingest_directory(
    directory: str,
) -> list[Chunk]:

    directory_path = Path(directory)

    all_chunks = []

    for path in directory_path.iterdir():

        if not path.is_file():
            continue

        if path.suffix.lower() not in [
            ".txt",
            ".md",
            ".pdf",
        ]:
            continue

        print(f"Processing {path.name}")

        text = read_file(path)

        chunks = chunk_text(
            text=text,
            source=path.name,
        )

        all_chunks.extend(chunks)

        print(
            f"  created {len(chunks)} chunks"
        )

    return all_chunks