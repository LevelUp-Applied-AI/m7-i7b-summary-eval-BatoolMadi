# Module 7 Week B — Integration Task: Summarization & Integrated Evaluation Report

This is the starter repo for the Module 7 Week B Integration Task. **The integrated evaluation report you produce here is the M7 deliverable.**

The full integration guide is at <a href="https://levelup-applied-ai.github.io/aispire-14005-pages/modules/module-7/496c1c2b" target="_blank">the integration guide page</a> — read it first.

## Quick start

```bash
pip install -r requirements.txt
make summarize    # runs full pipeline; first run downloads ~250 MB
```

The first call to `pipeline("summarization", ...)` downloads the model. Plan ~3 minutes for the first run; subsequent runs use cached weights. The full evaluation on 120 articles completes in ~6–8 minutes on CPU after the model is cached.

## What you will produce

Committed:
- `summarize.py` — your implementation
- Updated `README.md` — 1–2 paragraphs documenting model id, corpus version, re-run command (this section is the template; replace it)
- `summary_predictions.csv` — 120 rows with reference, predicted, and per-summary ROUGE
- `summary_metrics.json` — aggregate ROUGE-1/2/L F1
- `integrated-evaluation-report.md` — six-section integrated report (the M7 deliverable). Includes an optional Section 7 (Challenge Extensions) for learners completing challenge tiers — see the integration's learner guide.

**No model file** — pre-trained model loads from Hugging Face Hub at runtime.

## Data

- `data/tech_news_articles.csv` — 1,033 tech / entertainment / digital-culture news articles, curated from <a href="https://huggingface.co/datasets/glnmario/news-qa-summarization" target="_blank">glnmario/news-qa-summarization</a>. The full pool is here for inspection and stretch use; the integration evaluates on the 120-article subset that has reference summaries.
- `data/tech_news_summaries_reference.csv` — 120 reference summaries (one per evaluated article), shipped with the curated dataset (CNN editor-authored summaries from the source dataset).
- `data/tiny_articles_smoke.csv` + `data/tiny_refs_smoke.csv` — 3-row CI smoke fixtures (articles and references in separate files, matching the real-data schema).

## Make targets

```bash
make summarize    # full pipeline against the 120-article evaluation set
make smoke        # CI-only target — 3-row fixture
make clean        # remove generated outputs
```

## Submission

Open a Pull Request from your working branch into `main`. The autograder runs `make smoke` against the 3-row fixture and validates artifact schemas. PR description requirements are in the integration guide.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.

## Summarization Model

This project uses the Hugging Face model:

* `sshleifer/distilbart-cnn-6-6`

for abstractive summarization tasks. The model was loaded using the Hugging Face `pipeline("summarization")` API.

---

## Corpus Details

The evaluation corpus consists of more than 1,000 technology, entertainment, cybersecurity, and celebrity news articles provided in:

* `data/tech_news_articles.csv`

Reference summaries are stored in:

* `data/tech_news_summaries_reference.csv`

The stretch evaluation additionally uses a manually-authored QA dataset containing 20 extractive QA examples across multiple long-form articles.

---

## Results Summary

### Integration 7B Summarization Results

The summarization pipeline was evaluated using ROUGE metrics:

* ROUGE-1
* ROUGE-2
* ROUGE-L

### Stretch: Summarize-then-QA Results

| Strategy                      | EM   | F1     |
| ----------------------------- | ---- | ------ |
| Full-article QA with chunking | 0.35 | 0.4817 |
| Summarize-then-QA             | 0.20 | 0.2417 |

The results show that chunked full-document QA preserves factual accuracy better than summarize-then-QA, especially for numerical or detail-heavy questions.

---

## Re-run Instructions

Create and activate the virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the summarization evaluation:

```bash
python summarize.py
```

Run the stretch summarize-then-QA pipeline:

```bash
python stretch/thursday/pipeline_compose.py
```

---

## Implementation Notes

* The QA system uses `distilbert-base-cased-distilled-squad`.
* Long articles are processed using overlapping chunk windows.
* Summaries are generated deterministically using beam search (`num_beams=4`, `do_sample=False`).
* ROUGE scoring uses stemming-enabled evaluation.
* The summarize-then-QA strategy demonstrated lower factual recall because summarization occasionally removed answer evidence required for extractive QA.
