from utils import (
    load_midi,
    get_instrument_info,
    extract_notes,
    visualize_notes,
    create_directory,
    copy_midi_files,
    list_artist_folders
)

# Part 1: MIDI File Analysis
# -----------------------------------
print("=== MIDI File Analysis ===")
midi_file = "/path/to/your/midi/file.mid"  # Replace with an actual file path
midi_data = load_midi(midi_file)

if midi_data:
    # Get instrument info
    instruments = get_instrument_info(midi_data)
    print("Instruments:", instruments)

    # Extract notes
    notes = extract_notes(midi_data)
    for note in notes[:10]:  # Print only the first 10 notes for brevity
        print(note)

    # Visualize notes
    visualize_notes(midi_data)
else:
    print(f"Could not load MIDI file: {midi_file}")

# Part 2: Dataset Management
# -----------------------------------
print("\n=== Dataset Management ===")

# Define paths
source_dir = "/Users/dally/Documents/github/midi_gen-AI/datasets/lakh/clean_midi"
target_dir = "/Users/dally/Documents/github/midi_gen-AI/datasets/lakh/processed"

# Step 1: Create the target directory
print(f"Creating target directory at: {target_dir}")
create_directory(target_dir)

# Step 2: List all available artist folders
print("Listing all available artist folders...")
artist_folders = list_artist_folders(source_dir)
if artist_folders:
    print(f"Found {len(artist_folders)} artist folders:")
    print(artist_folders)
else:
    print("No artist folders found! Check the source directory path.")

# Step 3: Copy files from a specific artist
artist_name = "ABBA"  # Replace with the desired artist name
print(f"Copying MIDI files for artist: {artist_name}")
copy_midi_files(source_dir, target_dir, artist=artist_name)

# Step 4: Optionally, copy all files
# Uncomment the following lines to copy all files from all artist folders
# print("Copying all MIDI files from all artist folders...")
# copy_midi_files(source_dir, target_dir)

print(f"Dataset processing completed. Check the target directory: {target_dir}")
