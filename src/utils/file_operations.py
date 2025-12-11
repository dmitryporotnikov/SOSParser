#!/usr/bin/env python3
"""File operation utilities for SOSReport analyzer"""

import tarfile
import gzip
import bz2
from pathlib import Path
from utils.logger import Logger


def extract_tarball(tarball_path: Path, extract_to: Path) -> Path:
    """
    Extract a tarball (tar, tar.gz, tar.xz, tar.bz2) to target directory.
    Returns the path to the extracted sosreport directory.
    """
    Logger.info(f"Extracting tarball: {tarball_path}")
    
    try:
        with tarfile.open(tarball_path, 'r:*') as tar:
            # Extract all files
            tar.extractall(path=extract_to)
            
            # Find the root sosreport directory
            members = tar.getmembers()
            if members:
                # Get the top-level directory name
                root_name = members[0].name.split('/')[0]
                extracted_dir = extract_to / root_name
                
                if extracted_dir.exists():
                    Logger.debug(f"Extracted to: {extracted_dir}")
                    return extracted_dir
        
        Logger.error("Could not find extracted sosreport directory")
        raise Exception("Extraction failed: no root directory found")
        
    except Exception as e:
        Logger.error(f"Failed to extract tarball: {e}")
        raise


def validate_tarball(tarball_path: Path) -> bool:
    """Validate that the file is a valid tarball"""
    Logger.debug(f"Validating tarball: {tarball_path}")
    
    if not tarball_path.exists():
        raise FileNotFoundError(f"Tarball not found: {tarball_path}")
    
    if not tarball_path.is_file():
        raise ValueError(f"Not a file: {tarball_path}")
    
    # Try to open as tarball
    try:
        with tarfile.open(tarball_path, 'r:*') as tar:
            # Just check if we can read the first member
            members = tar.getmembers()
            if not members:
                raise ValueError("Tarball is empty")
        Logger.debug("Tarball validation successful")
        return True
    except Exception as e:
        Logger.error(f"Tarball validation failed: {e}")
        raise ValueError(f"Invalid tarball: {e}")


def get_sosreport_timestamp(tarball_path: Path) -> str:
    """Get timestamp from sosreport filename or file mtime"""
    try:
        # Try to parse from filename
        # sosreport-hostname-YYYY-MM-DD-random.tar.xz
        name = tarball_path.stem
        if '.tar' in name:
            name = name.split('.tar')[0]
        
        parts = name.split('-')
        # Look for date pattern YYYY-MM-DD or YYYYMMDD
        for i in range(len(parts) - 2):
            if len(parts[i]) == 4 and parts[i].isdigit():
                if len(parts[i+1]) == 2 and len(parts[i+2]) == 2:
                    date_str = f"{parts[i]}-{parts[i+1]}-{parts[i+2]}"
                    return date_str
        
        # Fallback to file modification time
        from datetime import datetime
        mtime = tarball_path.stat().st_mtime
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
    except Exception:
        return "Unknown"
