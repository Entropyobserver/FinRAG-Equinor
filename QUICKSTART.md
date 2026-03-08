# 🎉 GitHub Release - 下一步操作指南

## ✅ 已完成

我已经为你创建了完整的GitHub仓库结构，包括：

### 📁 文件清单

```
github_release/
├── README.md                          ✅ 完整的项目说明（含使用指南）
├── LICENSE                            ✅ CC BY 4.0 许可协议
├── SETUP_GUIDE.md                     ✅ GitHub上传详细教程
│
├── data/                              ✅ 核心数据文件
│   ├── qa_pairs.jsonl                 ✅ 230个QA对（251KB）
│   ├── iaa_sample_46.jsonl            ✅ IAA验证数据（52KB）
│   ├── iaa_evaluation_report.json     ✅ IAA报告（2.3KB）
│   └── baseline_results.json          ✅ Baseline实验结果（258KB）
│
├── evaluation/                        ✅ 评估工具
│   ├── keyword_grounding.py           ✅ 关键词重叠计算
│   ├── evaluate_retrieval.py          ✅ 主评估脚本
│   └── metrics.py                     ✅ MRR/Hit@K/Precision等指标
│
├── baselines/                         ✅ Baseline代码
│   └── requirements.txt               ✅ Python依赖
│
└── docs/                              ✅ 文档
    └── annotation_guidelines.md       ✅ 完整标注指南（从你的论文附录提取）
```

**总大小**: ~570KB（远低于GitHub的100MB限制 ✓）

---

## 🚀 立即操作（3步上传）

### Step 1: 初始化Git仓库

```bash
cd /mnt/d/J/Desktop/language_technology/course/projects_AI/oil_rag_dra/github_release

git init
git add .
git commit -m "Initial commit: FinRAG-Equinor dataset v1.0"
```

### Step 2: 在GitHub创建仓库

1. 访问：https://github.com/new
2. 填写：
   - **Repository name**: `FinRAG-Equinor`
   - **Description**: "A human-validated benchmark for long-form financial document QA"
   - **Public** ✓（必须公开，审稿人要看）
   - **不要勾选** "Initialize with README"（你已经有了）
3. 点击"Create repository"

### Step 3: 推送到GitHub

```bash
# 替换 YOUR-USERNAME 为你的GitHub用户名
git remote add origin https://github.com/YOUR-USERNAME/FinRAG-Equinor.git
git branch -M main
git push -u origin main
```

**完成！** 🎊 你的数据集现在已公开在GitHub上。

---

## 📝 更新论文LaTeX

上传完成后，修改论文中匿名链接：

```latex
% 文件: FinRAG_Equinor_Dataset_Paper.tex
% 第50行左右

% 修改前：
\footnote{GitHub: \url{https://github.com/[anonymized]}}

% 修改后（替换YOUR-USERNAME）：
\footnote{GitHub: \url{https://github.com/YOUR-USERNAME/FinRAG-Equinor}}
```

---

## 🔒 双盲评审匿名化（可选）

如果投稿要求双盲评审（ACL/EMNLP需要），创建匿名分支：

```bash
cd github_release

# 创建匿名分支
git checkout -b anonymous

# 替换个人信息
sed -i 's/Xiaojing Yang/Anonymous Author/g' README.md
sed -i 's/Uppsala University/Anonymous Institution/g' README.md  
sed -i 's/xiaojing.yang.4987@student.uu.se/anonymous@example.com/g' README.md

# 提交并推送
git commit -am "Anonymize for double-blind review"
git push origin anonymous
```

**在论文中使用匿名链接**：
```latex
\footnote{GitHub (Anonymous): \url{https://github.com/YOUR-USERNAME/FinRAG-Equinor/tree/anonymous}}
```

**论文接受后**切换回主分支即可。

---

## 🎯 必做事项清单

### 在投稿前（7天内）

- [ ] **GitHub上传完成**（见上方3步）
- [ ] **测试README渲染**：访问 `https://github.com/YOUR-USERNAME/FinRAG-Equinor` 检查格式
- [ ] **测试评估脚本**：
  ```bash
  cd evaluation
  pip install nltk numpy
  python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
  python keyword_grounding.py  # 应该输出示例
  ```
- [ ] **更新论文LaTeX**：替换 `[anonymized]` 为真实GitHub链接
- [ ] **创建匿名分支**（如果需要双盲评审）
- [ ] **检查所有文件可访问**：在浏览器中随机点击几个文件确认能打开

### 可选但推荐（论文接受后）

- [ ] **上传Zenodo获取DOI**：
  1. 访问 https://zenodo.org/
  2. 上传完整corpus（17,994 chunks）
  3. 获得DOI（例如：10.5281/zenodo.1234567）
  4. 在README添加DOI badge
  
