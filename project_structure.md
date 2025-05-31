# Neonatal Analyzer - Project Structure

```
proj_neonatal/
├── datasets/
│   ├── raw/                     # Raw data
│   │   ├── videos/              # Original videos
│   │   └── metadata/            # Video metadata
│   ├── processed/               # Processed data
│   │   ├── frames/              # Extracted frames
│   │   ├── features/            # Extracted features
│   │   └── annotations/         # Manual annotations
│   └── scripts/
│       ├── ✓ convert_videos.py        # Video conversion script
│       ├── ✓ data_normalizer.py       # Data cleaning/normalization
│       ├── ✓ spreadsheet_generator.py # Dataset spreadsheet generation
│       ├── extract_frames.py          # Frame extraction
│       ├── feature_extraction.py      # Feature extraction
│       └── data_split.py             # Data splitting
├── ml/
│   ├── models/
│   │   ├── yolov11/
│   │   │   ├── config/         # Configuration files
│   │   │   ├── weights/        # Model weights
│   │   └── other_models/      # Other models directory
│   └── scripts/                # Scripts for training and evaluation
└── docs/
    ├── datasets.md             # Dataset documentation
    ├── ml.md                    # Machine learning documentation
    └── mkdocs.yml               # Mkdocs configuration
```


---  

draft

```
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── vigilance.py          # Vigilance analysis agent
│   │   ├── movement.py           # Movement analysis agent
│   │   ├── expressions.py        # Facial expressions analysis agent
│   │   └── discomfort.py         # Discomfort analysis agent
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ml_models.py          # Machine Learning models
│   ├── api/
│   │   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── video_processor.py   # Video/frame processing
│   │   ├── subtitle_generator.py # Subtitle generation
│   │   └── alert_system.py      # Alert system
│   ├── config.py                # Configuration and constants
│   └── main.py                  # Main script
│
├── frontend/
│   └── (React/Vue.js application)
│
├── tests/
│
├── docker/
│   ├── Dockerfile.backend      # Backend Dockerfile
│   ├── Dockerfile.frontend     # Frontend Dockerfile
│   └── docker-compose.yml      # Docker Compose configuration
│
├── scripts/
│   ├── setup.sh               # Initial setup script
│   ├── run_tests.sh           # Test runner script
│   └── deploy.sh              # Deployment script
│
├── .env.example               # Environment variables example
├── .gitignore                 # Git ignore file
├── README.md                  # Main project documentation
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Python
```