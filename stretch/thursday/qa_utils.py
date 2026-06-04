import re
import string
from collections import Counter

from transformers import pipeline


def get_qa_model_name() -> str:
    """Return the QA model name."""
    return "distilbert-base-cased-distilled-squad"


def normalize_answer(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def remove_punc(text):
        return "".join(ch for ch in text if ch not in string.punctuation)

    def white_space_fix(text):
        return " ".join(text.split())

    def lower(text):
        return text.lower()

    return white_space_fix(
        remove_articles(
            remove_punc(
                lower(s)
            )
        )
    )


def exact_match(pred: str, gold: str) -> int:
    """Return 1 if normalized prediction equals normalized gold."""

    return int(normalize_answer(pred) == normalize_answer(gold))


def token_f1(pred: str, gold: str) -> float:
    """
    Token-level F1 score.
    """

    pred_tokens = normalize_answer(pred).split()
    gold_tokens = normalize_answer(gold).split()

    # both empty
    if len(pred_tokens) == 0 and len(gold_tokens) == 0:
        return 1.0

    # one empty
    if len(pred_tokens) == 0 or len(gold_tokens) == 0:
        return 0.0

    common = Counter(pred_tokens) & Counter(gold_tokens)

    num_same = sum(common.values())

    if num_same == 0:
        return 0.0

    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)

    f1 = 2 * precision * recall / (precision + recall)

    return f1


def build_qa_pipeline(model_name: str):
    """
    Build HuggingFace QA pipeline.
    """

    qa = pipeline(
        "question-answering",
        model=model_name
    )

    return qa


def predict_one(qa, question: str, context: str) -> str:
    """
    Run QA pipeline and return only answer string.
    """

    result = qa(
        question=question,
        context=context
    )

    return result["answer"]

