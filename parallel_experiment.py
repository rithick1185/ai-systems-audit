import tiktoken

enc = tiktoken.get_encoding("gpt2")

pairs = [
    ("The farmer is working in the field.",
     "किसान खेत में काम कर रहा है।"),

    ("The weather is good today.",
     "आज मौसम अच्छा है।"),

    ("We are learning artificial intelligence.",
     "हम कृत्रिम बुद्धिमत्ता सीख रहे हैं।"),

    ("The machine is running efficiently.",
     "मशीन कुशलता से चल रही है।"),

    ("The company wants to reduce costs.",
     "कंपनी लागत कम करना चाहती है।"),
]

print("English tokens | Hindi tokens | English words | Hindi words")
print("-" * 65)

total_eng_tokens = 0
total_hin_tokens = 0
total_eng_words = 0
total_hin_words = 0

for eng, hin in pairs:
    eng_tokens = len(enc.encode(eng.lower()))
    hin_tokens = len(enc.encode(hin.lower()))

    eng_words = len(eng.split())
    hin_words = len(hin.split())

    total_eng_tokens += eng_tokens
    total_hin_tokens += hin_tokens
    total_eng_words += eng_words
    total_hin_words += hin_words

    print(
        f"{eng_tokens:14} | {hin_tokens:12} | "
        f"{eng_words:13} | {hin_words:11}"
    )

print()
print("Total English tokens:", total_eng_tokens)
print("Total Hindi tokens:", total_hin_tokens)

print("English tokens/word:",
      round(total_eng_tokens / total_eng_words, 3))

print("Hindi tokens/word:",
      round(total_hin_tokens / total_hin_words, 3))

print("Hindi/English token ratio:",
      round(total_hin_tokens / total_eng_tokens, 3))