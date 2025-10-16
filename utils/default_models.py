import urllib.request
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError

from tqdm import tqdm


default_models = {
    "encoder": ("https://drive.google.com/uc?export=download&id=1Fahntl4uiuOLZzkgyUR8NhtMIKys6BNY", 17090379),
    "synthesizer": ("https://drive.google.com/file/d/1TGN7QqixdYnov5o4SUT6yr5xH5xw73JY/view?usp=sharing", 370554559),
    "vocoder": ("https://drive.google.com/file/d/19BSNQ7f5fSB-AxzPcZS5KbAUG61W79rj/view?usp=sharing", 53845290),
}


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download(url: str, target: Path, bar_pos=0):
    # Ensure the directory exists
    target.parent.mkdir(exist_ok=True, parents=True)

    desc = f"Downloading {target.name}"
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=desc, position=bar_pos, leave=False) as t:
        try:
            urllib.request.urlretrieve(url, filename=target, reporthook=t.update_to)
        except HTTPError:
            return


def ensure_default_models(models_dir: Path):
    # Define download tasks
    jobs = []
    for model_name, (url, size) in default_models.items():
        target_path = models_dir / "default" / f"{model_name}.pt"
        if target_path.exists():
            if target_path.stat().st_size != size:
                print(f"File {target_path} is not of expected size, redownloading...")
            else:
                continue

        thread = Thread(target=download, args=(url, target_path, len(jobs)))
        thread.start()
        jobs.append((thread, target_path, size))

    # Run and join threads
    for thread, target_path, size in jobs:
        thread.join()

        assert target_path.exists() and target_path.stat().st_size == size, \
            f"Download for {target_path.name} failed. You may download models manually instead.\n" \
            f"https://drive.google.com/drive/folders/1fU6umc5uQAVR2udZdHX-lDgXYzTyqG_j"
