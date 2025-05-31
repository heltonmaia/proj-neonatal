#!/usr/bin/env python3
"""
Dataset Spreadsheet Generator for Neonatal Analyzer

This module generates CSV spreadsheets containing information about video files
in the dataset for annotation and analysis purposes.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Any
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SpreadsheetGenerator:
    """
    A class to generate CSV spreadsheets from video dataset information.
    """
    
    def __init__(self, target_directory: str = "./dataset_v1_low", 
                 output_filename: str = "dataset_info.csv"):
        """
        Initialize the SpreadsheetGenerator.
        """
        self.target_directory = Path(target_directory)
        self.output_filename = output_filename
        self.supported_formats = ['.mp4', '.mov', '.mkv', '.avi']
        self.video_files_found = 0
    
    def validate_directory(self) -> bool:
        """
        Validate if the target directory exists.
        """
        if not self.target_directory.exists():
            logger.error(f"Directory '{self.target_directory}' not found!")
            return False
        return True
    
    def find_processed_videos(self) -> List[Path]:
        """
        Find all processed video files (containing '_low' in filename).
        """
        video_files = []
        
        for ext in self.supported_formats:
            pattern = f"*_low{ext}"
            for video_file in self.target_directory.rglob(pattern):
                video_files.append(video_file)
        
        video_files.sort()
        return video_files
    
    def get_relative_path(self, file_path: Path) -> str:
        """
        Get the relative path from the target directory.
        """
        try:
            relative_path = file_path.relative_to(Path.cwd())
            path_str = str(relative_path)
            if path_str.startswith('./'):
                path_str = path_str[2:]
            return path_str
        except ValueError:
            return str(file_path)
    
    def get_video_duration(self, file_path: Path) -> float:
        """
        Get video duration in seconds using ffprobe.
        """
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(file_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
            return duration
        except Exception as e:
            logger.error(f"Could not get duration for {file_path}: {e}")
            return 0.0
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata including file size and duration.
        """
        metadata = {}
        
        # File size in MB
        try:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            metadata['size_mb'] = f"{size_mb:.2f}"
        except OSError:
            metadata['size_mb'] = "unknown"
        
        # Video duration in seconds
        duration = self.get_video_duration(file_path)
        metadata['duration_seconds'] = f"{duration:.2f}"
        
        return metadata
    
    def generate_csv(self) -> Dict[str, Any]:
        """
        Generate the CSV spreadsheet with video file information.
        """
        if not self.validate_directory():
            return {"success": False, "error": "Invalid directory"}
        
        logger.info("Generating CSV spreadsheet with found videos...")
        logger.info(f"Output: {self.output_filename}")
        
        video_files = self.find_processed_videos()
        self.video_files_found = len(video_files)
        
        if self.video_files_found == 0:
            logger.warning("No processed video files found!")
            return {"success": False, "error": "No video files found"}
        
        try:
            with open(self.output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'file_path',
                    'size_mb',
                    'duration_seconds'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for video_file in video_files:
                    relative_path = self.get_relative_path(video_file)
                    metadata = self.extract_metadata(video_file)
                    
                    row = {
                        'file_path': relative_path,
                        'size_mb': metadata['size_mb'],
                        'duration_seconds': metadata['duration_seconds']
                    }
                    
                    writer.writerow(row)
            
            logger.info(f"CSV generated successfully: {self.output_filename}")
            logger.info(f"Total video files cataloged: {self.video_files_found}")
            
            return {
                "success": True,
                "output_file": self.output_filename,
                "videos_found": self.video_files_found
            }
            
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            return {"success": False, "error": str(e)}


def main():
    """Main function to run the spreadsheet generation process."""
    TARGET_DIR = "./dataset_v1_low"
    OUTPUT_CSV = "dataset_info.csv"
    
    generator = SpreadsheetGenerator(TARGET_DIR, OUTPUT_CSV)
    result = generator.generate_csv()
    
    if not result["success"]:
        logger.error(f"Failed to generate spreadsheet: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()