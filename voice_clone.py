from pathlib import Path
import os
import time
from typing import Optional, Tuple

import numpy as np
import soundfile as sf

# internal storage for loaded modules / objects
_models = {"loaded": False}


def init_models(
    enc_model_fpath: Optional[Path] = None,
    syn_model_fpath: Optional[Path] = None,
    voc_model_fpath: Optional[Path] = None,
    use_cpu: bool = False,
):
    """
    Load encoder/synthesizer/vocoder. Safe to call multiple times (loads once).
    - enc_model_fpath, syn_model_fpath, voc_model_fpath: optional Paths to .pt files
      (defaults to voice_cloning/saved_models/default/*)
    - use_cpu: if True sets CUDA_VISIBLE_DEVICES='-1' before importing model code.
    """
    global _models
    if _models.get("loaded"):
        return

    if use_cpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    from encoder import inference as encoder  # type: ignore
    from encoder.params_model import model_embedding_size as speaker_embedding_size  # type: ignore
    from synthesizer.inference import Synthesizer  # type: ignore
    from utils.default_models import ensure_default_models  # type: ignore
    from vocoder import inference as vocoder  # type: ignore

    base = Path(__file__).parent
    saved_models_dir = base / "saved_models"
    ensure_default_models(saved_models_dir)

    # defaults
    if enc_model_fpath is None:
        enc_model_fpath = saved_models_dir / "default" / "encoder.pt"
    if syn_model_fpath is None:
        syn_model_fpath = saved_models_dir / "default" / "synthesizer.pt"
    if voc_model_fpath is None:
        voc_model_fpath = saved_models_dir / "default" / "vocoder.pt"

    # load
    encoder.load_model(enc_model_fpath)
    synthesizer = Synthesizer(syn_model_fpath)
    vocoder.load_model(voc_model_fpath)

    _models.update(
        {
            "encoder": encoder,
            "synthesizer": synthesizer,
            "vocoder": vocoder,
            "speaker_embedding_size": speaker_embedding_size,
            "enc_model_fpath": str(enc_model_fpath),
            "syn_model_fpath": str(syn_model_fpath),
            "voc_model_fpath": str(voc_model_fpath),
            "loaded": True,
        }
    )

def synthesize_to_file(ref_audio: str, text: str, output_path: str = None, seed: int = None) -> str:
    init_models(use_cpu=True) 
    #Debug
    print('Models are initiated!')
    if not _models["loaded"]:
        raise RuntimeError("Models not initialized. Call init_models() first.")

    encoder = _models["encoder"]
    synthesizer = _models["synthesizer"]
    vocoder = _models["vocoder"]

    preprocessed_wav = encoder.preprocess_wav(ref_audio)
    embed = encoder.embed_utterance(preprocessed_wav)

    specs = synthesizer.synthesize_spectrograms([text], [embed])
    spec = specs[0]

    generated_wav = vocoder.infer_waveform(spec)

    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    generated_wav = encoder.preprocess_wav(generated_wav)  

    if output_path is None:
        out_dir = Path(__file__).parent.parent / "voices"
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / f"cloned_{int(time.time())}.wav"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    import soundfile as sf
    sf.write(str(output_path), generated_wav.astype(np.float32), synthesizer.sample_rate)

    return str(output_path)
