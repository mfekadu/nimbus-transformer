#!/usr/bin/env python3
from ntfp.ntfp import get_context, transformer
from ntfp.ntfp_types import Answer, Context, Question

if __name__ == "__main__":
    print("\n")
    user_input: str = input("question: ")
    question: Question = Question(user_input)

    context: Context = get_context(question)
    print("len(context): ", len(context))

    answer: Answer = transformer(question, context)
    print("\n\n\nanswer: ", answer)
