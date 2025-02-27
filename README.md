# DocSearch (QueryRank): Intelligent Document Retrieval System

## 📌 Project Overview
This project implements an **Information Retrieval System** that indexes a collection of documents, performs searches using multiple ranking models, and evaluates results using **TREC evaluation metrics**. The system works with the **Cranfield dataset**, containing 1,400 research abstracts.

## 🚀 Features
- **Indexing:** Converts XML-based documents into a structured format.
- **Search & Ranking Models:**
  - **Vector Space Model (VSM)** using TF-IDF & Cosine Similarity.
  - **BM25 Model** for probabilistic ranking.
  - **Language Model (LM)** for query likelihood ranking.
- **Evaluation:** Outputs results in TREC format for performance assessment.

## 📂 Repository Structure
```
docsearch-queryrank/
│── datasets/                 # Contains dataset files
│   ├── cran.all.1400.xml     # Collection of documents
│   ├── cran.qry.xml          # Queries for retrieval
│   ├── cranqrel.trec.txt     # Relevance judgments
│   ├── cran_all.csv          # Processed documents
│   ├── cran_query.csv        # Processed queries
│── src/                      # Source code
│   ├── search_engine.py      # Main search engine script
│   ├── xmltocsv.py           # XML to CSV conversion script
│── results/                  # Stores search results
│   ├── VSM_output.txt        # VSM ranking output
│   ├── BM25_output.txt       # BM25 ranking output
│   ├── LM_output.txt         # LM ranking output
│── README.md                 # Project documentation
│── requirements.txt          # Dependencies
```

## 🛠 Installation & Setup
1. **Clone the repository:**
```bash
git clone https://github.com/muonorb/DocSearch-QueryRank.git
cd DocSearch-QueryRank
```
2. **Install dependencies:**
```bash
pip install -r requirements.txt
```
3. **Run XML to CSV conversion:**
```bash
python src/xmltocsv.py
```
4. **Run the search engine:**
```bash
python src/main.py
```

## 📈 Ranking Methods
### 1️⃣ Vector Space Model (VSM)
- Uses **TF-IDF weighting**.
- Computes **Cosine Similarity** between query and documents.

### 2️⃣ BM25 (Best Matching 25)
- A probabilistic ranking function.
- Uses **term frequency & inverse document frequency**.

### 3️⃣ Language Model (LM)
- Uses **Query Likelihood Model**.
- Computes probability of generating query from each document.

## 📊 Evaluation
The system generates ranked lists in **TREC format**, which can be evaluated using [trec_eval](https://github.com/terrierteam/jtreceval).

### 🏆 Running TREC Evaluation
To evaluate your search engine performance using trec_eval, follow these steps:
```bash
git clone https://github.com/usnistgov/trec_eval.git
cd trec_eval
make CC=clang
make CC=gcc
../trec_eval -m all_trec cranqrel.trec.txt BM25_output.txt
```


## 📝 License
This project is licensed under the MIT License.

