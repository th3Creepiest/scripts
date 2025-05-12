import os
import numpy as np
import librosa
import pretty_midi


def audio_to_midi(audio_path, output_midi_path):
    """
    Converts an audio file (e.g., MP3) to a basic MIDI file.

    Args:
        audio_path (str): Path to the input audio file.
        output_midi_path (str): Path to save the output MIDI file.
    """
    print(f"Loading audio file: {audio_path}")
    try:
        y, sr = librosa.load(audio_path)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        print(
            "Please ensure ffmpeg is installed and in your system's PATH if you are using MP3 files."
        )
        return

    print("Detecting note onsets...")
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")

    if len(onsets) == 0:
        print("No onsets detected. Cannot create MIDI file.")
        return

    print(f"Detected {len(onsets)} onsets.")

    print("Estimating pitches...")
    # For simplicity, we'll assign a fixed pitch (C4) to each onset for now.
    # A more advanced approach would involve pitch tracking (e.g., librosa.pyin or crepe).
    # We'll also estimate pitches for segments between onsets.
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    midi_data = pretty_midi.PrettyMIDI()
    instrument_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    instrument = pretty_midi.Instrument(program=instrument_program)

    # Create notes based on onsets and estimated pitches
    for i in range(len(onsets)):
        start_time = onsets[i]
        end_time = (
            onsets[i + 1] if i + 1 < len(onsets) else start_time + 0.5
        )  # Default duration for last note

        # Get the pitch for the segment
        # Find the pitch with the maximum magnitude in the frame closest to the onset time
        onset_frame = librosa.time_to_frames(start_time, sr=sr)
        pitch_values_at_onset = pitches[:, onset_frame]
        magnitude_values_at_onset = magnitudes[:, onset_frame]

        # Filter out zero pitches and find the dominant pitch
        valid_pitch_indices = np.where(pitch_values_at_onset > 0)[0]
        if len(valid_pitch_indices) > 0:
            dominant_pitch_index = valid_pitch_indices[
                np.argmax(magnitude_values_at_onset[valid_pitch_indices])
            ]
            pitch_hz = pitches[dominant_pitch_index, onset_frame]
            midi_note_number = librosa.hz_to_midi(pitch_hz)
            # Ensure midi_note_number is an integer and within valid MIDI range (0-127)
            midi_note_number = int(float(np.clip(midi_note_number, 0, 127)))
            velocity = 100  # Fixed velocity
        else:
            # If no pitch detected, use a default (e.g., C4) or skip
            midi_note_number = 60  # MIDI C4
            velocity = 0  # Or a low velocity to indicate silence/uncertainty

        if velocity > 0:
            note = pretty_midi.Note(
                velocity=velocity,
                pitch=midi_note_number,
                start=start_time,
                end=end_time,
            )
            instrument.notes.append(note)

    midi_data.instruments.append(instrument)

    try:
        midi_data.write(output_midi_path)
        print(f"MIDI file saved to: {output_midi_path}")
    except Exception as e:
        print(f"Error writing MIDI file: {e}")


if __name__ == "__main__":
    directory = input("Enter directory path: ")
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            audio_file = os.path.join(directory, file)
            midi_out = os.path.splitext(audio_file)[0] + ".mid"
            audio_to_midi(audio_file, midi_out)
