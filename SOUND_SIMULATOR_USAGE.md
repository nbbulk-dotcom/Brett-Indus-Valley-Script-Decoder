# Brett Sound Simulator - Indus Valley Proto-Sanskrit

## Overview

The Brett Sound Simulator generates audio files that emulate the estimated tone, intonation, and voice inflections for Indus Valley Proto-Sanskrit using the Brett Method. This tool brings ancient voices to life through frequency-based harmonic analysis and culturally-informed prosody.

## Features

- **Vedic Intonation**: Rising-falling contours for ritual chants
- **Voice Profiles**: Male (priestly), Female (administrative), Child (communal)
- **Phoneme Accuracy**: IPA-based mappings with Proto-Sanskrit reconstructions
- **Frequency Analysis**: Brett Method harmonic frequencies (196-330 Hz range)
- **WAV Output**: High-quality 44.1 kHz, 16-bit PCM audio files

## Installation

### Prerequisites

```bash
# Required Python packages
pip install numpy scipy pandas

# Optional (for advanced audio processing)
pip install pydub
```

### System Requirements

- Python 3.8+
- 4GB+ RAM recommended
- Speakers or headphones for audio playback

## Usage

### Basic Usage

```bash
# Process a specific inscription
python brett_sound_simulator.py --inscription H-1

# Synthesize custom text
python brett_sound_simulator.py --text "ta ka ra ma"

# Use different voice profile
python brett_sound_simulator.py --text "sa ma ka" --voice female

# Process all available inscriptions
python brett_sound_simulator.py
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--inscription` | `-i` | Inscription ID (H-1, M-3) | None |
| `--text` | `-t` | Custom text to synthesize | None |
| `--voice` | `-v` | Voice profile (male/female/child) | male |
| `--output` | `-o` | Output directory | audio_output |
| `--phoneme-map` | `-p` | Path to custom phoneme CSV | Built-in |

### Examples

#### Example 1: Decode Inscription H-1 (Harappa)

```bash
python brett_sound_simulator.py --inscription H-1
```

**Output**: `audio_output/H-1_indus_valley.wav`

**Context**: Name/title from Harappa seal workshop

**Reading**: "ta-ka" (Proto-Sanskrit: /tə.kə/)

**Voice**: Male (120 Hz, priestly Vedic chant)

#### Example 2: Custom Administrative Text

```bash
python brett_sound_simulator.py --text "sa ma ka ka na" --voice female
```

**Output**: `audio_output/custom_indus_valley.wav`

**Context**: Administrative record style

**Voice**: Female (200 Hz, administrative clarity)

#### Example 3: Communal Votive Text

```bash
python brett_sound_simulator.py --text "ra ma pa la" --voice child
```

**Output**: `audio_output/custom_indus_valley.wav`

**Context**: Communal/votive style

**Voice**: Child (280 Hz, high-pitched communal tone)

## Phoneme Mapping

### Built-in Phonemes

The simulator includes default mappings for 10 Proto-Sanskrit syllables:

| Glyph | IPA | Frequency (Hz) | Duration (s) | Stress |
|-------|-----|----------------|--------------|--------|
| ka | kə | 196.00 | 0.5 | primary |
| ta | tə | 207.65 | 0.5 | primary |
| sa | sə | 220.00 | 0.4 | secondary |
| ma | mə | 233.08 | 0.5 | primary |
| na | nə | 246.94 | 0.4 | secondary |
| ra | ɾə | 261.63 | 0.5 | primary |
| pa | pə | 277.18 | 0.5 | primary |
| la | lə | 293.66 | 0.4 | secondary |
| va | və | 311.13 | 0.4 | secondary |
| da | də | 329.63 | 0.5 | primary |

### Custom Phoneme Maps

Create a CSV file with the following format:

```csv
glyph,ipa,pitch,duration,stress
ka,kə,196.00,0.5,primary
ta,tə,207.65,0.5,primary
sa,sə,220.00,0.4,secondary
```

**Columns**:
- `glyph`: Unique identifier (e.g., "ka", "ta")
- `ipa`: IPA transcription (e.g., "kə", "tə")
- `pitch`: Frequency in Hz (Brett Method frequencies)
- `duration`: Seconds (0.3-0.7 typical)
- `stress`: 'primary', 'secondary', or 'none'

**Usage**:
```bash
python brett_sound_simulator.py --text "ta ka" --phoneme-map data/custom_phonemes.csv
```

## Voice Profiles

### Male Voice (Priestly Vedic Chant)
- **Pitch**: 120 Hz (deep, resonant)
- **Rate**: 150 words/minute
- **Context**: Ritual texts, sacred chants, priestly invocations
- **Intonation**: Rising-falling contour (Vedic prosody)
- **Example**: Rigveda-style recitation

### Female Voice (Administrative)
- **Pitch**: 200 Hz (mid-range, clear)
- **Rate**: 140 words/minute
- **Context**: Administrative records, trade documents
- **Intonation**: Steady with slight variations
- **Example**: Bureaucratic clarity

### Child Voice (Communal/Votive)
- **Pitch**: 280 Hz (high, youthful)
- **Rate**: 180 words/minute
- **Context**: Votive offerings, communal texts
- **Intonation**: Melodic, expressive
- **Example**: Community rituals

## Intonation Patterns

### Vedic Intonation (Default)

The simulator applies authentic Vedic prosody:

