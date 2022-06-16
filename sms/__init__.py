__app_name__ = 'sms'
__version__ = '0.0.1'

(
    SUCCESS,
    DIR_ERROR, 
    VALUE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR, 
    JSON_ERROR, 
    FILE_ERROR
) = range(7)

ERROR = {
    DIR_ERROR: "config directory error",
    VALUE_ERROR: "Invalid value",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error",
    JSON_ERROR: "Json Error",
    FILE_ERROR: "config file error"
}

