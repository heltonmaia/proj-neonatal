#!/usr/bin/env python3
"""
Video Conversion Module for Neonatal Analyzer

This module provides functionality to recursively convert video files to lower resolution
for efficient processing in the neonatal behavior analysis system.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VideoConverter:
    """
    A class to handle batch video conversion operations.
    
    This class provides methods to convert video files to lower resolution
    while maintaining aspect ratio and audio quality.
    """
    
    def __init__(self, target_directory: str = "./dataset_v1_low"):
        """
        Initialize the VideoConverter.
        
        Args:
            target_directory (str): Directory containing videos to process
        """
        self.target_directory = Path(target_directory)
        self.supported_formats = ['.mp4', '.mov', '.mkv', '.avi']
        self.total_files = 0
        self.success_count = 0
        self.fail_count = 0
    
    def check_ffmpeg_installation(self) -> bool:
        """
        Check if ffmpeg is installed and available in PATH.
        
        Returns:
            bool: True if ffmpeg is available, False otherwise
        """
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("ffmpeg is not installed or not in PATH")
            logger.error("Install with: sudo apt install ffmpeg (Ubuntu/Debian)")
            return False
    
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
    
    def process_single_video(self, video_path: Path) -> bool:
        """
        Process a single video file for conversion.
        
        Args:
            video_path (Path): Path to the video file
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Generate output filename
            output_path = video_path.parent / f"{video_path.stem}_low{video_path.suffix}"
            
            logger.info(f"Processing: {video_path}")
            logger.info(f"  Converting to: {output_path.name}")
            
            # FFmpeg command for conversion
            cmd = [
                'ffmpeg', '-nostdin', '-i', str(video_path),
                '-vf', 'scale=640:-2',  # Scale to 640px width, maintain aspect ratio
                '-c:a', 'copy',         # Copy audio without re-encoding
                str(output_path),
                '-hide_banner', '-loglevel', 'error', '-y'
            ]
            
            # Execute conversion
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
                logger.info("  ✓ Conversion successful!")
                logger.info("  Removing original file...")
                video_path.unlink()  # Remove original file
                logger.info("  ✓ Original file removed")
                return True
            else:
                logger.error("  ✗ Error: output file not created correctly")
                if output_path.exists():
                    output_path.unlink()  # Clean up failed output
                return False
                
        except Exception as e:
            logger.error(f"  ✗ Error during conversion: {e}")
            return False
    
    def find_video_files(self) -> list[Path]:
        """
        Find all video files in the target directory, excluding already processed ones.
        
        Returns:
            list[Path]: List of video file paths to process
        """
        video_files = []
        
        for ext in self.supported_formats:
            # Find all files with supported extensions
            pattern = f"*{ext}"
            for video_file in self.target_directory.rglob(pattern):
                # Skip files that already have '_low' in the name
                if '_low' not in video_file.stem:
                    video_files.append(video_file)
        
        return video_files
    
    def convert_all_videos(self) -> Dict[str, Any]:
        """
        Convert all eligible video files in the target directory.
        
        Returns:
            Dict[str, Any]: Summary of conversion results
        """
        if not self.check_ffmpeg_installation():
            return {"success": False, "error": "ffmpeg not available"}
        
        if not self.validate_directory():
            return {"success": False, "error": "Invalid directory"}
        
        logger.info(f"Starting recursive conversion in: {self.target_directory}")
        logger.info("=" * 50)
        
        video_files = self.find_video_files()
        self.total_files = len(video_files)
        
        logger.info(f"Found {self.total_files} video files to process")
        
        # Process each video file
        for video_file in video_files:
            if self.process_single_video(video_file):
                self.success_count += 1
            else:
                self.fail_count += 1
        
        # Generate final report
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a summary report of the conversion process.
        
        Returns:
            Dict[str, Any]: Conversion summary statistics
        """
        logger.info("")
        logger.info("=" * 50)
        logger.info("Final Report:")
        logger.info(f"Total eligible files found: {self.total_files}")
        logger.info(f"Successful conversions: {self.success_count}")
        logger.info(f"Failed conversions: {self.fail_count}")
        
        success = self.fail_count == 0
        if success:
            logger.info("All conversions completed successfully!")
        else:
            logger.warning("Some conversions failed.")
        
        return {
            "success": success,
            "total_files": self.total_files,
            "successful": self.success_count,
            "failed": self.fail_count
        }


def main():
    """Main function to run the video conversion process."""
    # Configuration - change this to your desired directory
    TARGET_DIR = "./dataset_v1_low"
    
    converter = VideoConverter(TARGET_DIR)
    result = converter.convert_all_videos()
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
