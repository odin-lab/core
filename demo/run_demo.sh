#!/bin/bash

# Simple script to run the audio recording demo
# Requires tmux to be installed

SESSION="audio-demo"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "tmux is required but not installed. Please install tmux first."
    exit 1
fi

# Kill any existing session
tmux kill-session -t $SESSION 2>/dev/null

# Create a new tmux session
tmux new-session -d -s $SESSION

# Split the window into 3 panes
tmux split-window -h -t $SESSION
tmux split-window -v -t $SESSION

# Run microphone module in first pane
tmux send-keys -t $SESSION:0.0 "uv run python microphone_module.py" C-m

# Run recorder module in second pane
tmux send-keys -t $SESSION:0.1 "uv run python recorder_module.py" C-m

# Give modules time to start
sleep 2

# Run the demo manager in third pane
tmux send-keys -t $SESSION:0.2 "uv run python demo_manager.py" C-m

# Attach to the session
echo "Starting demo in tmux session '$SESSION'"
echo "Use 'Ctrl-B D' to detach from the session"
echo "Use 'tmux attach -t $SESSION' to reattach"
tmux attach-session -t $SESSION 