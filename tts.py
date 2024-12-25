#!/usr/bin/python3
import sys
import subprocess
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QSlider, QLabel, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer


class NormalizedTextEdit(QTextEdit):
    """Custom QTextEdit that removes HTML tags from pasted content."""
    def insertFromMimeData(self, source):
        if source.hasHtml():
            html = source.html()
            plain_text = self.strip_html_tags(html)
            self.setPlainText(plain_text)
        elif source.hasText():
            text = source.text()
            self.setPlainText(text)
        else:
            super().insertFromMimeData(source)

    @staticmethod
    def strip_html_tags(html):
        """Remove all HTML tags and return plain text."""
        text = re.sub(r"<[^>]+>", "", html)
        return re.sub(r"\s+", " ", text.strip())


class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text to Speech")
        self.setGeometry(100, 100, 500, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Textbox with character counter
        self.textbox = NormalizedTextEdit(self)
        self.textbox.setPlaceholderText("Paste text here. HTML will be removed automatically.")
        self.textbox.textChanged.connect(self.update_character_count)
        layout.addWidget(self.textbox)

        # Character counter
        self.char_counter_label = QLabel("Characters: 0", self)
        layout.addWidget(self.char_counter_label)

        # Speed Slider
        layout.addLayout(self.create_slider_layout("Speed", 80, 450, 280, self.update_speed_label))

        # Pitch Slider
        layout.addLayout(self.create_slider_layout("Pitch", 0, 99, 40, self.update_pitch_label))

        # Volume Slider
        layout.addLayout(self.create_slider_layout("Volume", 0, 200, 100, self.update_volume_label))

        # Buttons layout
        button_layout = QHBoxLayout()

        # Speak Button
        self.button_speak = QPushButton("💬 Speak", self)
        self.button_speak.clicked.connect(self.speak_text_from_cursor)
        self.button_speak.setFixedHeight(60)
        button_layout.addWidget(self.button_speak)

        # Pause Button
        self.button_pause = QPushButton("⏸ Pause", self)
        self.button_pause.clicked.connect(self.pause_speaking)
        self.button_pause.setFixedHeight(60)
        self.button_pause.setEnabled(False)
        button_layout.addWidget(self.button_pause)

        # Resume Button
        self.button_resume = QPushButton("▶ Resume", self)
        self.button_resume.clicked.connect(self.resume_speaking)
        self.button_resume.setFixedHeight(60)
        self.button_resume.setEnabled(False)
        button_layout.addWidget(self.button_resume)

        # Stop Button
        self.button_stop = QPushButton("🛑 Stop", self)
        self.button_stop.clicked.connect(self.stop_speaking)
        self.button_stop.setFixedHeight(60)
        button_layout.addWidget(self.button_stop)

        # Sweep Button
        self.button_sweep = QPushButton("🧹 Sweep", self)
        self.button_sweep.clicked.connect(self.clear_textbox)
        self.button_sweep.setFixedHeight(60)
        button_layout.addWidget(self.button_sweep)

        layout.addLayout(button_layout)

        # State variables
        self.espeak_process = None
        self.is_paused = False
        self.timer = QTimer()

    def create_slider_layout(self, label, min_value, max_value, default_value, callback):
        """Creates a slider layout with a label."""
        layout = QHBoxLayout()
        slider_label = QLabel(f"{label}: {default_value}")
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(default_value)
        slider.valueChanged.connect(lambda value: slider_label.setText(f"{label}: {value}"))
        slider.valueChanged.connect(callback)
        layout.addWidget(slider_label)
        layout.addWidget(slider)
        setattr(self, f"{label.lower()}_slider", slider)
        setattr(self, f"{label.lower()}_slider_label", slider_label)
        return layout

    def update_character_count(self):
        """Update the character counter based on text length."""
        char_count = len(self.textbox.toPlainText())
        self.char_counter_label.setText(f"Characters: {char_count}")

    def update_speed_label(self):
        """Handle speed slider changes."""
        pass

    def update_pitch_label(self):
        """Handle pitch slider changes."""
        pass

    def update_volume_label(self):
        """Handle volume slider changes."""
        pass

    def clear_textbox(self):
        """Clear all text from the textbox."""
        self.textbox.clear()

    def normalize_text(self, text):
        """Normalize the input text to remove inconsistencies."""
        text = re.sub(r"\s+", " ", text.strip())
        text = re.sub(r"[^\w\s.,!?'-]", "", text)
        return text

    def speak_text_from_cursor(self):
        """Speak text starting from the current cursor position."""
        cursor = self.textbox.textCursor()
        start_pos = cursor.position()
        raw_text = self.textbox.toPlainText()

        # Extract text starting from the cursor position
        text_from_cursor = raw_text[start_pos:].strip()
        if not text_from_cursor:
            QMessageBox.warning(self, "Error", "No text available to speak from the cursor position.")
            return

        normalized_text = self.normalize_text(text_from_cursor)

        speed = self.speed_slider.value()
        pitch = self.pitch_slider.value()
        volume = self.volume_slider.value()

        self.stop_speaking()

        try:
            espeak_cmd = ["espeak", f"-s{speed}", f"-p{pitch}", f"-a{volume}", normalized_text]
            print("Executing command:", " ".join(espeak_cmd))  # Debug log
            self.espeak_process = subprocess.Popen(
                espeak_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.button_speak.setEnabled(False)
            self.button_pause.setEnabled(True)
            self.timer.timeout.connect(self.check_process)
            self.timer.start(100)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "espeak command not found. Please ensure espeak is installed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def check_process(self):
        """Check if the espeak process has finished."""
        if self.espeak_process and self.espeak_process.poll() is not None:
            self.timer.stop()
            self.stop_speaking()
            self.textbox.moveCursor(self.textbox.textCursor().Start)  # Reset cursor to the start of the text

    def pause_speaking(self):
        if self.espeak_process and not self.is_paused:
            self.espeak_process.send_signal(subprocess.signal.SIGSTOP)
            self.is_paused = True
            self.button_pause.setEnabled(False)
            self.button_resume.setEnabled(True)

    def resume_speaking(self):
        if self.espeak_process and self.is_paused:
            self.espeak_process.send_signal(subprocess.signal.SIGCONT)
            self.is_paused = False
            self.button_pause.setEnabled(True)
            self.button_resume.setEnabled(False)

    def stop_speaking(self):
        if self.espeak_process:
            self.espeak_process.terminate()
            self.espeak_process.wait()
            self.espeak_process = None
        self.button_speak.setEnabled(True)
        self.button_pause.setEnabled(False)
        self.button_resume.setEnabled(False)
        self.is_paused = False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Check if espeak is installed
    if subprocess.run(["which", "espeak"], stdout=subprocess.DEVNULL).returncode != 0:
        QMessageBox.critical(None, "Error", "espeak is not installed. Please install it and try again.")
        sys.exit(1)

    main_window = TextToSpeechApp()
    main_window.show()
    sys.exit(app.exec())
