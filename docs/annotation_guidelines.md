# Annotation Guidelines - FinRAG-Equinor

## Overview

This document provides the complete annotation protocol used in Stage 3 (Human Validation) and Stage 5 (Inter-Annotator Agreement Study) of the FinRAG-Equinor dataset construction.

---

## 1. Question Quality Criteria

All questions must satisfy **four requirements** to be included in the dataset:

### 1.1 Clarity
- ✅ No ambiguous pronouns (e.g., "it", "they", "the company" without clear referent)
- ✅ No undefined entities (all entities must be explicitly named or clearly referenced)
- ✅ Self-contained questions that can be understood without additional context

**Example**:
- ❌ Bad: "What was the revenue in that year?"  
- ✅ Good: "What was Equinor's revenue in 2023?"

### 1.2 Answerability
- ✅ Can be answered from the specified annual report
- ✅ Does not require external knowledge beyond the document
- ✅ Has a clear, verifiable answer (not opinion-based)

**Example**:
- ❌ Bad: "Do you think Equinor's strategy is good?" (opinion-based)
- ✅ Good: "What is Equinor's stated strategy for renewable energy?"

### 1.3 Specificity
- ✅ Includes year constraints where relevant (e.g., "According to the 2023 report...")
- ✅ Specifies the metric or entity being asked about
- ✅ Avoids overly broad questions

**Example**:
- ❌ Bad: "What is the company's financial performance?"  
- ✅ Good: "What was Equinor's operating income in Q4 2023?"

### 1.4 Non-triviality
- ✅ Requires more than keyword lookup
- ✅ Tests understanding of financial concepts or document structure
- ✅ Discriminative (not all questions should be equally easy)

**Example**:
- ❌ Bad: "What company is this report about?" (trivial)
- ✅ Good: "According to the 2020 report, what is the relationship between Net Debt Ratio and dividend policy?"

---

## 2. Answer Extraction Protocol

Answers should follow these principles:

### 2.1 Minimality
- ✅ Include **only** information directly addressing the question
- ❌ Do not include extraneous context or background information
- ✅ Remove redundant phrases

**Example**:
- **Question**: "What was Equinor's CAPEX in 2023?"
- ❌ Bad answer: "In 2023, Equinor continued its investment strategy with a focus on low-carbon projects, and the capital expenditure (CAPEX) was $15.2 billion."
- ✅ Good answer: "$15.2 billion"

### 2.2 Verbatim Extraction (Where Possible)
- ✅ Extract exact text from the document rather than paraphrasing
- ✅ Preserve original wording, numbers, and units
- ⚠️ Exception: When the document contains pronouns, resolve them for clarity

**Example**:
- **Document text**: "The company reported operating income of $5.2B in Q4. This represented a 12% increase."
- **Question**: "What was the company's operating income in Q4?"
- ✅ Good answer: "$5.2B" (or "$5.2 billion", both acceptable)

### 2.3 Self-Contained Answers
- ✅ Answers should be readable without document context
- ✅ Resolve pronouns (e.g., "it" → "Equinor")
- ✅ Expand acronyms on first use (e.g., "CAPEX (Capital Expenditure)")

**Example**:
- **Document**: "The project achieved first oil in 2023. It is expected to produce 100,000 boe/day."
- **Question**: "What is the expected production from the project mentioned?"
- ❌ Bad: "It is expected to produce 100,000 boe/day" (pronoun unclear)
- ✅ Good: "The project is expected to produce 100,000 boe/day"

### 2.4 Completeness
- ✅ Include all necessary qualifiers (units, time periods, conditions)
- ✅ Do not omit critical context that changes the meaning

**Example**:
- **Question**: "What was the effective tax rate?"
- ❌ Bad: "15%" (missing context)
- ✅ Good: "15% for ordinary taxable income in 2023"

---

## 3. Evidence Paragraph Selection

For each question-answer pair, annotators must mark **all relevant evidence paragraphs**.

### 3.1 Inclusion Criteria
- ✅ Mark **all paragraphs** that contribute to the answer
- ✅ Include paragraphs even if only **one sentence** is relevant
- ✅ For multi-hop questions, ensure **all reasoning steps** are covered

**Example**:
- **Question**: "What is the relationship between Net Debt Ratio and dividend policy?"
- **Evidence paragraphs**:
  1. Paragraph defining Net Debt Ratio
  2. Paragraph stating the target ratio (15–30%)
  3. Paragraph explaining dividend policy
  4. Paragraph linking debt management to dividend decisions

### 3.2 Multi-Hop Question Handling
- ✅ Identify and mark **all intermediate reasoning steps**
- ✅ Ensure each "hop" has supporting evidence

**Example**:
- **Question**: "According to the 2020 report, what emissions reduction targets were set, and what technologies were mentioned?"
- **Required evidence**:
  1. Paragraph stating emissions reduction targets (e.g., "50% by 2030")
  2. Paragraph discussing Carbon Capture and Storage (CCS)
  3. Paragraph mentioning electrification of offshore platforms

**Average Evidence Paragraphs**:
- Single-hop questions: 1.68 ± 0.84 paragraphs
- Multi-hop questions: 2.13 ± 0.73 paragraphs

---

## 4. Inter-Annotator Agreement Study

To validate annotation quality, we conducted an IAA study on **46 randomly sampled QA pairs** (20% of the dataset).

### 4.1 Evaluation Dimensions

Two independent annotators evaluated each QA pair on three dimensions:

#### Dimension 1: Correctness
**Question**: Does the extracted answer accurately reflect the document content?

