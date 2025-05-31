# 📁 Script Documentation - Datasets

This directory documents the scripts located in `datasets/scripts/` that perform essential steps in preparing and organizing data for the **Neonatal Analyzer** project.

---

## ✅ Available Scripts (Documented)

### `convert_videos.py`

**Function:** Converts all videos in a directory to a lower-resolution version (640px width) while preserving the original audio.

**Usage:**

```bash
python convert_videos.py
```

**Requirements:**

* `ffmpeg` installed (used for video conversion).

**Output:**

* Creates new files with `_low` suffix in the same directory as originals.
* Original files are removed after successful conversion.

**Notes:**

* Final resolution is adjusted to 640 pixels width with proportional height.
* Already converted files (with `_low` in name) are ignored.

---

### `data_normalizer.py`

**Function:** Standardizes file and folder names within a directory by removing accents, special characters, and spaces.

**Usage:**

```bash
python data_normalizer.py
```

**What the script does:**

* Renames files and folders to lowercase.
* Removes accents and replaces spaces/commas with `_`.
* Keeps only alphanumeric characters, `.`, `_`, and `-`.

**Example:**

```
"Vídeo 1, Bebê.mov" → "video_1_bebe.mov"
```

**Generated report:**

* Count of processed files and directories.
* List of names before and after renaming.

---

### `spreadsheet_generator.py`

**Function:** Creates a `.csv` file containing information about all converted videos in a directory.

**Usage:**

```bash
python spreadsheet_generator.py
```

**Requirements:**

* `ffprobe` (part of `ffmpeg`, used to get video duration).

**Output:**

* `dataset_info.csv` file containing:

  * `file_path`: Relative video path.
  * `size_mb`: File size in MB.
  * `duration_seconds`: Video duration in seconds.

**Notes:**

* The script looks for files with `_low` in their name.
* Returns error messages for invalid directories or missing videos.

---

## 📝 Recommended Execution Order

1. **Name normalization:**

```bash
python data_normalizer.py
```

2. **Video conversion:**

```bash
python convert_videos.py
```

3. **Metadata spreadsheet generation:**

```bash
python spreadsheet_generator.py
```