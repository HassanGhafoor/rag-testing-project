from pathlib import Path

CORPUS_DIR = Path("corpus")


def load_documents():
    docs = []
    for path in sorted(CORPUS_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        source = path.relative_to(CORPUS_DIR).as_posix()
        docs.append({"source": source, "text": text})
    return docs


def chunk_by_section(doc):
    title = ""
    sections = []
    current_heading = "Introduction"
    current_lines = []

    for line in doc["text"].splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## "):
            if current_lines:
                sections.append((current_heading, current_lines))
            current_heading = line[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, current_lines))

    chunks = []
    for heading, body_lines in sections:
        body = "\n".join(body_lines).strip()
        if not body:
            continue
        chunks.append({
            "id": f"{doc['source']}::{len(chunks)}",
            "source": doc["source"],
            "section": heading,
            "text": f"{title} - {heading}\n\n{body}",
        })
    return chunks


if __name__ == "__main__":
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_by_section(doc))

    print(f"Documents: {len(docs)}")
    print(f"Chunks: {len(all_chunks)}")

    sizes = [len(c["text"]) for c in all_chunks]
    print(f"Chunk size (chars): min={min(sizes)}, max={max(sizes)}, avg={sum(sizes) // len(sizes)}")

    for c in all_chunks:
        if c["source"] == "handbook/benefits.md":
            print("\n" + "=" * 60)
            print(c["id"], "|", c["section"])
            print(c["text"][:300])