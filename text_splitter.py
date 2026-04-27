from langchain_text_splitters import RecursiveCharacterTextSplitter


with open("temp/intro_pdf_text.txt", "r") as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", " "],
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    with open(f"temp/chunk_{i}.txt", "w") as f:
        f.write(chunk)
