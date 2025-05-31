#!/usr/bin/env python3
"""
Data Normalization Module for Neonatal Analyzer

This module provides functionality to normalize file and directory names
by removing accents, special characters, and standardizing naming conventions.
"""

import os
import re
import unicodedata
from pathlib import Path
from typing import List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    A class to handle file and directory name normalization.
    
    This class provides methods to clean and standardize file/folder names
    by removing accents, special characters, and applying consistent naming rules.
    """
    
    def __init__(self, target_directory: str = "./dataset_v1"):
        """
        Initialize the DataNormalizer.
        
        Args:
            target_directory (str): Directory to process for name normalization
        """
        self.target_directory = Path(target_directory)
        self.files_processed = 0
        self.directories_processed = 0
    
    def normalize_name(self, name: str) -> str:
        """
        Normalize a filename or directory name according to standardized rules.
        
        Args:
            name (str): Original name to normalize
            
        Returns:
            str: Normalized name following the rules:
                - Convert to lowercase
                - Remove accents and diacritics  
                - Replace spaces and commas with underscores
                - Remove special characters (keep only alphanumeric, underscore, hyphen, dot)
                - Clean up multiple consecutive underscores
                - Remove leading/trailing underscores
        """
        # Convert to lowercase
        name = name.lower()
        
        # Remove accents and diacritics using Unicode normalization
        name = unicodedata.normalize('NFD', name)
        name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
        
        # Remove spaces before dots (e.g., "file .txt" → "file.txt")
        name = re.sub(r' +\.', '.', name)
        
        # Remove underscores before dots (e.g., "file_.txt" → "file.txt")  
        name = re.sub(r'_+\.', '.', name)
        
        # Replace spaces and commas with underscores
        name = re.sub(r'[ ,]+', '_', name)
        
        # Remove special characters (keep only alphanumeric, underscore, hyphen, dot)
        name = re.sub(r'[^a-z0-9_.-]', '', name)
        
        # Remove multiple consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Remove leading/trailing underscores, but preserve those before extensions
        name = re.sub(r'^_+', '', name)  # Remove leading underscores
        name = re.sub(r'_+$', '', name)  # Remove trailing underscores
        name = re.sub(r'_+\.', '.', name)  # Remove underscores before dots
        
        return name
    
    def validate_directory(self) -> bool:
        """
        Validate if the target directory exists.
        
        Returns:
            bool: True if directory exists, False otherwise
        """
        if not self.target_directory.exists():
            logger.error(f"Directory '{self.target_directory}' not found!")
            return False
        return True
    
    def process_files(self) -> List[Tuple[str, str]]:
        """
        Process and rename all files in the target directory recursively.
        
        Returns:
            List[Tuple[str, str]]: List of (old_name, new_name) tuples for renamed files
        """
        renamed_files = []
        
        # Process all files recursively
        for file_path in self.target_directory.rglob('*'):
            if file_path.is_file():
                old_name = file_path.name
                new_name = self.normalize_name(old_name)
                
                if old_name != new_name:
                    new_path = file_path.parent / new_name
                    try:
                        file_path.rename(new_path)
                        logger.info(f"Renamed file: {old_name} → {new_name}")
                        renamed_files.append((str(file_path), str(new_path)))
                        self.files_processed += 1
                    except OSError as e:
                        logger.error(f"Failed to rename file {old_name}: {e}")
        
        return renamed_files
    
    def process_directories(self) -> List[Tuple[str, str]]:
        """
        Process and rename all directories in the target directory recursively.
        
        Note: Directories are processed in reverse order (deepest first) to avoid
        path conflicts during renaming.
        
        Returns:
            List[Tuple[str, str]]: List of (old_path, new_path) tuples for renamed directories
        """
        renamed_dirs = []
        
        # Get all directories and sort by depth (deepest first)
        all_dirs = [d for d in self.target_directory.rglob('*') if d.is_dir()]
        all_dirs.sort(key=lambda x: len(x.parts), reverse=True)
        
        for dir_path in all_dirs:
            # Skip the root target directory itself
            if dir_path == self.target_directory:
                continue
                
            old_name = dir_path.name
            new_name = self.normalize_name(old_name)
            
            if old_name != new_name:
                new_path = dir_path.parent / new_name
                try:
                    dir_path.rename(new_path)
                    logger.info(f"Renamed directory: {old_name} → {new_name}")
                    renamed_dirs.append((str(dir_path), str(new_path)))
                    self.directories_processed += 1
                except OSError as e:
                    logger.error(f"Failed to rename directory {old_name}: {e}")
        
        return renamed_dirs
    
    def normalize_all(self) -> dict:
        """
        Normalize all files and directories in the target directory.
        
        Returns:
            dict: Summary of normalization results including counts and renamed items
        """
        if not self.validate_directory():
            return {"success": False, "error": "Invalid directory"}
        
        logger.info(f"Processing files and directories in: {self.target_directory}")
        
        # Process files first, then directories
        renamed_files = self.process_files()
        renamed_directories = self.process_directories()
        
        logger.info("Normalization completed!")
        logger.info(f"Files processed: {self.files_processed}")
        logger.info(f"Directories processed: {self.directories_processed}")
        
        return {
            "success": True,
            "files_processed": self.files_processed,
            "directories_processed": self.directories_processed,
            "renamed_files": renamed_files,
            "renamed_directories": renamed_directories
        }


def main():
    """Main function to run the data normalization process."""
    # Configuration - change this to your desired directory
    TARGET_DIR = "./dataset_v1"
    
    normalizer = DataNormalizer(TARGET_DIR)
    result = normalizer.normalize_all()
    
    if result["success"]:
        logger.info("Data normalization completed successfully!")
    else:
        logger.error(f"Data normalization failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
