import pymupdf


def parse_pdf(pdf_bytes: bytes) -> list[dict]:

    document = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    pages = []

    for page_number, page in enumerate(
        document,
        start=1,
    ):

        text = page.get_text("text")

        pages.append(
            {
                "page": page_number,
                "text": text,
            }
        )

    document.close()

    return pages