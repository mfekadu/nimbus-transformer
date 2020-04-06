#!/usr/bin/env python3
from ntfp.ntfp import get_context, transformer
from ntfp.ntfp_types import (
    Answer,
    Context,
    Query,
    Question,
    WebPage,
    ExtraDataDict,
    Score,
    Start,
    End,
)
from typing import Tuple, cast
import pandas as pd
from os import listdir


if __name__ == "__main__":
    print("\n")
    user_input: str = input("question: ")
    question: Question = Question(user_input)

    google_data: Tuple[Query, WebPage, Context] = get_context(question)
    query, page, context = google_data
    print("len(context): ", len(context))

    trfrmr_data: Tuple[Answer, ExtraDataDict] = transformer(question, context)
    answer = trfrmr_data[0]
    extra_data = trfrmr_data[1]
    print("\n\n\nanswer: ", answer)

    CSV_FILENAME = "data.csv"

    score: Score = cast(Score, extra_data["score"])
    start: Start = cast(Start, extra_data["start"])
    end: End = cast(End, extra_data["end"])
    tokenizer: str = extra_data["tokenizer"]
    model: str = extra_data["model"]
    # fmt:off
    data = {
        "question": [question],
        "query": [query],
        "answer": [answer],
        "score": [score],
        "start": [start],
        "end": [end],
        "tokenizer": [tokenizer],
        "model": [model],
        "context": [context],
        "page": [page],
    }
    # fmt:on

    df: pd.DataFrame = pd.DataFrame(data)

    if CSV_FILENAME in listdir("."):
        df.to_csv(CSV_FILENAME, mode="a", header=False)
        print(f"appended new row to {CSV_FILENAME}")
    else:
        df.to_csv(CSV_FILENAME)
        print(f"created {CSV_FILENAME} and appended a row.")
