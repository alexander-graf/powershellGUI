import sys
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a text edit widget to display the PowerShell output
        self.output_widget = QTextEdit(self)
        self.output_widget.setReadOnly(True)

        # Create a layout and set the text edit widget as the central widget
        layout = QVBoxLayout()
        layout.addWidget(self.output_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a process for running PowerShell
        self.powershell_process = QProcess(self)
        self.powershell_process.setProgram("pwsh.exe")
        self.powershell_process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        # Connect the readyReadStandardOutput signal to handle the PowerShell output
        self.powershell_process.readyReadStandardOutput.connect(self.handle_output)

        # Start the PowerShell process
        self.powershell_process.start()

    def handle_output(self):
        # Read the output from the PowerShell process
        output = self.powershell_process.readAllStandardOutput()

        # Convert the output QByteArray to a Python string
        output_str = str(output.data(), encoding='utf-8')

        # Append the output to the text edit widget
        self.output_widget.append(output_str)

    def closeEvent(self, event):
        # Terminate the PowerShell process when the application is closed
        self.powershell_process.terminate()
        self.powershell_process.waitForFinished()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())