# 🚀 立即上传到 GitHub

## ✅ 已准备就绪的文件

```
github_release/
├── data/
│   ├── qa_pairs.jsonl (251KB) - 230个QA pairs
│   ├── iaa_sample_46.jsonl (52KB) - IAA验证样本
│   ├── iaa_evaluation_report.json (2.3KB) - Cohen's κ报告
│   └── baseline_results.json (258KB) - 7种chunking策略结果
├── evaluation/
│   ├── keyword_grounding.py - 关键词重叠评估
│   ├── evaluate_retrieval.py - 主评估脚本
│   └── metrics.py - IR指标计算
├── baselines/
│   └── requirements.txt - Python依赖
├── docs/
│   └── annotation_guidelines.md - 完整标注规范
├── README.md - 项目文档
├── LICENSE - CC BY 4.0
└── QUICKSTART.md - 快速开始

总大小: ~620KB ✅ (GitHub限制100MB)
```

---

## 📝 第1步：初始化Git仓库

```bash
cd /mnt/d/J/Desktop/language_technology/course/projects_AI/oil_rag_dra/github_release

git init
git add .
git commit -m "Initial release: FinRAG-Equinor v1.0 - 230 QA pairs, Cohen's κ=0.79"
```

---

## 🌐 第2步：在GitHub上创建仓库

1. 访问: https://github.com/new
2. 填写信息:
   - **Repository name**: `FinRAG-Equinor`
   - **Description**: `A human-validated benchmark for long-form financial document QA (230 QA pairs, 17,994 chunks, Cohen's κ=0.79)`
   - **Public** ✅ (必须public，审稿人要访问)
   - **不要** 勾选 "Add a README file"
3. 点击 **Create repository**

---

## 📤 第3步：推送到GitHub

```bash
git remote add origin https://github.com/Entropyobserver/FinRAG-Equinor.git
git branch -M main
git push -u origin main
```

**完成后访问**: https://github.com/Entropyobserver/FinRAG-Equinor

---

## 📄 第4步：更新论文LaTeX

在你的 `FinRAG_Equinor_Dataset_Paper.tex` 文件中：

**找到这一行** (大约第90行):
```latex
The dataset is publicly available\footnote{GitHub: \url{https://github.com/[anonymized]}}
```

**替换为**:
```latex
The dataset is publicly available\footnote{GitHub: \url{https://github.com/Entropyobserver/FinRAG-Equinor}}
```

---

## ✅ 第5步：验证上传

检查以下内容在GitHub上显示正常：

- [ ] README.md正确渲染（表格、徽章显示）
- [ ] data/qa_pairs.jsonl有230行
- [ ] 所有Python脚本可以点击查看
- [ ] LICENSE文件存在

测试脚本可运行：
```bash
cd evaluation
python keyword_grounding.py  # 应输出3个示例
```

---

## 🎯 关于17,994个chunks

**现在不上传完整chunks**。README中已说明：

```markdown
## Data Access

### QA Pairs
The 230 expert-validated QA pairs are available in `data/qa_pairs.jsonl`.

### Full Corpus Chunks
Due to size constraints, the full 17,994 text chunks will be released via Zenodo upon paper acceptance.  
To reproduce chunking from original PDFs:
1. Download Equinor annual reports (2010–2024) from https://www.equinor.com/investors/annual-report
2. Run our preprocessing script (coming soon)
```

**投稿论文时这样写就够了**。审稿人主要看：
1. ✅ 230个QA pairs公开
2. ✅ 评估脚本完整
3. ✅ Annotation guidelines详细
4. ✅ 承诺论文接收后提供完整数据

**论文接收后**，再上传17,994个chunks到Zenodo（免费，50GB限制），获得DOI。

---

## 🔐 双盲审稿怎么办？

如果投**ACL/EMNLP**(需要double-blind)，创建匿名分支：

```bash
cd /mnt/d/J/Desktop/language_technology/course/projects_AI/oil_rag_dra/github_release
git checkout -b anonymous
```

替换README.md中的识别信息：
```bash
sed -i 's/Xiaojing Yang/Anonymous Author/g' README.md
sed -i 's/Uppsala University/Anonymous Institution/g' README.md
sed -i 's/xiaojing.yang.4987@student.uu.se/anonymous@example.com/g' README.md
git commit -am "Anonymize for double-blind review"
git push origin anonymous
```

然后在论文里用匿名分支URL：
```latex
\footnote{GitHub: \url{https://github.com/Entropyobserver/FinRAG-Equinor/tree/anonymous}}
```

**但如果投LREC-COLING**（single-blind），直接用主分支：
```latex
\footnote{GitHub: \url{https://github.com/Entropyobserver/FinRAG-Equinor}}
```

---

## 📧 需要帮助？

如果遇到问题：

1. **Git push失败** (Authentication failed):
   ```bash
   # 使用Personal Access Token
   git remote set-url origin https://Entropyobserver:<YOUR_TOKEN>@github.com/Entropyobserver/FinRAG-Equinor.git
   ```
   在https://github.com/settings/tokens生成token

2. **文件太大** (unlikely, 你只有620KB):
   - GitHub单文件限制100MB，你完全OK

3. **Python脚本不运行**:
   ```bash
   pip install nltk numpy
   python -m nltk.downloader punkt stopwords
   ```

---

## 🎉 完成！

上传完成后：
1. ✅ 更新LaTeX论文的GitHub链接
2. ✅ 编译PDF，确认链接可点击
3. ✅ 提交论文到LREC-COLING 2026 (推荐) 或 ACL 2026

**你的GitHub**: https://github.com/Entropyobserver/FinRAG-Equinor

审稿人会看到：
- ✅ 专业的README（表格、徽章、示例代码）
- ✅ 完整的230个QA pairs
- ✅ 可复现的评估脚本
- ✅ 详细的annotation guidelines
- ✅ IAA验证数据（κ=0.79）

**这就是top-tier数据集论文的标准！** 🚀
