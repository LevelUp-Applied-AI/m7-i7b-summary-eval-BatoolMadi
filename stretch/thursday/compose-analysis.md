# Summarize-then-QA — Trade-Off Analysis Memo

## 1. Test Set Design

* Total questions: 20
* Article types chosen: long-form entertainment, cybersecurity, celebrity, music, and fashion news articles whose token lengths exceeded the QA model context window (~384 tokens).
* Question types:

  * factual questions,
  * entity-attribution questions,
  * location and date questions,
  * numerical/statistical questions,
  * and several deeper-in-document questions.
* Why these choices:

The test set was intentionally designed around long articles because the purpose of this stretch is to compare full-document QA with chunking against summarize-then-QA. I selected articles containing detailed facts, statistics, names, and contextual information spread throughout the article. Some questions focused on top-of-document information while others targeted details appearing later in the article to better expose the strengths and weaknesses of chunking and summarization pipelines.

---

## 2. Strategy A Results — QA on the Full Article (with Chunking)

* Aggregate EM: 0.35

* Aggregate F1: 0.4817

* Where Strategy A wins:

Strategy A performed better on detailed factual questions because chunking preserved more of the original article information.

Examples:

* EX_13 correctly identified "3,200 account hijacking cases."
* EX_16 correctly extracted the Twitter growth statistic "1,382 percent."
* EX_03 correctly identified "The Pianist."

These answers depended on precise factual details that were preserved in the original article chunks.

* Where Strategy A loses:

Strategy A occasionally struggled when irrelevant chunks contained distracting entities or repeated names.

Examples:

* Some celebrity-related questions returned partial answers instead of the full expected span.
* Long articles containing repeated references to the same people occasionally confused the QA model across chunks.

---

## 3. Strategy B Results — QA on the Summary

* Aggregate EM: 0.20

* Aggregate F1: 0.2417

* Where Strategy B wins:

Strategy B worked best for high-level questions where the answer appeared early in the article or represented the article’s central topic.

Examples:

* EX_01 about Roman Polanski being arrested in Switzerland.
* EX_09 involving Grey's Anatomy.
* EX_17 about Roberto Cavalli being born in Florence.

These details were usually preserved in the generated summaries.

* Where Strategy B loses:

Strategy B frequently failed when summarization removed specific factual evidence.

Examples:

* EX_13 failed because the summary omitted the statistic about "3,200 account hijacking cases."
* EX_16 failed because the detailed "1,382 percent" Twitter growth statistic was not consistently preserved.

This demonstrates that summarization can reduce answer accuracy for extractive QA tasks.

---

## 4. Faithfulness Analysis (Strategy B)

**Article (excerpt):**

> "Since 2006, nearly 3,200 account hijacking cases have been reported to the Internet Crime Complaint Center."

**Summary:**

> The summary discussed cybercrime and phishing attacks on social networking sites but omitted the exact statistic.

**Question:**

How many account hijacking cases have been reported since 2006?

**Strategy B prediction:**

Incorrect or incomplete answer.

**Gold:**

"3,200 account hijacking cases"

**What was lost in summarization:**

The generated summary preserved the general idea that cybercrime on social networks is increasing, but it removed the exact numerical statistic needed for extractive QA. Because the evidence sentence disappeared during summarization, the QA model could not recover the correct answer from the summary alone.

---

## 5. Recommendation

| Use Strategy A when…                                                  | Use Strategy B when…                                                                 |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Article length exceeds 800 tokens and factual precision is important. | High-level semantic understanding is sufficient and lower compute cost is preferred. |
| The answer location is unknown or appears deep in the article.        | The question targets the main topic or top-of-document information.                  |
| Questions involve statistics, names, dates, or detailed evidence.     | Approximate answers are acceptable.                                                  |

Justification:

Strategy A achieved higher performance overall (EM = 0.35, F1 = 0.4817) because chunking preserved detailed evidence from the original articles. Strategy B achieved lower performance (EM = 0.20, F1 = 0.2417) because summarization removed important factual details. However, summarize-then-QA uses shorter contexts and may reduce compute requirements, making it useful for lightweight or high-level QA tasks.
