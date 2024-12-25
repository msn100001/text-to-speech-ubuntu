
# Text-to-Speech Application

A Python-based text-to-speech application using `espeak` and `PyQt6`. This software provides a graphical interface for converting text to speech with options to adjust speed, pitch, and volume. It also features HTML text normalization, cursor-based playback, and more.

---

## Features

### Core Functionality
- **Text-to-Speech**: Convert any text input into speech using the `espeak` command-line tool.
- **Start from Cursor**: Speech begins from the current cursor position in the text editor.
- **Pause/Resume**: Pause and resume speech playback.
- **Stop**: Stop speech playback at any point.

### Additional Features
- **Sweep Button**: Clears all text from the input field.
- **HTML Normalization**: Automatically strips out HTML tags from pasted content.
- **Character Counter**: Displays the number of characters in the text editor.
- **Adjustable Sliders**:
  - **Speed**: Control the speed of speech (range: 80–450).
  - **Pitch**: Adjust the pitch of the voice (range: 0–99).
  - **Volume**: Set the volume of the voice (range: 0–200).

---

## Dependencies

### Required Software
- **Python 3.x**: Make sure Python 3.x is installed on your system.
- **espeak**: A speech synthesizer command-line tool.
- **PyQt6**: A Python library for creating graphical user interfaces.

---

## Installation

### 1. Install Python 3.x
Most Linux systems come with Python pre-installed. To verify, run:
```bash
python3 --version
```

If not installed, install Python 3.x:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Install `espeak`
Install `espeak` for text-to-speech functionality:
```bash
sudo apt install espeak
```

### 3. Install `PyQt6`
Install the `PyQt6` library using pip:
```bash
pip install PyQt6
```

---

## Usage

### Running the Program
1. Save the script as `tts.py` or another filename of your choice.
2. Make the script executable:
   ```bash
   chmod +x tts.py
   ```
3. Run the script:
   ```bash
   ./tts.py
   ```

### GUI Functionality
- **Enter Text**: Type or paste text into the text box.
- **Adjust Sliders**: Use the sliders to modify speech speed, pitch, and volume.
- **Speak**: Click the **Speak** button to start text-to-speech.
- **Pause/Resume**: Use the **Pause** and **Resume** buttons to control playback.
- **Stop**: Stop speech playback at any time.
- **Sweep**: Clear all text from the input field using the **Sweep** button.

---

## Troubleshooting

### Common Issues
1. **`espeak` Not Found**:
   Ensure `espeak` is installed:
   ```bash
   sudo apt install espeak
   ```
2. **Missing PyQt6**:
   Install it using pip:
   ```bash
   pip install PyQt6
   ```
3. **Program Does Not Start**:
   Check for Python errors by running the script directly:
   ```bash
   python3 tts.py
   ```

---

## Contributions
Contributions are welcome! Please open a pull request or submit an issue if you encounter bugs or have feature suggestions.

---

## License
This project is open-source and available under the MIT License.
