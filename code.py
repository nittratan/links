[loggers]
keys=root,myLogger

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=defaultFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_myLogger]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=myLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=defaultFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=defaultFormatter
args=('myapp.log', 'a')

[formatter_defaultFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S


