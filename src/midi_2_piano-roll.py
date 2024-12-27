import os
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import argparse

def load_midi(file_path):
    try:
        midi_data = pretty_midi.PrettyMIDI(file_path)
        return midi_data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def extract_notes(midi_data):
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            notes.append({
                'pitch': note.pitch,
                'start': note.start,
                'end': note.end,
                'velocity': note.velocity,
                'instrument': instrument.name or f"Program {instrument.program}"
            })
    return notes

def notes_to_pianoroll(notes, time_step=0.05, num_pitches=128, separate_bars=False, tempo=120):
    max_time = max(note['end'] for note in notes)
    num_steps = int(np.ceil(max_time / time_step))
    pianoroll = np.zeros((num_steps, num_pitches), dtype=np.uint8)

    for note in notes:
        start_step = int(note['start'] / time_step)
        end_step = int(note['end'] / time_step)
        pitch = note['pitch']
        pianoroll[start_step:end_step, pitch] = note['velocity']

    if separate_bars:
        bar_length = 60 / tempo * 4  # 4/4 time signature
        bar_steps = int(bar_length / time_step)
        bars = [pianoroll[i:i+bar_steps] for i in range(0, len(pianoroll), bar_steps)]
        return pianoroll, bars

    return pianoroll, None

def save_pianoroll(data, save_path):
    data = {str(key): value for key, value in data.items()}  # Ensure all keys are strings
    np.savez_compressed(save_path, **data)
    print(f"Pianoroll saved to {save_path}")

def visualize_pianoroll(pianoroll):
    plt.figure(figsize=(12, 8))
    plt.imshow(pianoroll.T, aspect='auto', origin='lower', cmap='hot', interpolation='nearest')
    plt.colorbar(label='Velocity')
    plt.xlabel('Time Steps')
    plt.ylabel('MIDI Pitches')
    plt.title('Pianoroll Visualization')
    plt.show()

def convert_midi_to_pianoroll(args):
    input_dir = args.input_dir
    output_dir = args.output_dir
    time_step = args.time_step
    separate_bars = args.separate_bars

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for midi_file in os.listdir(input_dir):
        if midi_file.endswith('.mid'):
            input_path = os.path.join(input_dir, midi_file)
            output_path = os.path.join(output_dir, os.path.splitext(midi_file)[0] + '.npz')

            print(f"Processing {midi_file}...")
            midi_data = load_midi(input_path)

            if midi_data:
                notes = extract_notes(midi_data)
                pianoroll, bars = notes_to_pianoroll(notes, time_step=time_step, separate_bars=separate_bars)

                data = {'pianoroll': pianoroll}
                if bars is not None:
                    data['bars'] = np.array(bars, dtype=object)

                save_pianoroll(data, output_path)

def visualize_pianoroll_file(args):
    pianoroll_path = args.pianoroll_path
    data = np.load(pianoroll_path, allow_pickle=True)
    pianoroll = data['pianoroll']
    print(f"Pianoroll shape: {pianoroll.shape}")
    visualize_pianoroll(pianoroll)

def main():
    parser = argparse.ArgumentParser(description="Convert MIDI files to pianoroll format and visualize them.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for conversion
    convert_parser = subparsers.add_parser("convert", help="Convert MIDI to pianoroll")
    convert_parser.add_argument("input_dir", type=str, help="Directory containing MIDI files")
    convert_parser.add_argument("output_dir", type=str, help="Directory to save pianoroll files")
    convert_parser.add_argument("--time_step", type=float, default=0.05, help="Time step for pianoroll")
    convert_parser.add_argument("--separate_bars", action="store_true", help="Separate pianoroll into bars")

    # Subparser for visualization
    visualize_parser = subparsers.add_parser("visualize", help="Visualize pianoroll from .npz file")
    visualize_parser.add_argument("pianoroll_path", type=str, help="Path to the saved pianoroll .npz file")

    args = parser.parse_args()

    if args.command == "convert":
        convert_midi_to_pianoroll(args)
    elif args.command == "visualize":
        visualize_pianoroll_file(args)

if __name__ == "__main__":
    main()