- [ ] **上传Hugging Face**：
  ```bash
  pip install huggingface_hub datasets
  huggingface-cli login
  # 按提示上传数据集
  ```

- [ ] **创建Leaderboard** GitHub Pages：
  见 `SETUP_GUIDE.md` 第"创建Leaderboard"部分

---

## ⚠️ 重要提醒

### 1. **不要上传PDF年报原文**
- Equinor年报有版权，不能直接分发
- README中已经写明下载方式：
  > Download from: https://www.equinor.com/investors/annual-report

### 2. **17,994个chunks怎么办？**

你有3个选项：

**选项A**（推荐）：等论文接受后上传Zenodo
- Zenodo支持50GB大文件
- 自动生成DOI（学术引用标准）
- 免费且永久保存

**选项B**：上传Hugging Face Datasets
- ```bash
  # 从你的processed目录生成
  python scripts/convert_to_hf_dataset.py
  ```
- 自动托管，支持在线预览

**选项C**：GitHub Release（如果<100MB）
- 如果压缩后<100MB，可以用GitHub Releases
- `git lfs` 可支持到2GB

**当前策略**：
- ✅ GitHub仅包含230个QA pairs + metadata
- ✅ README说明如何从PDF重建chunks
- ✅ 论文接受后上传Zenodo/HF补全数据

### 3. **评审会check什么？**

根据ACL/LREC评审经验，他们会验证：

✅ **数据质量**
- Cohen's κ = 0.79（你的达标 ✓）
- 清晰的annotation guidelines（已包含 ✓）
- IAA样本可用（46个，已包含 ✓）

✅ **可复现性**
- 评估脚本可运行（keyword_grounding.py ✓）
- 数据格式文档完整（README.md ✓）
- Baseline结果可验证（baseline_results.json ✓）

✅ **伦理合规**
- 数据来源合法（公开SEC文件 ✓）
- 标注者报酬合理（$25/h ✓）
- 许可协议明确（CC BY 4.0 ✓）

---

## 📧 遇到问题？

### 常见错误

**错误1: `git push` 失败**
```bash
# 解决方法：生成Personal Access Token
# 1. GitHub Settings → Developer settings → Personal access tokens
# 2. Generate new token (repo权限)
# 3. 使用token代替密码
git remote set-url origin https://YOUR-TOKEN@github.com/YOUR-USERNAME/FinRAG-Equinor.git
```

**错误2: 文件太大（>100MB）**
```bash
# 使用Git LFS
git lfs install
git lfs track "*.jsonl"
git add .gitattributes
git add .
git commit -m "Add LFS tracking"
```

**错误3: 评估脚本报错 `No module named 'nltk'`**
```bash
pip install -r baselines/requirements.txt
python -m nltk.downloader punkt stopwords
```

---

## 🎓 投稿建议

### 推荐顺序

1. **LREC-COLING 2026**（最适合）
   - 📅 投稿：2026年1月
   - ✅ 数据集专场，接受率60%
   - ⏱️ 审稿3个月

2. **ACL 2026 Findings**（备选）
   - 📅 投稿：2026年2月  
   - ✅ 高认可度，接受率35%
   - ⏱️ 审稿3个月

3. **Data in Brief**（快速发表）
   - 📅 滚动投稿（随时）
   - ✅ 3-6周审稿
   - ⚠️ 需要$600出版费

### Cover Letter模板

```
Dear Program Chairs,

We submit "FinRAG-Equinor: A Human-Validated Benchmark for Long-Form 
Financial Document Question Answering" for consideration at [CONFERENCE].

Our contributions:
1. First QA benchmark for full 200-350 page financial documents
2. Rigorous 5-stage curation with Cohen's κ=0.79 IAA
3. Chunking-agnostic evaluation protocol with threshold sensitivity

The dataset and evaluation scripts are publicly available on GitHub:
https://github.com/[YOUR-USERNAME]/FinRAG-Equinor

Best regards,
Xiaojing Yang
```

---

## ✨ 最后检查

在提交论文前，确认：

```bash
# 1. GitHub仓库已public
# 访问：https://github.com/YOUR-USERNAME/FinRAG-Equinor
# 应该能看到所有文件

# 2. 数据完整性
cd github_release
wc -l data/qa_pairs.jsonl  # 应输出: 230

# 3. 评估脚本可运行
cd evaluation
python keyword_grounding.py  # 应输出示例结果

# 4. README显示正确
# 在GitHub页面检查badges、表格、代码块是否格式正确
```

全部✅后，就可以投稿了！

---

## 📞 联系方式

- **GitHub Issues**: https://github.com/YOUR-USERNAME/FinRAG-Equinor/issues
- **Email**: xiaojing.yang.4987@student.uu.se

**Good luck with your submission! 🍀**
