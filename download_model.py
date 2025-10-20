import argparse
import os
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer


def download_model(model_name: str, cache_dir: str) -> None:
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)

    # Download tokenizer and model weights into cache_dir
    AutoTokenizer.from_pretrained(model_name, cache_dir=str(cache_path))
    AutoModelForCausalLM.from_pretrained(model_name, cache_dir=str(cache_path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a Hugging Face model into ./models")
    parser.add_argument(
        "--model",
        default=os.environ.get("EKKO_MODEL", "gpt2"),
        help="Model name or path on Hugging Face (default: gpt2)",
    )
    parser.add_argument(
        "--dir",
        default=os.environ.get("EKKO_MODELS_DIR", "./models"),
        help="Target directory to store model files (default: ./models)",
    )
    args = parser.parse_args()

    print(f"Downloading model '{args.model}' to '{args.dir}' ...")
    download_model(args.model, args.dir)
    print("Download completed.")


if __name__ == "__main__":
    main()


