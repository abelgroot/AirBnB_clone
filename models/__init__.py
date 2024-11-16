#!/usr/bin/python3
"""
This module defines create a unique FileStorage instance
"""

from models.engine.file_storage import FileStorage

# Create a unique FileStorage instance for the application and
# Call the reload() to load any existing serialized data
storage = FileStorage()
storage.reload()
