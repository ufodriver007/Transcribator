import whisper


def get_file(file_path: str) -> str:
    model = whisper.load_model("small")
    res = model.transcribe(file_path)
    return res["text"].strip()

