# GitHub Repository Setup Guide

## 📦 Preparing Files for Upload

### Step 1: Copy Core Data Files

```bash
cd /mnt/d/J/Desktop/language_technology/course/projects_AI/oil_rag_dra

# Copy QA pairs
cp data/test/gold_qa_230.jsonl github_release/data/qa_pairs.jsonl

# Copy IAA data (optional, for transparency)
cp data/test/iaa_sample_46.jsonl github_release/data/iaa_sample.jsonl
cp results/iaa_evaluation_report.json github_release/data/

# Copy evaluation results
cp results/03_chunking_evaluation/comparison_results.json github_release/data/baseline_results.json
```

### Step 2: Simplify Chunk Data

The full 17,994 chunks are too large for GitHub (>100MB). Two options:

**Option A**: Upload to Zenodo/Hugging Face (recommended)
```bash
# Create metadata file only
python scripts/create_chunk_metadata.py \
  --input data/processed/paragraphs/ \
  --output github_release/data/corpus_metadata.json
```

**Option B**: Create sample subset for GitHub
```bash
# Include first 1,000 chunks as example
python scripts/create_chunk_sample.py \
  --input data/processed/paragraphs/ \
  --output github_release/data/corpus_sample.jsonl \
  --num_samples 1000
```

### Step 3: Copy Evaluation Scripts

```bash
# Already created via previous steps
# - evaluation/keyword_grounding.py
# - evaluation/evaluate_retrieval.py
# - evaluation/metrics.py
```

### Step 4: Create Simple Baseline Example

```bash
# Copy simplified baseline from your existing scripts
cp scripts/03_evaluation/01_embedding_models/evaluate_dense_only.py \
   github_release/baselines/dense_retrieval.py
```

---

## 🔧 Local Testing Before Upload

### Test 1: Verify Data Format

```bash
cd github_release

# Check QA pairs format
head -n 3 data/qa_pairs.jsonl | python -m json.tool

# Count entries
wc -l data/qa_pairs.jsonl  # Should be 230
```

### Test 2: Run Evaluation Script

```bash
cd evaluation

# Create dummy predictions for testing
python -c "
import json
predictions = []
for i in range(10):
    predictions.append({
        'question_id': f'test_{i}',
        'retrieved_chunks': [
            {'chunk_id': 'chunk_1', 'text': 'Sample text', 'score': 0.9}
        ]
    })
with open('test_predictions.jsonl', 'w') as f:
    for pred in predictions:
        f.write(json.dumps(pred) + '\n')
"

# Run evaluation
python evaluate_retrieval.py \
  --predictions test_predictions.jsonl \
  --gold_data ../data/qa_pairs.jsonl \
  --threshold 0.60
```

### Test 3: Check README Rendering

```bash
# If you have grip installed
grip README.md --browser

# Or push to a test branch and view on GitHub
```

---

## 🚀 Creating GitHub Repository

### Step 1: Initialize Repository

