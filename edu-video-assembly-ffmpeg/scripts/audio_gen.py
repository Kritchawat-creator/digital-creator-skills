"""Generate original (copyright-free, self-made) music bed and sound effects as WAV files.

Everything here is synthesised from code, so the channel owns it outright.
Output: audio/music_loop.wav (seamless loop), audio/sfx_*.wav
"""
import array
import math
import random
import wave

SR = 44100
random.seed(7)


def write_wav(path, samples, sr=SR):
    """Write mono float samples (-1..1) as 16-bit PCM."""
    peak = max(1e-9, max(abs(s) for s in samples))
    gain = 0.89 / peak
    data = array.array("h", (int(max(-1.0, min(1.0, s * gain)) * 32767) for s in samples))
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())


def pluck(freq, dur, decay=0.996):
    """Karplus-Strong plucked string (ukulele-like)."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = [random.uniform(-1, 1) for _ in range(period)]
    out = []
    for i in range(n):
        v = buf[i % period]
        nxt = buf[(i + 1) % period]
        buf[i % period] = decay * 0.5 * (v + nxt)
        out.append(v)
    return out


def note(name):
    """Note name like 'C4' to Hz."""
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    semis = names[name[0]] + (1 if "#" in name else 0) + 12 * (int(name[-1]) - 4)
    return 440.0 * 2 ** (semis / 12)


def mix_into(dst, src, start, gain=1.0):
    for i, s in enumerate(src):
        j = start + i
        if j < len(dst):
            dst[j] += s * gain


def make_music():
    """16-bar happy loop: C - G - Am - F, 104 bpm, plucked chords + soft bass + light shaker."""
    bpm = 104
    beat = 60 / bpm
    bars = 16
    total = int(SR * beat * 4 * bars)
    out = [0.0] * total
    chords = [["C4", "E4", "G4"], ["G3", "B3", "D4"], ["A3", "C4", "E4"], ["F3", "A3", "C4"]]
    bass = ["C3", "G2", "A2", "F2"]
    melody_pattern = [0, 2, 1, 2, 0, 2, 1, 2]  # chord-tone arpeggio per eighth note
    for bar in range(bars):
        ch = chords[bar % 4]
        bar_start = int(SR * beat * 4 * bar)
        # bass on beats 1 and 3
        for b in (0, 2):
            s = pluck(note(bass[bar % 4]), beat * 2, 0.998)
            mix_into(out, s, bar_start + int(SR * beat * b), 0.55)
        # arpeggio eighth notes (one octave up)
        for k, idx in enumerate(melody_pattern):
            f = note(ch[idx]) * 2
            s = pluck(f, beat * 0.9, 0.994)
            mix_into(out, s, bar_start + int(SR * beat * 0.5 * k), 0.30)
        # strum on beat 1
        for idx, nm in enumerate(ch):
            s = pluck(note(nm), beat * 3, 0.997)
            mix_into(out, s, bar_start + int(SR * 0.012 * idx), 0.25)
        # shaker on off-beats
        for k in range(8):
            if k % 2 == 1:
                start = bar_start + int(SR * beat * 0.5 * k)
                for i in range(int(SR * 0.05)):
                    env = math.exp(-i / (SR * 0.012))
                    if start + i < total:
                        out[start + i] += random.uniform(-1, 1) * 0.05 * env
    # gentle fade at loop edges to avoid clicks
    edge = int(SR * 0.01)
    for i in range(edge):
        out[i] *= i / edge
        out[-1 - i] *= i / edge
    write_wav("audio/music_loop.wav", out)


def env_tone(freqs, dur, attack=0.005, release=0.25, shape="sine"):
    n = int(SR * dur)
    out = []
    for i in range(n):
        t = i / SR
        env = min(1.0, t / attack) * math.exp(-t / release)
        v = 0.0
        for f in freqs:
            ph = 2 * math.pi * f * t
            v += math.sin(ph) if shape == "sine" else (1.0 if math.sin(ph) >= 0 else -1.0) * 0.5
        out.append(v * env / len(freqs))
    return out


def make_sfx():
    write_wav("audio/sfx_ding.wav", env_tone([1318.5, 1975.5], 0.9, release=0.3))          # correct answer
    write_wav("audio/sfx_buzz.wav", env_tone([110, 116], 0.6, release=0.5, shape="square"))  # wrong answer
    write_wav("audio/sfx_pop.wav", env_tone([880], 0.15, release=0.04))                     # text pop
    write_wav("audio/sfx_tick.wav", env_tone([2000], 0.06, release=0.01))                   # countdown tick
    # whoosh: noise with rising band emphasis
    n = int(SR * 0.6)
    w, lp = [], 0.0
    for i in range(n):
        t = i / n
        a = 0.02 + 0.5 * t
        lp += a * (random.uniform(-1, 1) - lp)
        w.append(lp * math.sin(math.pi * t))
    write_wav("audio/sfx_whoosh.wav", w)
    # chime sting for section titles: quick rising arpeggio
    st = [0.0] * int(SR * 1.2)
    for k, nm in enumerate(["C5", "E5", "G5", "C6"]):
        mix_into(st, env_tone([note(nm)], 0.8, release=0.35), int(SR * 0.09 * k), 0.8)
    write_wav("audio/sfx_sting.wav", st)


if __name__ == "__main__":
    make_sfx()
    make_music()
    print("audio done")
