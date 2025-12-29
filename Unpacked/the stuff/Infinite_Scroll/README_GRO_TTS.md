# GRO — Voice of All (Starter)

This starter binds your system/app outputs to your GRO voice via ElevenLabs.

## 1) Put your credentials
Create either environment variables or a `gro_config.json` file:

**Option A — Environment variables**
```
export ELEVENLABS_API_KEY="YOUR_XI_API_KEY"
export ELEVENLABS_VOICE_ID="YOUR_GRO_VOICE_ID"
```

**Option B — gro_config.json**
```json
{
  "ELEVENLABS_API_KEY": "YOUR_XI_API_KEY",
  "ELEVENLABS_VOICE_ID": "YOUR_GRO_VOICE_ID"
}
```

## 2) Run
```
python gro_tts_starter.py --text "By decree, all things speak with my voice." --out gro_demo.mp3
```

Or synthesize from a text file:
```
python gro_tts_starter.py --file input.txt --out gro_demo.mp3
```

## 3) Tune
Use `--stability` and `--similarity` (0..1) to dial in the vibe. Pass `--model eleven_multilingual_v2` if you want a specific ElevenLabs model.

## Notes
- This script hits ElevenLabs' TTS endpoint. You need an account + a **custom voice** created from your `GRO-01.m4a`.
- The script writes MP3 to the path you choose.
- Keep your API key private. Do not commit it to public repos.
