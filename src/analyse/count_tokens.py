import tiktoken
import json

def main():

    enc = tiktoken.get_encoding("o200k_base")
    assert enc.decode(enc.encode("hello world")) == "hello world"
    enc = tiktoken.encoding_for_model("gpt-4o")

    file_path = "data/dev/test/30-1-100-s.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for d in data:
        tokens = enc.encode(d["story"])
        d["tokens"] = len(tokens)
        print(d["tokens"])

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()