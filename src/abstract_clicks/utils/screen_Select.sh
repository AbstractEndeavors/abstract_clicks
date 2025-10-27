#!/bin/bash

# Configuration variables
WINDOW_TITLE="$1"  # Partial window title to match (passed as argument)
PASTE_AFTER_SWITCH="${2:-false}"  # Whether to paste after switching (true/false)

# Check if xdotool is installed
if ! command -v xdotool >/dev/null 2>&1; then
  echo "Error: xdotool is not installed. Install it with 'sudo apt install xdotool'."
  exit 1
fi

# Check if WINDOW_TITLE is provided
if [ -z "$WINDOW_TITLE" ]; then
  echo "Usage: $0 <partial-window-title> [paste-after-switch]"
  echo "Example: $0 Firefox true"
  echo "List open windows with: wmctrl -l"
  exit 1
fi

# Find window ID by partial title match (case-insensitive)
WINDOW_ID=$(xdotool search --name --onlyvisible "$WINDOW_TITLE" | head -n 1)

if [ -z "$WINDOW_ID" ]; then
  echo "Error: No visible window found with title containing '$WINDOW_TITLE'."
  echo "List open windows with: wmctrl -l"
  exit 1
fi

# Activate the window
echo "Switching to window with title containing '$WINDOW_TITLE' (ID: $WINDOW_ID)..."
xdotool windowactivate "$WINDOW_ID"

# Check if window was successfully activated
if xdotool getactivewindow | grep -q "$WINDOW_ID"; then
  echo "Window successfully activated."
else
  echo "Error: Failed to activate window."
  exit 1
fi

# Optionally perform a paste action (Ctrl+V)
if [ "$PASTE_AFTER_SWITCH" = "true" ]; then
  echo "Performing paste action..."
  # Simulate Ctrl+V (requires xdotool)
  xdotool key --clearmodifiers ctrl+v
  # Small delay to ensure paste completes
  sleep 0.2
  echo "Paste action completed."
fi

exit 0
