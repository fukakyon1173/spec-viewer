import json
from pathlib import Path

from PyPDF2 import PdfReader

PDF_PATH = Path("denki.pdf")
OUTPUT_PATH = Path("spec-index-denki.json")
PART_NAME = "電気編"


def main():
    if not PDF_PATH.exists():
        print(f"PDF が見つかりません: {PDF_PATH}")
        return

    print(f"PDF 読み込み開始: {PDF_PATH}")

    with PDF_PATH.open("rb") as f:
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        print(f"ページ数: {num_pages}")

        items = []

        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text = page.extract_text() or ""
            text = " ".join(text.split())

            item = {
                "id": f"denki-p{page_number + 1}",
                "part": PART_NAME,
                "chapter": "",
                "section": "",
                "page": page_number + 1,
                "text": text,
            }
            items.append(item)

    data = {"items": items}

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"書き出し完了: {OUTPUT_PATH} （{len(items)} 件）")


if __name__ == "__main__":
    main()
