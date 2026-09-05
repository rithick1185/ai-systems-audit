import subprocess

corpus_args = [
    "--corpus", "eng=partA/corpus/eng_sample.txt",
    "--corpus", "hin=partA/corpus/hin_sample.txt",
    "--corpus", "kan=partA/corpus/kan_sample.txt",
    "--corpus", "tam=partA/corpus/tam_sample.txt",
]

print("Running GPT-2 benchmark...")
subprocess.run(
    [
        "python",
        "fertility.py",
        *corpus_args,
        "--tokenizer",
        "gpt2",
    ],
    check=True,
)

print("\nRunning XLM-RoBERTa benchmark...")
subprocess.run(
    [
        "python",
        "fertility.py",
        *corpus_args,
        "--tokenizer",
        "hf:xlm-roberta-base",
    ],
    check=True,
)