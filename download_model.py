import argparse
import os
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer


def download_model(model_name: str, cache_dir: str | None, force: bool = False) -> None:
    # When cache_dir is None, Hugging Face uses the default user cache (~/.cache/huggingface)
    kwargs = {"cache_dir": cache_dir} if cache_dir else {}
    if force:
        kwargs["force_download"] = True
        kwargs["local_files_only"] = False
    AutoTokenizer.from_pretrained(model_name, **kwargs)
    AutoModelForCausalLM.from_pretrained(model_name, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a Hugging Face model into ./models")
    parser.add_argument(
        "--model",
        default=os.environ.get("EKKO_MODEL", "gpt2"),
        help="Model name or path on Hugging Face (default: gpt2)",
    )
    parser.add_argument(
        "--dir",
        default=os.environ.get("EKKO_MODELS_DIR", None),
        help="Optional cache directory to store model files (default: HF user cache)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if files exist",
    )
    args = parser.parse_args()

    where = args.dir if args.dir else "<hf default cache>"
    print(f"Downloading model '{args.model}' to {where} (force={args.force}) ...")
    download_model(args.model, args.dir, force=args.force)
    print("Download completed.")


if __name__ == "__main__":
    main()


