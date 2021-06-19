#! /bin/bash

# Usage: ./find_replace.sh <old> <new>

echo "grep -RiIl "$1" | xargs sed -i 's/$1/$2/g'"
