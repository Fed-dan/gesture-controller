# Gesture Controller

> Control your PC with hand gestures via webcam.
> All gestures and actions are fully configurable via YAML — no coding required.

## Gestures

| Gesture | Hand  | Action                                |
|---------|-------|:--------------------------------------|
| OPEN    | Right | Configurable (default: open browser)  |
| PEACE   | Right | Configurable (default: open Spotify)  |
| PINCH   | Right | Brightness control                    |
| OPEN    | Left  | Configurable (default: open explorer) |
| PEACE   | Left  | Configurable (default: open terminal) |
| PINCH   | Left  | Volume control                        |

## Quick Start

```bash
git clone https://github.com/Fed-dan/gesture-controller
cd gesture-controller
pip install -r requirements.txt
python main.py
```

## Configuration

All gestures and actions are defined in `config/`:

|           File           | Purpose                                                           |
|:------------------------:|:------------------------------------------------------------------|
|     `gestures.yaml`      | Add new gestures and define geometry (which landmarks to compare) |
|     `auxiliary.yaml`     | Define auxiliary conditions (e.g. thumb direction)                |
| `combined_gestures.yaml` | Combine gestures with auxiliary conditions                        | 
| `complex_gestures.yaml`  | Define gesture sequences                                          |
|      `actions.yaml`      | Map gestures to actions                                           |
|       `apps.yaml`        | Define application paths                                          |
|      `config.yaml`       | Tune parameters (sensitivity, smoothing, etc.)                    |

### Example: change what OPEN does

Edit `config/actions.yaml`:
```yaml
ACTIONS:
  simple_right:
    OPEN: launch_1  # change this
```

Edit `config/apps.yaml`:
```yaml
APPS:
  launch_1: "C:/Path/To/Your/App.exe"
```

## Architecture

Three-layer pipeline:
Camera → HandDetector → GestureClassifier → ActionController
↓               ↓
Renderer        Smoother + Debounce

- **Capture** — camera input, frame rendering
- **Vision** — hand detection, gesture classification, smoothing
- **Controller** — volume, brightness, app launcher

## Tech Stack

Python · OpenCV · MediaPipe · PyAutoGUI · pycaw · screen-brightness-control · PyYAML

## Requirements

- Python 3.10+
- Webcam
- Windows (volume/brightness control)