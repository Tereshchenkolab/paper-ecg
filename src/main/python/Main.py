"""
Main.py
Created November 1, 2020

Entry point for the application
"""

import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from controllers.MainController import MainController


if __name__ == '__main__':
    context = ApplicationContext()

    # Translate asset paths to useable format for PyInstaller
    def resource(relativePath):
        return context.get_resource(relativePath)

    # Launch the main controller and window
    controller = MainController()

    # Hang
    exit_code = context.app.exec_()

    print(f"Exiting with status {exit_code}")
    sys.exit(exit_code)