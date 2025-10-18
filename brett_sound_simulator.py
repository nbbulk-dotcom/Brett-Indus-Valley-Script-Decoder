#!/usr/bin/env python3
"""
Brett Sound Simulator - Indus Valley Proto-Sanskrit
====================================================
Generates audio files that emulate the estimated tone, intonation, and voice 
inflections for Indus Valley Proto-Sanskrit using the Brett Method.

Created by: Nicolas of the Family Brett
Date: October 18, 2025
License: MIT
"""

import numpy as np
from scipy.io import wavfile
import pandas as pd
import os
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Install with: pip install pydub")

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    type: str  # 'male', 'female', 'child'
    pitch: float  # Hz
    rate: int  # Words per minute
    description: str

@dataclass
class PhonemeData:
    """Phoneme data structure"""
    glyph: str
    ipa: str
    pitch: float
    duration: float
    stress: str

class IndusValleySoundSimulator:
    """Sound simulator for Indus Valley Proto-Sanskrit"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.voice_profiles = {
            'male': VoiceProfile('male', 120, 150, 'Priestly Vedic chant tone'),
            'female': VoiceProfile('female', 200, 140, 'Administrative tone'),
            'child': VoiceProfile('child', 280, 180, 'Communal/votive tone')
        }
        self.base_freq = 440  # Vedic-inspired A4
        
    def load_phoneme_map(self, file_path: str) -> Dict[str, PhonemeData]:
        """Load phoneme-to-IPA mapping"""
        if not os.path.exists(file_path):
            # Create default phoneme map
            return self._create_default_phoneme_map()
        
        df = pd.read_csv(file_path)
        phoneme_map = {}
        for _, row in df.iterrows():
            phoneme_map[row['glyph']] = PhonemeData(
                glyph=row['glyph'],
                ipa=row['ipa'],
                pitch=row['pitch'],
                duration=row['duration'],
                stress=row['stress']
            )
        return phoneme_map
    
    def _create_default_phoneme_map(self) -> Dict[str, PhonemeData]:
        """Create default phoneme mappings for Indus Valley"""
        default_phonemes = {
            'ka': PhonemeData('ka', 'kə', 196.00, 0.5, 'primary'),
            'ta': PhonemeData('ta', 'tə', 207.65, 0.5, 'primary'),
            'sa': PhonemeData('sa', 'sə', 220.00, 0.4, 'secondary'),
            'ma': PhonemeData('ma', 'mə', 233.08, 0.5, 'primary'),
            'na': PhonemeData('na', 'nə', 246.94, 0.4, 'secondary'),
            'ra': PhonemeData('ra', 'ɾə', 261.63, 0.5, 'primary'),
            'pa': PhonemeData('pa', 'pə', 277.18, 0.5, 'primary'),
            'la': PhonemeData('la', 'lə', 293.66, 0.4, 'secondary'),
            'va': PhonemeData('va', 'və', 311.13, 0.4, 'secondary'),
            'da': PhonemeData('da', 'də', 329.63, 0.5, 'primary')
        }
        return default_phonemes
    
    def generate_tone(self, freq: float, duration: float) -> np.ndarray:
        """Generate sine wave for phoneme"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(2 * np.pi * freq * t)
        
        # Apply envelope to avoid clicks
        envelope = np.ones_like(tone)
        fade_samples = int(0.01 * self.sample_rate)
        if len(tone) > 2 * fade_samples:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
    
    def apply_vedic_intonation(self, audio: np.ndarray, stress: str) -> np.ndarray:
        """Apply Vedic rising-falling intonation for ritual chants"""
        samples = len(audio)
        
        if stress == 'primary':
            # Rising-falling contour for stressed syllables
            rise = np.linspace(0.8, 1.2, samples // 2)
            fall = np.linspace(1.2, 0.9, samples - samples // 2)
            curve = np.concatenate([rise, fall])
        elif stress == 'secondary':
            # Slight rise for secondary stress
            curve = np.linspace(0.9, 1.05, samples)
        else:
            # Neutral for unstressed
            curve = np.ones(samples)
        
        return audio * curve
    
    def synthesize_phrase(self, text: str, voice_type: str = 'male', 
                         phoneme_map: Optional[Dict] = None) -> np.ndarray:
        """Synthesize a phrase into audio"""
        if phoneme_map is None:
            phoneme_map = self._create_default_phoneme_map()
        
        audio_segments = []
        syllables = text.replace('-', ' ').split()
        
        for syllable in syllables:
            if syllable in phoneme_map:
                phoneme = phoneme_map[syllable]
                
                # Generate tone
                tone = self.generate_tone(phoneme.pitch, phoneme.duration)
                
                # Apply Vedic intonation
                tone = self.apply_vedic_intonation(tone, phoneme.stress)
                
                # Adjust for voice profile
                voice = self.voice_profiles[voice_type]
                pitch_factor = voice.pitch / 120  # Normalize to male baseline
                tone = self._adjust_pitch(tone, pitch_factor)
                
                audio_segments.append(tone)
                
                # Add brief silence between syllables
                silence = np.zeros(int(0.1 * self.sample_rate))
                audio_segments.append(silence)
        
        # Combine all segments
        if audio_segments:
            combined = np.concatenate(audio_segments)
            # Normalize to prevent clipping
            max_val = np.max(np.abs(combined))
            if max_val > 0:
                combined = combined / max_val * 0.8
            return combined
        return np.array([])
    
    def _adjust_pitch(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """Adjust pitch of audio by resampling"""
        if factor == 1.0:
            return audio
        
        # Simple pitch shift by resampling
        indices = np.arange(0, len(audio), factor)
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]
    
    def save_wav(self, audio: np.ndarray, output_path: str):
        """Save audio as WAV file"""
        # Convert to 16-bit PCM
        audio_int = (audio * 32767).astype(np.int16)
        wavfile.write(output_path, self.sample_rate, audio_int)
        print(f"Saved audio to: {output_path}")
    
    def process_inscription(self, inscription_id: str, output_dir: str = 'audio_output'):
        """Process a decoded inscription into audio"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Example inscriptions from the decoder
        inscriptions = {
            'H-1': {'text': 'ta ka', 'voice': 'male', 'context': 'Name/title'},
            'M-3': {'text': 'sa ma ka ka na', 'voice': 'female', 'context': 'Administrative'}
        }
        
        if inscription_id not in inscriptions:
            print(f"Inscription {inscription_id} not found")
            return
        
        insc = inscriptions[inscription_id]
        print(f"Processing {inscription_id}: {insc['text']}")
        print(f"Context: {insc['context']}")
        print(f"Voice: {insc['voice']}")
        
        # Synthesize audio
        audio = self.synthesize_phrase(insc['text'], insc['voice'])
        
        # Save output
        output_path = os.path.join(output_dir, f"{inscription_id}_indus_valley.wav")
        self.save_wav(audio, output_path)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Brett Sound Simulator for Indus Valley Proto-Sanskrit'
    )
    parser.add_argument('--inscription', '-i', help='Inscription ID (e.g., H-1, M-3)')
    parser.add_argument('--text', '-t', help='Custom text to synthesize (e.g., "ta ka ra")')
    parser.add_argument('--voice', '-v', choices=['male', 'female', 'child'], 
                       default='male', help='Voice profile')
    parser.add_argument('--output', '-o', default='audio_output', 
                       help='Output directory')
    parser.add_argument('--phoneme-map', '-p', help='Path to phoneme CSV file')
    
    args = parser.parse_args()
    
    simulator = IndusValleySoundSimulator()
    
    if args.inscription:
        # Process specific inscription
        simulator.process_inscription(args.inscription, args.output)
    elif args.text:
        # Process custom text
        os.makedirs(args.output, exist_ok=True)
        
        phoneme_map = None
        if args.phoneme_map:
            phoneme_map = simulator.load_phoneme_map(args.phoneme_map)
        
        print(f"Synthesizing: {args.text}")
        print(f"Voice: {args.voice}")
        
        audio = simulator.synthesize_phrase(args.text, args.voice, phoneme_map)
        output_path = os.path.join(args.output, f"custom_indus_valley.wav")
        simulator.save_wav(audio, output_path)
    else:
        # Process all available inscriptions
        print("Processing all available inscriptions...")
        for insc_id in ['H-1', 'M-3']:
            simulator.process_inscription(insc_id, args.output)

if __name__ == "__main__":
    main()
