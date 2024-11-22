import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QFileDialog, QTextEdit

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Python IDE")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
    
    def initUI(self):
        # Create main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Set the layout for the main widget
        layout = QVBoxLayout()
        
        # Code Editor area (PlainTextEdit for the code input)
        self.code_editor = QPlainTextEdit(self)
        self.code_editor.setPlaceholderText("Write your Python code here...")
        layout.addWidget(self.code_editor)
        
        # Output area (TextEdit for displaying execution results)
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)  # Make the output area read-only
        layout.addWidget(self.output_area)

        # Button to execute code
        self.run_button = QPushButton("Run Code", self)
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        # File management buttons (Open, Save)
        file_layout = QHBoxLayout()
        self.open_button = QPushButton("Open File", self)
        self.save_button = QPushButton("Save File", self)
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        
        file_layout.addWidget(self.open_button)
        file_layout.addWidget(self.save_button)
        layout.addLayout(file_layout)

        # Set the main layout of the window
        main_widget.setLayout(layout)
    
    def run_code(self):
        # Get the code from the code editor
        code = self.code_editor.toPlainText()

        try:
            # Redirect output to the output area
            output = self.execute_code(code)
            self.output_area.setText(output)
        except Exception as e:
            self.output_area.setText(f"Error: {str(e)}")

    def execute_code(self, code):
        try:
            # Redirect standard output and error to capture print statements and errors
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = sys.stderr = StringIO()

            # Execute the code
            exec(code)

            # Get the output
            output = sys.stdout.getvalue()

            # Restore original stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return output if output else "Execution complete, no output."

        except Exception as e:
            return str(e)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as file:
                code = file.read()
                self.code_editor.setPlainText(code)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Python File", "", "Python Files (*.py);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as file:
                code = self.code_editor.toPlainText()
                file.write(code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())
