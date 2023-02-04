import os
import _dataTemplate

script_dir = os.path.dirname(__file__)

filePath = script_dir + "\\" + "_dataTemplate" + ".py"
print(filePath)
exec(open(filePath).read())

_data = [[0,1,2,3]]

print(_dataTemplate.Data_Template_Dict(_data))
