"""
Utility.py
Created November 1, 2020

General purpose functionality to extend Python and use
throughout the code base (i.e. from Utility import *).
"""
import sys, os, platform

onMacOS = platform.system() == "Darwin"

def helloWorld():
    return "Hello, world!"
