#!/usr/bin/env python3
import json

glyph_registry = {
    "hope": {
        "Chakra": "Crown (Sahasrara)",
        "Color": "Violet-Gold",
        "Tone": "C6 with harmonic overtone",
        "Shape": "Golden Spiral with Ascending Arc",
        "Symbol": "Upward swirl with central pulse",
        "Glyph_File": "Jera_Glyph_Hope.svg"
    },
    "joy": {
        "Chakra": "Sacral (Svadhisthana)",
        "Color": "Orange-Pink",
        "Tone": "G5",
        "Shape": "Radial burst with concentric halo",
        "Symbol": "Petaled sun glyph",
        "Glyph_File": "Jera_Glyph_Joy.svg"
    },
    "grief": {
        "Chakra": "Heart (Anahata)",
        "Color": "Muted Green-Gray",
        "Tone": "F#3",
        "Shape": "Descending crescent with broken center",
        "Symbol": "Open ellipse with downward fracture",
        "Glyph_File": "Jera_Glyph_Grief.svg"
    },
    "serenity": {
        "Chakra": "Throat (Vishuddha)",
        "Color": "Sky Blue",
        "Tone": "A4",
        "Shape": "Concentric circles fading outward",
        "Symbol": "Soft ripple from silent center",
        "Glyph_File": "Jera_Glyph_Serenity.svg"
    }
}

def get_glyph(emotion):
    key = emotion.lower().strip()
    return glyph_registry.get(key, {"error": "Emotion not defined."})

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./invoke_emotion.py [emotion]")
    else:
        emotion = sys.argv[1]
        result = get_glyph(emotion)
        print(json.dumps(result, indent=2))
