import os
import shutil
import pretty_midi
import matplotlib.pyplot as plt


# MIDI File Loading and Analysis Functions
def load_midi(file_path):
    """
    Load a MIDI file and return the PrettyMIDI object.
    Handles errors gracefully.
    """
    try:
        midi_data = pretty_midi.PrettyMIDI(file_path)
        return midi_data
    except Exception as e:
        print(f"Error loading MIDI file {file_path}: {e}")
        return None


def get_instrument_info(midi_data):
    """
    Extract instrument information from a MIDI file.
    """
    instruments = []
    for instrument in midi_data.instruments:
        instruments.append({
            'name': instrument.name or f"Program {instrument.program}",
            'program': instrument.program
        })
    return instruments


def pitch_to_note_name(pitch):
    """
    Convert MIDI pitch number to a human-readable note name.
    """
    return pretty_midi.note_number_to_name(pitch)


def extract_notes(midi_data):
    """
    Extract note information from a MIDI file, including pitch, start, end, and instrument.
    """
    note_data = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            note_data.append({
                'pitch': note.pitch,
                'note_name': pitch_to_note_name(note.pitch),
                'start': note.start,
                'end': note.end,
                'instrument': instrument.name or f"Program {instrument.program}"
            })
    return note_data


def visualize_notes(midi_data, save_path=None):
    """
    Visualize notes from a MIDI file as a scatter plot.
    Optionally save the plot to a file.
    """
    for instrument in midi_data.instruments:
        start_times = [note.start for note in instrument.notes]
        pitches = [note.pitch for note in instrument.notes]
        plt.scatter(start_times, pitches, label=instrument.name or f"Program {instrument.program}")
    plt.xlabel('Start Time (s)')
    plt.ylabel('MIDI Pitch')
    plt.title('MIDI Note Events')
    plt.legend()
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()


# Dataset Management Functions
def list_artist_folders(directory, filter_keyword=None):
    """
    List all artist folders in a given directory.
    Optionally filter folders by a keyword.
    """
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []
    folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    if filter_keyword:
        folders = [name for name in folders if filter_keyword.lower() in name.lower()]
    return folders


def copy_midi_files(source_dir, target_dir, artist=None):
    """
    Copy MIDI files from the source directory to the target directory.
    If an artist is specified, only copy files from that artist's folder.
    """
    if artist:
        artist_path = os.path.join(source_dir, artist)
        if not os.path.exists(artist_path):
            print(f"Artist '{artist}' does not exist in {source_dir}.")
            return
        midi_files = [f for f in os.listdir(artist_path) if f.endswith('.mid')]
        for midi_file in midi_files:
            print(f"Copying {midi_file}...")
            shutil.copy(os.path.join(artist_path, midi_file), target_dir)
        print(f"Copied {len(midi_files)} files for artist '{artist}'.")
    else:
        # Copy all MIDI files from all artist folders
        total_files = 0
        for folder in os.listdir(source_dir):
            folder_path = os.path.join(source_dir, folder)
            if os.path.isdir(folder_path):
                midi_files = [f for f in os.listdir(folder_path) if f.endswith('.mid')]
                for midi_file in midi_files:
                    print(f"Copying {midi_file} from folder {folder}...")
                    shutil.copy(os.path.join(folder_path, midi_file), target_dir)
                    total_files += 1
        print(f"Copied {total_files} files from all artist folders.")


def create_directory(directory):
    """
    Create a directory if it does not exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")
