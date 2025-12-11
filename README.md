# SOSParser

A web application for automated analysis of Linux sosreport/supportconfig diagnostic files.

[![Docker Hub](https://img.shields.io/docker/pulls/samuelmatildes/sosparser)](https://hub.docker.com/r/samuelmatildes/sosparser)
[![Docker Image Size](https://img.shields.io/docker/image-size/samuelmatildes/sosparser/latest)](https://hub.docker.com/r/samuelmatildes/sosparser)

## Project Structure

```
sosparser/
├── webapp/          # Flask web application
│   ├── app.py      # Main Flask app
│   ├── templates/  # HTML templates
│   └── static/     # CSS, JS, images
├── src/             # Core analyzer logic
│   ├── core/       # Main analyzer orchestration
│   ├── analyzers/  # Domain-specific analyzers
│   │   ├── system/ # System information
│   │   ├── network/# Network analysis
│   │   ├── logs/   # Log analysis
│   │   └── scenarios/ # Pattern-based scenario detection
│   ├── reporting/  # Report generation
│   ├── templates/  # Report HTML template
│   ├── scenarios/  # Scenario JSON configs
│   ├── static/     # Report assets
│   └── utils/      # Utility functions
└── README.md
```

## Architecture

The application follows a domain-based architecture with clear separation:

1. **Webapp Layer** (`webapp/`): Flask application handling file uploads and serving results
2. **Analyzer Layer** (`src/`): Core analysis logic, completely independent of webapp
3. **Report Generation**: Template-based HTML report generation with Jinja2

## Features

- **File Upload**: Accepts sosreport tarballs (.tar.xz, .tar.gz, .tar.bz2, .tar)
- **Automated Analysis**: 
  - System information extraction (CPU, memory, disks, DMI)
  - System configuration (packages, kernel modules, users)
  - Filesystem analysis
  - Network configuration analysis
  - Cloud provider detection (AWS, Azure, GCP, Oracle Cloud)
  - Advanced log viewer with search and filtering
- **Interactive Reports**: Ultra-dark themed HTML reports with tabbed navigation
- **Privacy-Focused**: Auto-cleanup of uploaded files and reports after viewing

## Installation

### 🐳 Docker (Recommended)

The easiest way to run SOSParser is using Docker:

```bash
docker pull samuelmatildes/sosparser:latest
docker run -d -p 8000:8000 --name sosparser samuelmatildes/sosparser:latest
```

Then open http://localhost:8000 in your browser.

#### With Persistent Storage (Optional)

```bash
mkdir -p data/uploads data/outputs
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data/uploads:/app/webapp/uploads \
  -v $(pwd)/data/outputs:/app/webapp/outputs \
  --name sosparser \
  samuelmatildes/sosparser:latest
```

#### Using Docker Compose

```bash
# Download docker-compose.yml from the repository
docker-compose up -d
```

### 🐍 Python (Development)

#### Prerequisites

- Python 3.10+
- pip

#### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the webapp:
```bash
python3 webapp/app.py
```

The webapp will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Open `http://localhost:8000` in your browser
2. Select a sosreport tarball file (supports .tar.xz, .tar.gz, .tar.bz2, .tar)
3. Click "Analyze Report"
4. View the generated interactive analysis report with:
   - **Summary**: System overview, hardware specs, memory, report metadata
   - **System Config**: OS details, packages, kernel modules, users & groups
   - **Filesystem**: Mount points, disk usage, LVM configuration
   - **Network**: Interfaces, routing, DNS, firewall rules
   - **Cloud**: Cloud provider detection and configuration (if applicable)
   - **Logs**: Advanced log viewer with search, filters, and highlighting

### Docker Management

```bash
# View logs
docker logs -f sosparser

# Stop the container
docker stop sosparser

# Start the container
docker start sosparser

# Remove the container
docker rm -f sosparser

# Update to latest version
docker pull samuelmatildes/sosparser:latest
docker rm -f sosparser
docker run -d -p 8000:8000 --name sosparser samuelmatildes/sosparser:latest
```

### Command Line (Direct Analysis)

```python
from src.core.analyzer import run_analysis

report_path = run_analysis(
    "/path/to/sosreport.tar.xz",
    debug_mode=True
)
print(f"Report generated: {report_path}")
```

## Adding Scenarios

Scenarios are JSON-based pattern matching configurations stored in `src/scenarios/`.

Example scenario structure:
```json
{
  "ScenarioName": "My Scenario",
  "Description": "Detect specific issues",
  "ScenarioConfigs": [
    {
      "AlertName": "Issue Name",
      "Level": "Warning",
      "FailureSignature": "signature_name",
      "Workflow": "https://docs.example.com/troubleshooting",
      "MessageTemplate": "Description of the issue",
      "Recommendations": [
        "Fix step 1",
        "Fix step 2"
      ],
      "FileConfigs": [
        {
          "FilePath": "var/log",
          "FileName": "messages",
          "LookFor": [
            {
              "Pattern": "error_pattern",
              "Type": "regex",
              "Severity": "Warning",
              "MaxMatches": 20
            }
          ]
        }
      ]
    }
  ]
}
```

## Development

### Project Principles

1. **Domain Separation**: Webapp and analyzer are completely separate
2. **Template-Based**: Reports use Jinja2 templates for easy customization
3. **Scenario-Driven**: Issue detection through JSON configurations
4. **No External Dependencies**: Minimal dependencies, uses Python stdlib where possible

### Code Structure

- Analyzers are modular and independent
- Each analyzer returns structured data
- Report generator combines all data into HTML
- Scenarios can be added/modified without code changes

## Supported Formats

- `.tar.xz` (recommended)
- `.tar.gz`
- `.tar.bz2`
- `.tgz`
- `.tar`

## Theme

The application uses a custom ultra-dark condensed theme:
- **Webapp**: Cyan/Orange accents on ultra-dark background
- **Report**: Purple/Cyan accents on ultra-dark background with condensed spacing

Both themes are modern, space-efficient, and maintain excellent readability.

## Build from Source

### Build Docker Image Locally

```bash
git clone <your-repo-url>
cd sosparser
docker build -t sosparser:local .
docker run -d -p 8000:8000 sosparser:local
```

### Or use the build script

```bash
./docker-build.sh
```

## Docker Hub

Official Docker image: [samuelmatildes/sosparser](https://hub.docker.com/r/samuelmatildes/sosparser)

Available tags:
- `latest` - Latest stable release from main branch
- `v*.*.*` - Specific version releases
- Multi-platform support: `linux/amd64`, `linux/arm64`

## Support

For issues, questions, or contributions, please visit the GitHub repository.

## License

[Add your license here]
