# 📄 PDF Outline Extractor – Round 1A (Adobe India Hackathon 2025)

## 🧠 Overview

This tool extracts a structured outline (title, H1, H2, H3 headings with page numbers) from any PDF. It is optimized to run **fully offline**, within a **Docker container**, and meets all Round 1A constraints:

✅ CPU-only
✅ ≤ 200MB total footprint
✅ ≤ 10 seconds execution (per file)
✅ No internet access

---

## ⚙️ How It Works

### 🧩 Heading Detection Strategy

1. **Font Analysis**: Ranks font sizes to detect hierarchy.
2. **Title Detection**: Picks the largest and most centered text on page 1.
3. **Heading Classification**:

   * H1, H2, H3 based on font size + boldness
   * Uses layout and formatting to ensure accuracy
4. **Filtering**: Removes bullets, noise, and irrelevant text using regex.

---

## 🛠 Tech Stack

* **PyMuPDF (fitz)** – For extracting text, font styles, and layout
* **Python Standard Libraries** – `json`, `collections`, `re`, `os`, `glob`

---

## 📦 Project Structure

```
Round1A/
├── test.py            # PDF heading extraction logic
├── main.py            # Docker entrypoint
├── requirements.txt   # Python dependencies (PyMuPDF==1.23.8)
├── Dockerfile         # Container setup
├── README.md          # You're here!
├── input/             # Put PDF files here
└── output/            # Extracted .json files go here
```

---

## 🚀 Quick Start (No Setup Errors!)

### ✅ Prerequisites

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows, Linux, or macOS)
* Make sure Docker is **running**
* Create the following folders in the project directory:

  ```
  mkdir input output
  ```

> ⚠️ On **Windows (PowerShell)**, use `pwd` and **not** `$(pwd)` (see Run section below).

---

### 🧱 Step 1 – Build the Docker Image

```powershell
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

This will download Python 3.9-slim and install the required dependencies (`PyMuPDF==1.23.8`).

---

### ▶️ Step 2 – Run the Extractor

#### 🔸 On **Windows (PowerShell)**:

```powershell
docker run --rm ^
  -v ${PWD}/input:/app/input ^
  -v ${PWD}/output:/app/output ^
  --network none ^
  pdf-outline-extractor:latest
```

#### 🔸 On **Linux/macOS (bash)**:

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
```

---

### 📤 Output

* For each `yourfile.pdf` in `/input`, you'll get `yourfile.json` in `/output`
* JSON structure:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Section Header",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Subsection Header",
      "page": 2
    }
  ]
}
```

---

## ✅ Constraints Met

| Requirement       | Status                   |
| ----------------- | ------------------------ |
| Architecture      | ✅ AMD64                  |
| Offline Execution | ✅ No network access      |
| Speed             | ✅ ≤ 10s for 50-page PDFs |
| File Size         | ✅ Under 200MB total      |
| CPU Only          | ✅ No GPU needed          |
| Valid JSON Output | ✅ As per spec            |

---

## 🧪 Tested With

* Text-based PDFs
* Scanned/image-heavy PDFs (graceful fallback)
* Japanese and multilingual PDFs
* Technical papers, forms, brochures, etc.

---

## 🛡️ Error Handling

* Skips unreadable/malformed PDFs (doesn't crash)
* Validates input format
* Outputs detailed logs inside the container
* Keeps running even if one file fails

---

## 🤝 Contributing / Troubleshooting

* If you see Docker errors like `invalid reference format`, check that you are using the correct syntax for your shell (PowerShell vs Bash).
* For permission issues, ensure Docker Desktop has access to the `input/` and `output/` folders.
* If Docker fails to build, verify your internet connection during the build phase (it pulls base images only once).

---

## 👨‍💻 Developed For

**Adobe India Hackathon 2025 – Round 1A: PDF Structural Outline Extraction**
By: *[Triple Byte]*

---
