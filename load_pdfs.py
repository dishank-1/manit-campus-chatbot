
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

# Folder containing campus PDF documents
DATA_DIR = Path("data")


def load_pdfs():
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDFs found in the data folder.")
        print("Add at least one PDF and run this script again.")
        return []

    all_documents = []

    for pdf_path in pdf_files:
        print(f"\nLoading: {pdf_path.name}")

        try:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()

            for document in documents:
                # Keep track of where each page came from
                document.metadata["source"] = pdf_path.name

            all_documents.extend(documents)

            print(f"Pages loaded: {len(documents)}")

        except Exception as error:
            print(f"Could not load {pdf_path.name}: {error}")

    return all_documents


if __name__ == "__main__":
    documents = load_pdfs()

    print("\n========== SUMMARY ==========")
    print(f"Total pages loaded: {len(documents)}")

    if documents:
        print("\nFirst page metadata:")
        print(documents[0].metadata)

        print("\nFirst 1000 characters:")
        print(documents[0].page_content[:1000])
