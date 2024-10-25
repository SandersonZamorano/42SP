#!bin/bash/
find -name "*.sh" -exec basename {} ".sh" \; | cat -e

