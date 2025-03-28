#!/bin/bash

BACKUP_DIR=backups
NOW=$(date '+%Y-%m-%d %H%M%S')
FILE_NAME=backup_$NOW.sql

mkdir -p "$BACKUP_DIR"

echo "Creating backup..."
docker exec -t db pg_dump -U postgres images_db > "$BACKUP_DIR/$FILE_NAME" && echo "Backup $FILE_NAME created" || echo "Backup $FILE_NAME failed"