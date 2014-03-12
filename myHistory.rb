require_relative 'dota2.rb'

file1 = ARGV[0]
file2 = ARGV[1]
res = makeResourceMatchHistory(file1, file2)
idArr = returnMatchIDs(res)
resArr = makeResourceMatchQuery(file1, idArr)
createMatchFiles(resArr)