@echo off


set MYSQLDUMP_PATH="C:\Program Files\MySQL\MySQL Server 8.3\bin\mysqldump.exe"
set ZIP_PATH="C:\Program Files\7-Zip\7z.exe"
set BACKUP_DIR="D:\automated_scripts\MySQL_Backups"
set BACKUP_LOG_FILE="%BACKUP_DIR%\backup_log.txt"


:: Read specific values from .env file (assuming DB_BACKUP_USER and DB_BACKUP_PASSWORD are defined there)
for /f "tokens=1,* delims==" %%a in ('type .env') do (
  if "%%a"=="DB_BACKUP_USER" set DB_BACKUP_USER=%%b
  if "%%a"=="DB_BACKUP_PASSWORD" set DB_BACKUP_PASSWORD=%%b
)

:: Get current date in YYYY-MM-DD format
for /f "tokens=1-3 delims=-" %%i in ('echo %date%') do (
  set "yy=%%k"
  set "mm=%%i"
  set "dd=%%j"
)

:: Start logging
echo %date% %time% - Starting backup process >> "%BACKUP_LOG_FILE%"
echo ---------------------------------------- >> "%BACKUP_LOG_FILE%"

:: List of databases to back up
set "DATABASES=kbbio sys"

:: Backup each database
for %%a in (%DATABASES%) do (
  echo %date% %time% - Backing up database: %%a >> "%BACKUP_LOG_FILE%"

  %MYSQLDUMP_PATH% --host=localhost --user=%DB_BACKUP_USER% --password=%DB_BACKUP_PASSWORD% --single-transaction --databases %%a > %BACKUP_DIR%\%%a_%yy%-%mm%-%dd%.sql

  if %errorlevel% neq 0 (
    echo An error occurred while dumping database: %%a >> %BACKUP_LOG_FILE%
    exit /b 1
  )

  %ZIP_PATH% a -tgzip %BACKUP_DIR%\%%a_%yy%-%mm%-%dd%.zip %BACKUP_DIR%\%%a_%yy%-%mm%-%dd%.sql

  if %errorlevel% neq 0 (
    echo An error occurred while zipping database: %%a >> "%BACKUP_LOG_FILE%"
    exit /b 1
  )

  del %BACKUP_DIR%\%%a_%yy%-%mm%-%dd%.sql
  echo %date% %time% - Backup completed: %%a >> "%BACKUP_LOG_FILE%"
)

:: End logging
echo ---------------------------------------- >> "%BACKUP_LOG_FILE%"
echo %date% %time% - Backup process completed >> "%BACKUP_LOG_FILE%"
