# Integrated Evaluation Report — Module 7

## Section 1: Comparison Table

| Task                                                      | Approach                          | Model                                 | Training Cost           | Inference Cost   | Quality Metric              | Value                                                                                            |
| --------------------------------------------------------- | --------------------------------- | ------------------------------------- | ----------------------- | ---------------- | --------------------------- | ------------------------------------------------------------------------------------------------ |
| Sentiment classification (Lab 7A)                         | Fine-tuning                       | DistilBERT                            | ~30 min CPU + 3K labels | ~50 ms / example | Macro-F1                    | 0.6303                                                                                           |
| Domain transfer of fine-tuned classifier (Integration 7A) | Fine-tuned model on out-of-domain | DistilBERT                            | Already trained         | ~50 ms / example | Domain-shift judgment       | Moderate to severe domain shift observed; predictions became less reliable on tech-news articles |
| Extractive QA (Lab 7B)                                    | Pre-trained inference             | distilbert-base-cased-distilled-squad | 0                       | ~50 ms / example | EM / token-F1               | 0.344 / 0.4611                                                                                   |
| Abstractive summarization (Integration 7B)                | Pre-trained inference             | sshleifer/distilbart-cnn-6-6          | 0                       | ~3 sec / example | ROUGE-1 / ROUGE-2 / ROUGE-L | 0.3689 / 0.1589 / 0.2661                                                                         |

---

## Section 2: Findings

* Fine-tuning DistilBERT for sentiment classification achieved a macro-F1 of 0.6303, demonstrating that task-specific training improves performance when labeled data is available.
* The fine-tuned sentiment classifier showed visible domain-shift degradation when applied to tech-news articles because it was originally trained on app reviews rather than informational news text.
* The pre-trained QA model achieved 0.344 exact match and 0.4611 token-F1, indicating that it often generated partially correct answers even when exact spans were missed.
* The DistilBART summarizer achieved ROUGE-1 0.3689, ROUGE-2 0.1589, and ROUGE-L 0.2661 without any additional training.
* Pre-trained inference provided useful QA and summarization capabilities at zero training cost, making it practical when labeled datasets are unavailable.

---

## Section 3: Faithfulness Check (Qualitative)

### High-ROUGE Example — NEWS_0079

ROUGE Scores:

* ROUGE-1: 0.643
* ROUGE-2: 0.390
* ROUGE-L: 0.619

Observation:
The generated summary closely matched the reference summary and preserved the main factual claims from the article. The summary was faithful because all major details appeared in the source article. In this case, ROUGE aligned well with actual summary quality because both lexical overlap and factual consistency were high.

---

### Mid-ROUGE Example — NEWS_0040

ROUGE Scores:

* ROUGE-1: 0.367
* ROUGE-2: 0.083
* ROUGE-L: 0.245

Observation:
The generated summary captured the central topic of the article but omitted several supporting details found in the reference summary. The summary remained factually correct, but the lower ROUGE-2 score reflected weaker phrase-level overlap. This example demonstrates that summaries can still be useful even when lexical overlap is moderate.

---

### Low-ROUGE Example — NEWS_0042

ROUGE Scores:

* ROUGE-1: 0.128
* ROUGE-2: 0.000
* ROUGE-L: 0.077

Observation:
The generated summary failed to capture important information contained in the reference summary and omitted several key details. Although the summary did not contain obvious hallucinations, it was incomplete and less informative. This example highlights a limitation of pre-trained summarization on domain-specific news content.

---

## Section 4: Production Decision Matrix

| Scenario                                                              | Recommendation        | Justification                                                                                                                                                           |
| --------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Real-time app-review sentiment dashboard for trading desk             | Fine-tuning           | The fine-tuned DistilBERT classifier achieved a macro-F1 of 0.6303 and provides low-latency predictions suitable for real-time monitoring.                              |
| Internal tech / entertainment news summary digest for a newsroom team | Pre-trained inference | DistilBART achieved ROUGE-1 0.3689 without any training cost, making it practical for low-risk summarization workflows.                                                 |
| Domain-expert QA on legal contracts                                   | Fine-tuning           | The pre-trained QA model achieved only 0.344 EM and 0.4611 token-F1, suggesting that domain-specific fine-tuning would be necessary for high-stakes legal applications. |

---

## Section 5: What You Would Do Differently

If a labeled summarization dataset were available for the tech and entertainment news domain, I would fine-tune the summarization model on that dataset. Domain-specific fine-tuning would likely improve ROUGE scores and help the model better capture terminology, writing style, and important details common in the target domain. I would also add a manual faithfulness evaluation process to ensure that improvements in ROUGE correspond to genuinely more accurate summaries rather than simply higher lexical overlap.

---

## Section 6: Limits of the Evaluation

The evaluation metrics used in this project do not fully capture output quality. ROUGE measures lexical overlap between generated and reference summaries but does not guarantee factual faithfulness. Similarly, exact match and token-F1 measure answer correctness but provide no information about model confidence or calibration. In addition, latency measurements were collected under single-request conditions and may not reflect real production workloads under heavy traffic. These limitations should be considered when interpreting the results and making deployment decisions.