```bash
cd github_release

git init
git add .
git commit -m "Initial commit: FinRAG-Equinor dataset"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `FinRAG-Equinor`
3. Description: "A human-validated benchmark for long-form financial document QA"
4. **Public** (required for paper submission)
5. Do NOT initialize with README (you already have one)

### Step 3: Push to GitHub

```bash
# Replace [YOUR-USERNAME] with your GitHub username
git remote add origin https://github.com/[YOUR-USERNAME]/FinRAG-Equinor.git
git branch -M main
git push -u origin main
```

---

## 📝 Post-Upload Checklist

### Update Paper LaTeX

In `FinRAG_Equinor_Dataset_Paper.tex`, replace:

```latex
% Before (anonymous)
\footnote{GitHub: \url{https://github.com/[anonymized]}}

% After (public)
\footnote{GitHub: \url{https://github.com/[YOUR-USERNAME]/FinRAG-Equinor}}
```

### Create DOI on Zenodo

1. Go to https://zenodo.org/
2. Click "New Upload"
3. Upload full corpus (17,994 chunks)
4. Fill metadata:
   - **Title**: FinRAG-Equinor Dataset
   - **Authors**: Xiaojing Yang
   - **Description**: (Copy from README)
   - **License**: CC BY 4.0
   - **Keywords**: question answering, financial documents, retrieval
5. Click "Publish" → Get DOI

### Update README with DOI

```bash
# Edit README.md
# Replace https://doi.org/10.XXXX/zenodo.XXXXXXX with actual DOI
```

---

## 🤗 Optional: Upload to Hugging Face

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create dataset
python -c "
from datasets import Dataset
import json

# Load QA pairs
with open('data/qa_pairs.jsonl') as f:
    data = [json.loads(line) for line in f]

# Create dataset
dataset = Dataset.from_list(data)
dataset.push_to_hub('[YOUR-USERNAME]/FinRAG-Equinor')
"
```

---

## 📊 Creating a Leaderboard (Optional)

### Option 1: GitHub Pages

```bash
# Create docs/ folder for GitHub Pages
mkdir -p docs
cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>FinRAG-Equinor Leaderboard</title>
</head>
<body>
    <h1>FinRAG-Equinor Leaderboard</h1>
    <table>
        <tr>
            <th>Model</th>
            <th>MRR@10</th>
            <th>Hit@10</th>
            <th>Paper</th>
        </tr>
        <tr>
            <td>E5-large-v2</td>
            <td>0.5803</td>
            <td>71.3%</td>
            <td><a href="#">Yang 2026</a></td>
        </tr>
    </table>
</body>
</html>
EOF

git add docs/
git commit -m "Add leaderboard"
git push
```

Enable GitHub Pages:
- Go to repository Settings → Pages
- Source: `main` branch, `/docs` folder
- Visit: https://[YOUR-USERNAME].github.io/FinRAG-Equinor/

---

## 🔒 Anonymization for Double-Blind Review

### Create Anonymous Mirror (Before Submission)

```bash
# Create anonymous branch
git checkout -b anonymous

# Replace identifiable information
sed -i 's/Xiaojing Yang/Anonymous Author/g' README.md
sed -i 's/Uppsala University/Anonymous Institution/g' README.md
sed -i 's/xiaojing.yang.4987@student.uu.se/anonymous@example.com/g' README.md

git commit -am "Anonymize for double-blind review"
git push origin anonymous
```

### In Paper Submission

Use anonymous link:
```latex
\footnote{GitHub (Anonymous): \url{https://github.com/[YOUR-USERNAME]/FinRAG-Equinor/tree/anonymous}}
```

### After Acceptance

Merge anonymous changes back and switch to `main`:
```bash
git checkout main
git push origin main
```

---

## 📧 Final Checklist

Before submitting paper:

- [ ] GitHub repository is public
- [ ] All data files uploaded (<100MB limit)
- [ ] README.md complete with badges
- [ ] LICENSE file added (CC BY 4.0)
- [ ] Evaluation scripts tested and documented
- [ ] Baseline results reproducible
- [ ] Anonymous branch created (if double-blind)
- [ ] DOI obtained from Zenodo (optional but recommended)
- [ ] Paper LaTeX updated with real GitHub link
- [ ] All [YOUR-USERNAME] placeholders replaced

---

## 🛠 Troubleshooting

### Problem: File >100MB

**Solution 1**: Use Git LFS
```bash
git lfs install
git lfs track "*.jsonl"
git add .gitattributes
```

**Solution 2**: Host on Zenodo
```bash
# Remove large files from git
git rm --cached data/corpus_full.jsonl

# Add link to README
echo "Download full corpus: https://zenodo.org/record/XXXXX" >> README.md
```

### Problem: Evaluation script fails

Check dependencies:
```bash
pip install -r baselines/requirements.txt
python -m nltk.downloader punkt stopwords
```

### Problem: Can't push to GitHub

Check authentication:
```bash
# Use SSH instead of HTTPS
git remote set-url origin git@github.com:[YOUR-USERNAME]/FinRAG-Equinor.git

# Or use personal access token
git remote set-url origin https://[TOKEN]@github.com/[YOUR-USERNAME]/FinRAG-Equinor.git
```

---

## 📞 Support

If issues persist:
- Open issue on GitHub: https://github.com/[YOUR-USERNAME]/FinRAG-Equinor/issues
- Email: xiaojing.yang.4987@student.uu.se
