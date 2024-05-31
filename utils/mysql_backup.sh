#!/bin/bash

LOG_FILE="/mnt/d/bash_backups/db_backups.log"

log_message() {
    log_time=$(date +"%d-%b-%Y %H:%M:%S")
    echo "[$log_time] $1" >> $LOG_FILE
}

mysqldump_backup() {
    log_message "Starting MySQL dump backup..."

    DB_BACKUP_USER=""
    DB_BACKUP_PASS=""
    DB_NAME=""
    TIMESTAMP=$(date +"%d-%b-%Y")
    LOCAL_BACKUP_DIR="/path/local/mysqldump"
#    SERVER_BACKUP_DIR="username@server:/path/server/mysqldump/"
    MAX_BACKUPS=7

    # Create local backup directory
    mkdir -p $LOCAL_BACKUP_DIR

    # Perform MySQL dump backup using mysqldump
    mysqldump -u $DB_BACKUP_USER -p$DB_BACKUP_PASS $DB_NAME > $LOCAL_BACKUP_DIR/$DB_NAME-$TIMESTAMP.sql

    # Sync local backup to server backup directory (dry run)
#    rsync -avn --delete $LOCAL_BACKUP_DIR/$SERVER_BACKUP_DIR/

    # Rotate backup files on both local and server
    cd $LOCAL_BACKUP_DIR
#    ls -t $DB_NAME-*.sql | tail -n +$((MAX_BACKUPS+1)) | xargs rm --

#    ssh $SERVER_BACKUP_DIR cd $SERVER_BACKUP_DIR && ls -t $DB_NAME-*.sql | tail -n +$((MAX_BACKUPS+1)) | xargs rm --

    log_message "MySQL dump backup completed."
}

mariabackup_backup() {
    log_message "Starting MariaBackup database backup..."

    DB_BACKUP_USER=""
    DB_BACKUP_PASS=""
    DB_NAME=""
    TIMESTAMP=$(date +"%d-%b-%Y")
    LOCAL_BACKUP_DIR="/path/local/mariabackup"
#    SERVER_BACKUP_DIR="username@server:/path/server/mariabackup/"
    MAX_BACKUPS=7

    # Create local backup directory
    mkdir -p $LOCAL_BACKUP_DIR

    # Perform database dump backup using mariabackup
    mariabackup --user=$DB_BACKUP_USER --password=$DB_BACKUP_PASS --backup --target-dir=$LOCAL_BACKUP_DIR/$TIMESTAMP --databases=$DB_NAME

    # Prepare the backup for restoration
    mariabackup --prepare --target-dir=$LOCAL_BACKUP_DIR/$TIMESTAMP

    # Sync local backup to server backup directory (dry run)
#    rsync -avn --delete $LOCAL_BACKUP_DIR/$SERVER_BACKUP_DIR/

    # Rotate backup files on both local and server
    cd $LOCAL_BACKUP_DIR
#    ls -t | tail -n +$((MAX_BACKUPS+1)) | xargs rm -rf --

 #   ssh $SERVER_BACKUP_DIR cd $SERVER_BACKUP_DIR && ls -t | tail -n +$((MAX_BACKUPS+1)) | xargs rm -rf --

    log_message "MariaBackup database backup completed."
}

mysqldump_backup >> $LOG_FILE 2>&1
mariabackup_backup >> $LOG_FILE 2>&1
