# Hand Sign Screen Lock

A lightweight computer-vision utility that locks the host screen when a closed-fist gesture is held for a configurable number of consecutive frames.

## Technical highlights
- Uses MediaPipe Hands and OpenCV to track a single hand and evaluate fingertip/pip relationships to detect a closed fist.
- Cross-platform lock helpers for Linux, macOS (Darwin), and Windows. The script attempts multiple platform-appropriate lock commands.
- Low CPU idle loop and short debounce window to avoid accidental triggers.

## Usage
Run from the `hand_sign_screenlock` directory with an active virtual environment (OpenCV & MediaPipe required):

```bash
python hand_lock.py
```

Optional flags:

- `--camera`: camera index (default `0`)
- `--fist-frames`: number of consecutive frames required to trigger lock (default `3`)

Example:

```bash
python hand_lock.py --camera 1 --fist-frames 4
```

## Notes
- Depending on your operating system, locking may require additional permissions or slight command adjustments.
- If the script cannot open the camera it will exit with code `1`.
- To stop the script without locking, terminate the process (Ctrl+C) before making the required fist gesture.