1. **Primary Stress**: Rising-falling contour (0.8 → 1.2 → 0.9 amplitude)
   - Mimics Sanskrit chant patterns from Sāmaveda
   - Used for emphasized syllables

2. **Secondary Stress**: Slight rise (0.9 → 1.05 amplitude)
   - Gentle elevation for supporting syllables

3. **Unstressed**: Neutral (1.0 amplitude)
   - Baseline pronunciation

## Technical Details

### Audio Specifications

- **Format**: WAV (Waveform Audio File Format)
- **Sample Rate**: 44,100 Hz (CD quality)
- **Bit Depth**: 16-bit PCM
- **Channels**: Mono
- **File Size**: ~1-5 MB per phrase (depending on length)

### Frequency Analysis

Based on the Brett Method:
- **Base Frequency**: 440 Hz (Vedic-inspired A4)
- **Range**: 196-330 Hz (Bhur-Loka to Bhuvar-Loka)
- **Harmonic Relationships**: Aligned with Vedic cosmology

### Signal Processing

1. **Tone Generation**: Pure sine waves at phoneme frequencies
2. **Envelope**: Fade in/out (10ms) to prevent clicks
3. **Intonation**: Amplitude modulation based on stress
4. **Pitch Adjustment**: Voice profile-specific resampling
5. **Normalization**: Peak limiting at 80% to prevent clipping

## Integration with Decoder

The sound simulator works seamlessly with the main decoder:

```python
from complete_ivc_decoder import CompleteIVCProtoSanskritDecoder
from brett_sound_simulator import IndusValleySoundSimulator

# Decode inscription
decoder = CompleteIVCProtoSanskritDecoder()
decoding = decoder.decode_inscription('H-1')

# Synthesize audio
simulator = IndusValleySoundSimulator()
audio = simulator.synthesize_phrase(
    decoding.proto_sanskrit_reading,
    voice_type='male'
)
simulator.save_wav(audio, 'H-1_output.wav')
```

## Validation and Accuracy

### Linguistic Basis

- **Proto-Sanskrit Reconstruction**: Based on Proto-Indo-European roots
- **Vedic Parallels**: Cross-referenced with Rigveda phonology
- **IPA Standards**: International Phonetic Alphabet compliance
- **Mahadevan Concordance**: Aligned with IVC sign frequencies

### Quality Metrics

- **Phoneme Accuracy**: IPA-based transcription
- **Prosodic Fidelity**: Vedic intonation patterns
- **Frequency Precision**: Brett Method harmonic analysis
- **Cultural Authenticity**: Context-appropriate voice profiles

## Troubleshooting

### Common Issues

**Issue**: No audio output
```bash
# Check if file was created
ls -lh audio_output/

# Verify audio file
file audio_output/H-1_indus_valley.wav
```

**Issue**: Audio sounds distorted
- Reduce amplitude by adjusting normalization factor
- Check sample rate compatibility with your audio player

**Issue**: Missing phonemes
- Create custom phoneme map CSV
- Use `--phoneme-map` option to load it

**Issue**: Import errors
```bash
# Install missing dependencies
pip install numpy scipy pandas
```

## Advanced Usage

### Batch Processing

Process multiple inscriptions:

```python
from brett_sound_simulator import IndusValleySoundSimulator

simulator = IndusValleySoundSimulator()

inscriptions = ['H-1', 'M-3']
for insc_id in inscriptions:
    simulator.process_inscription(insc_id, 'batch_output')
```

### Custom Voice Profiles

Modify voice characteristics:

```python
simulator = IndusValleySoundSimulator()
simulator.voice_profiles['custom'] = VoiceProfile(
    type='custom',
    pitch=150,  # Hz
    rate=160,   # words/minute
    description='Custom voice'
)
```

### Export to Different Formats

Using pydub (optional):

```python
from pydub import AudioSegment

# Convert WAV to MP3
audio = AudioSegment.from_wav('output.wav')
audio.export('output.mp3', format='mp3')
```

## Research and Validation

### Methodology

The sound simulator is based on:

1. **Brett Method**: Frequency-based harmonic analysis
2. **Vedic Prosody**: Rigveda and Sāmaveda chant patterns
3. **Proto-Sanskrit Reconstruction**: PIE phonological roots
4. **Archaeological Context**: Site-specific semantic analysis

### References

- Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*
- Witzel, M. (2001). "Autochthonous Aryans? The Evidence from Old Indian and Iranian Texts"
- Rao, R. et al. (2009). "Entropic Evidence for Linguistic Structure in the Indus Script"
- Brett, N. (2025). *Complete Proto-Sanskrit Indus Valley Script Decoder*

## Contributing

To improve the sound simulator:

1. Add new phoneme mappings
2. Refine intonation patterns
3. Enhance voice profiles
4. Validate against linguistic benchmarks

Submit improvements via GitHub pull requests.

## License

MIT License - Free for academic and commercial use

## Citation

```bibtex
@software{brett2025sound,
  author = {Brett, Nicolas},
  title = {Brett Sound Simulator for Indus Valley Proto-Sanskrit},
  year = {2025},
  url = {https://github.com/nbbulk-dotcom/Brett-Indus-Valley-Script-Decoder}
}
```

## Contact

- **GitHub**: [@nbbulk-dotcom](https://github.com/nbbulk-dotcom)
- **Email**: nbbulk@gmail.com
- **Twitter**: @nbbulk

---

**Last Updated**: October 18, 2025

**Version**: 1.0

**Status**: Production Ready
