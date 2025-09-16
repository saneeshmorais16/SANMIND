from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException
import tempfile, os, ffmpeg
from faster_whisper import WhisperModel
from services import nlp

router = APIRouter()

# load a tiny model for CPU; set device="cpu"
_model = WhisperModel("tiny", device="cpu", compute_type="int8")

def webm_to_wav_bytes(webm_bytes: bytes, sr: int = 16000) -> bytes:
    """Decode webm/opus -> wav PCM using ffmpeg in-memory pipes."""
    in_stream = ffmpeg.input('pipe:', format='webm')
    out_stream = ffmpeg.output(
        in_stream.audio, 'pipe:', format='wav', acodec='pcm_s16le', ac=1, ar=sr
    ).overwrite_output()
    out, err = ffmpeg.run(out_stream, input=webm_bytes, capture_stdout=True, capture_stderr=True)
    return out  # WAV bytes

@router.post("/voice")
async def predict_voice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".webm", ".ogg", ".mp3", ".wav")):
        raise HTTPException(400, "Please upload a short audio clip (webm/ogg/wav).")

    raw = await file.read()

    # 1) decode to wav bytes
    try:
        wav_bytes = webm_to_wav_bytes(raw, sr=16000)
    except ffmpeg.Error as e:
        raise HTTPException(400, f"Audio decode failed: {e.stderr.decode('utf-8', 'ignore')[:200]}")

    # 2) write temp wav for faster-whisper
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(wav_bytes)
        tmp_path = tmp.name

    try:
        # 3) transcribe
        segments, info = _model.transcribe(tmp_path, language="en")
        text = " ".join(seg.text.strip() for seg in segments).strip() or "(no speech detected)"

        # 4) reuse your text emotion model
        emotion, conf = nlp.heuristic_emotion(text)
        reply = f"(voice) I heard: “{text}”"

        return {"emotion": emotion, "confidence": conf, "note": reply, "transcript": text}
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
