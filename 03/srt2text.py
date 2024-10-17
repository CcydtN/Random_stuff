import sys
import os
import nltk.data
import yt_dlp
from pathlib import Path


def srt2text(input_path):
    with input_path.open() as file:
        data = file.read().splitlines()

    start_idx = 0
    groups = []
    for i, val in enumerate(data):
        # print(i,val)
        if val == "" and start_idx < i:
            groups.append(data[start_idx:i])
            start_idx = i + 1

    # check the groups are in order
    assert all(
        int(groups[i][0]) + 1 == int(groups[i + 1][0]) for i in range(len(groups) - 1)
    )

    fragments = [t for group in groups for t in group[2:]]

    text = " ".join(fragments)
    # print(text)

    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    return "\n\n".join(tokenizer.tokenize(text))


if __name__ == "__main__":
    input_path = Path(sys.argv[1].replace(" ", "\ "))
    output_path = Path(sys.argv[2])
    print(input_path, output_path)
    assert input_path.exists()

    output_text = srt2text(input_path)
    with open(output_path, "w") as file:
        file.write(output_text)
