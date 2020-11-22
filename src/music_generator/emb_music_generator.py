import fractions
import pickle
from typing import List

import music21
import numpy as np
import pandas as pd
import tensorflow as tf

from .music_generator import MusicGenerator


class EmbMusicGenerator(MusicGenerator):
    def __init__(self, path_to_model: str, path_to_samples: str, path_to_tokenizer: str, random_state: int):
        self._samples: pd.DataFrame = pd.read_csv(path_to_samples)
        self._model = tf.keras.models.load_model(path_to_model)
        with open(path_to_tokenizer, "rb") as f:
            self._tokenizer: tf.keras.preprocessing.text.Tokenizer = pickle.load(f)
        np.random.seed(random_state)
        self._seq_len: int = len(self._samples["ChordDurationSeq"][0].split())

    def generate(self, elements_amount: int, file_name: str):
        generated_stream: music21.stream.Stream = music21.stream.Stream()
        generated_stream.append(music21.instrument.Piano())
        sample_idx: int = np.random.randint(0, 150)
        seed = np.array(
            [z for sublist in self._tokenizer.texts_to_sequences([self._samples["ChordDurationSeq"][sample_idx]]) for z
             in sublist]).reshape((-1, 100))
        for _ in range(elements_amount):
            predictions = self._model.predict(seed)
            next_element_idx: int = np.argsort(predictions)[0][-3:][np.random.randint(0, 3)]
            inp = np.roll(seed, -1)
            inp[0][0] = next_element_idx
            next_element, next_duration = self._tokenizer.sequences_to_texts([[next_element_idx]])[0].split("#")
            try:
                next_duration = float(next_duration)
            except Exception:
                next_duration = float(fractions.Fraction(next_duration))
            next_duration *= 4  # We have quoterLength in data
            if next_element == "rest":
                generated_stream.append(music21.note.Rest(duration=music21.duration.Duration(next_duration)))
                continue
            chord: List[int] = [int(v) for v in next_element.split('|')]
            if len(chord) > 1:
                generated_stream.append(music21.chord.Chord(chord, duration=music21.duration.Duration(next_duration)))
            else:
                generated_stream.append(music21.note.Note(chord[0], duration=music21.duration.Duration(next_duration)))
        generated_stream.write('midi', fp=file_name)
