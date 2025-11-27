import json
from pathlib import Path

from PyPDF2 import PdfReader

# ===== 設定 =====
# このスクリプトと同じフォルダにある PDF 名
PDF_PATH = Path("kenchiku.pdf")

# 出力する JSON ファイル名
OUTPUT_PATH = Path("spec-index-kenchiku.json")

# part は編名（建築編で固定）
PART_NAME = "建築編"


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
            text = " ".join(text.split())  # 改行の整理

            item = {
                "id": f"kenchiku-p{page_number + 1}",
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
