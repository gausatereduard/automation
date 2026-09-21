#!/bin/bash

# Check that at least one argument was provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 dir_to_clean [file_types...]"
    exit 1
fi

dst_dir="$1"
shift

# Check that the directory exists
if [ ! -d "$dst_dir" ]; then
    echo "Error: Directory does not exist: $dst_dir"
    exit 1
fi

# Default extension
if [ "$#" -eq 0 ]; then
    file_types=(".tmp")
else
    file_types=("$@")
fi

deleted_count=0

# Find and delete files with the specified extensions
for ext in "${file_types[@]}"; do
    while IFS= read -r -d '' file; do
        rm -f "$file"
        ((deleted_count++))
    done < <(find "$dst_dir" -type f -name "*$ext" -print0)
done

echo "Deleted files: $deleted_count"
