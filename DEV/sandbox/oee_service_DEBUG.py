import configparser

config = configparser.ConfigParser()
# config.read('DEBUG\\DEBUG.config')
config.read('oee-service\\oee_conf.config')

print(config['PROCESS'])
print('\n')
print(config['PROCESS']['upTimeStates'])