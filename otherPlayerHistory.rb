require_relative 'dota2.rb'

res = requestOtherPlayerInfo(ARGV[0], ARGV[1])
matchArr = returnMatchIDs(res)
idArr = makeResourceMatchQuery(ARGV[0], matchArr)
createOtherMatchFiles(idArr, ARGV[1])