from pathlib import Path
import hashlib
import gdown

default_models = {
    "encoder": {
        "id": "1Fahntl4uiuOLZzkgyUR8NhtMIKys6BNY",
        "sha256": "39373b86598fa3da9fcddee6142382efe09777e8d37dc9c0561f41f0070f134e"},
    "synthesizer": {
        "id": "1TGN7QqixdYnov5o4SUT6yr5xH5xw73JY",
        "sha256": "c05e07428f95d0ed8755e1ef54cc8ae251300413d94ce5867a56afe39c499d94"},
    "vocoder": {
        "id": "19BSNQ7f5fSB-AxzPcZS5KbAUG61W79rj",
        "sha256": "1d7a6861589e927e0fbdaa5849ca022258fe2b58a20cc7bfb8fb598ccf936169"},
}

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): # Loads with chunks 8192 bytes each until returns ""
            h.update(chunk)
    return h.hexdigest()



def download(file_id: str, target: Path):
    url = f"https://drive.google.com/uc?id={file_id}"
    # Ensure the directory exists
    target.parent.mkdir(exist_ok=True, parents=True)
    desc = f"Downloading {target.name}"
    gdown.download(url, str(target), quiet=False)

def ensure_default_models(models_dir: Path):
    # Define download tasks
    jobs = []
    for model_name, info in default_models.items():
        target_path = models_dir / "default" / f"{model_name}.pt"
        expected_hash = info["sha256"]
        needs_download = True

        while needs_download:

            download(info["id"], target_path)

            if target_path.exists():
                actual_hash = compute_sha256(target_path)
                if expected_hash == actual_hash:
                    print(f"{model_name} downloaded and verified!")
                    needs_download = False
                else:
                    print(f"{model_name} has hash mismatch, redownloading...")

