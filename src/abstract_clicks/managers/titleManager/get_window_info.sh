#!/bin/bash

# Function to get monitor boundaries
get_monitors() {
    monitors=()
    while IFS= read -r line; do
        if [[ $line =~ ([a-zA-Z0-9-]+)\ connected\ ([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+) ]]; then
            name=${BASH_REMATCH[1]}
            width=${BASH_REMATCH[2]}
            height=${BASH_REMATCH[3]}
            x_offset=${BASH_REMATCH[4]}
            y_offset=${BASH_REMATCH[5]}
            monitors+=("$name $x_offset $y_offset $width $height")
        fi
    done < <(xrandr --query | grep " connected")
}

# Function to find window by ID, title, or PID
find_window() {
    local search_type=$1 search_value=$2
    case $search_type in
        id)
            wmctrl -l -p | grep "$search_value" | awk '{print $1}'
            ;;
        title)
            wmctrl -l -p | grep -i "$search_value" | awk '{print $1}'
            ;;
        pid)
            wmctrl -l -p | awk -v pid="$search_value" '$3 == pid {print $1}'
            ;;
        *)
            echo "Invalid search type"
            exit 1
            ;;
    esac
}

# Function to move window to monitor
move_to_monitor() {
    local win_id=$1 monitor_name=$2
    for monitor in "${monitors[@]}"; do
        read -r name x y w h <<< "$monitor"
        if [[ $name == "$monitor_name" ]]; then
            wmctrl -i -r "$win_id" -e 0,"$x","$y",-1,-1
            echo "Moved window $win_id to $monitor_name ($x,$y)"
            return
        fi
    done
    echo "Monitor $monitor_name not found"
    exit 1
}

# Function to control window state
control_window() {
    local win_id=$1 action=$2
    case $action in
        minimize)
            xdotool windowminimize "$win_id"
            echo "Minimized window $win_id"
            ;;
        maximize)
            wmctrl -i -r "$win_id" -b add,maximized_vert,maximized_horz
            echo "Maximized window $win_id"
            ;;
        close)
            xdotool windowclose "$win_id"
            echo "Closed window $win_id"
            ;;
        *)
            echo "Invalid action"
            exit 1
            ;;
    esac
}

# Main script
if [[ $# -lt 4 ]]; then
    echo "Usage: $0 <search_type> <search_value> <monitor_name> <action>"
    echo "search_type: id, title, or pid"
    echo "action: minimize, maximize, or close"
    echo "Example: $0 title Firefox HDMI-1 maximize"
    exit 1
fi

search_type=$1
search_value=$2
monitor_name=$3
action=$4

# Get monitor info
get_monitors

# Find window
win_id=$(find_window "$search_type" "$search_value")
if [[ -z $win_id ]]; then
    echo "No window found for $search_type: $search_value"
    exit 1
fi
if [[ $(echo "$win_id" | wc -l) -gt 1 ]]; then
    echo "Multiple windows found, using first one: $win_id"
    win_id=$(echo "$win_id" | head -n 1)
fi

# Move to monitor
move_to_monitor "$win_id" "$monitor_name"

# Perform action
control_window "$win_id" "$action"
