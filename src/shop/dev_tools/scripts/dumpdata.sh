#!/bin/bash
# 
# Create data fixtures from currently active database.
#
# Author: Thomas Gwasira
# Date: 2022

cmd="SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
IFS=$'\n'
fqry=(`sqlite3 db.sqlite3 "$cmd"`)

for table in "${fqry[@]}"; do
    dd_table=$(echo "$table" | sed 's/_/./')
    django-admin dumpdata $dd_table --indent 2 --output "fixtures/"$table".json"
done