- ✅ **Yes**: Answer is factually correct and supported by evidence
- ❌ **No**: Answer contains errors, misinterpretations, or unsupported claims

**Result**: Cohen's κ = **0.88** (Almost Perfect)

#### Dimension 2: Completeness
**Question**: Does the answer contain all necessary information, and nothing extraneous?

- ✅ **Yes**: Answer is complete and minimal
- ⚠️ **Partial**: Answer is too verbose or missing minor details
- ❌ **No**: Answer is incomplete or contains irrelevant information

**Result**: Cohen's κ = **0.48** (Moderate)  
**Note**: Moderate agreement reflects inherent subjectivity in judging answer scope.

#### Dimension 3: Answerability
**Question**: Is the question answerable from the provided evidence paragraphs?

- ✅ **Yes**: Evidence paragraphs contain sufficient information
- ❌ **No**: Question requires additional paragraphs or external knowledge

**Result**: Cohen's κ = **1.00** (Perfect)

### 4.2 Overall Agreement
**Cohen's κ = 0.79** (Substantial Agreement)

This meets the threshold for reliable annotation quality in NLP benchmarks.

---

## 5. Disagreement Resolution

When annotators disagreed:

1. **Initial Round**: Two annotators independently evaluate
2. **Flagging**: Disagreements are automatically flagged
3. **Consensus Discussion**: Third expert annotator reviews and facilitates discussion
4. **Final Decision**: Majority vote or expert adjudication

### 5.1 Common Disagreement Patterns

| **Pattern** | **Resolution Strategy** |
|-------------|------------------------|
| Answer verbosity (Completeness) | Prefer minimal answer, include qualifier in separate field |
| Paragraph boundary (Evidence) | Include if ≥1 sentence is relevant |
| Difficulty classification | Use objective criteria (# hops, # entities, # constraints) |

---

## 6. Special Cases

### 6.1 Numerical Questions
- ✅ Include **unit** (e.g., "$5.2 billion", not "5.2")
- ✅ Include **time period** (e.g., "in Q4 2023")
- ✅ Preserve original formatting (e.g., "15%" not "0.15")

### 6.2 Multi-Hop Questions
- ✅ Mark flag `"requires_multiple_paragraphs": true`
- ✅ List all relevant paragraph IDs in `"gold_paragraph_ids"`
- ✅ Ensure answer synthesizes information (not just concatenation)

### 6.3 Comparative Questions
- ✅ Include both comparands (e.g., "2022: $10B, 2023: $12B")
- ✅ State the comparison result explicitly (e.g., "increased by 20%")

### 6.4 Definitional Questions
- ✅ Extract verbatim definition from document
- ✅ Include calculation formula if provided (e.g., "ROACE = Net Income / Average Capital Employed")

---

## 7. Annotation Interface

Annotators used a custom web-based interface with:

1. **PDF Viewer**: Full annual report with highlighting
2. **Question Panel**: Displays candidate question
3. **Answer Editor**: Text box for extracting answer
4. **Paragraph Selector**: Multi-select checkboxes for evidence paragraphs
5. **Validation Buttons**: Accept / Reject / Revise

---

## 8. Quality Control Metrics

| **Metric** | **Value** |
|------------|-----------|
| Total candidates reviewed | 300 |
| Accepted (as-is) | 97 (32.3%) |
| Accepted (with modifications) | 168 (56.0%) |
| Rejected | 132 (44.0%) |
| Questions refined for clarity | 71 (42.3% of accepted) |
| Answers corrected for errors | 58 (34.5% of accepted) |

---

## 9. Annotator Training

Before annotation, both annotators completed:

1. **Tutorial**: 2-hour training session on financial document structure
2. **Practice Set**: 20 example annotations with feedback
3. **Calibration**: Joint review of 10 cases to align standards
4. **Qualification Test**: Must achieve κ > 0.70 on 10 test cases

---

## 10. Compensation and Ethics

- **Hourly Rate**: $25/hour (above local minimum wage)
- **Total Hours**: ~120 hours (60 hours per annotator)
- **Consent**: All participants provided informed consent
- **Authorship**: Annotators offered co-authorship for contributed questions

---

## 11. Example Annotations

### Example 1: Numerical Extraction

**Question**: "According to the 2018 report, what was Equinor's total equity production in mboe per day?"

**Answer**: "2,083 mboe per day"

**Evidence**: Section "Operational Summary", paragraph 3

**Difficulty**: Easy

**Query Type**: `numerical_exact`

---

### Example 2: Causal Reasoning

**Question**: "What factors drove the increase in operating income in Q4 2018?"

**Answer**: "Increased production from Johan Sverdrup field and higher oil prices averaging $71/barrel."

**Evidence**: Section "Financial Results", paragraphs 7–8 (2 paragraphs)

**Difficulty**: Medium

**Query Type**: `reason_why`

---

### Example 3: Multi-Hop Reasoning (Hard)

**Question**: "What is the relationship between the Net Debt Ratio and the company's dividend policy as discussed in the 2020 report?"

**Answer**: "The company maintains a Net Debt Ratio target of 15–30% to support a competitive and progressive dividend policy, aiming for annual dividend growth subject to cash flow stability."

**Evidence**: 
- Section "Financial Strategy", paragraph 4 (Net Debt Ratio definition)
- Section "Dividend Policy", paragraphs 2–3 (dividend strategy)

**Requires Multiple Paragraphs**: `true`

**Difficulty**: Hard

**Query Type**: `other`

---

## 12. Contact

For questions about annotation guidelines, please contact:
- **Author**: Xiaojing Yang
- **Email**: xiaojing.yang.4987@student.uu.se
