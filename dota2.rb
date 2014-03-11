require 'open-uri'
require 'xmlsimple'

def makeResourceMatchHistory(keyFile, idFile)
  path = File.expand_path(File.dirname(__FILE__)) + "/text_files/"
  resource = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?format=XML&key="
  open(path + keyFile, "r") { |f|
    f.each_line { |line|
      resource += line 
    }
  }
  open(path + idFile, "r") { |f| 
    i = 0
    f.each_line { |line| 
      if i == 1 then 
        resource += "&account_id=" + line 
      end
      i = i + 1
    }
  }
  return resource
end

def returnMatchIDs(resource)
  idArr = Array.new()
  uri = URI.parse(resource)
  parseHash = XmlSimple.xml_in(uri, { 'KeyAttr' => 'name' })
  parseHash.each do |key, value|
    if key == 'num_results' then
      @num = parseHash[key][0].to_i
    end
    if key == 'matches' then
      i = 0
      while i < @num
        idArr.push(parseHash[key][0]['match'][i]['match_id'][0])
        i += 1
      end
    end
  end
  return idArr
end

def makeResourceMatchQuery(keyFile, matchIDArr)
  path = File.expand_path(File.dirname(__FILE__)) + "/text_files/"
  resourceArr = Array.new()
  resource = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?format=XML&key="
  open(path + keyFile, "r") { |f|
    f.each_line { |line|
      resource += line 
    }
  }
  matchIDArr.each do |val|
    resourceArr.push(resource + "&match_id=" + val)
  end
  return resourceArr
end

def createMatchFiles(matchQueryArr)
  matchQueryArr.each do |res|
    uri = URI.parse(res)
    parseHash = XmlSimple.xml_in(uri, { 'KeyAttr' => 'name' })
    open("matches/" + parseHash['match_id'][0] + '.xml' , 'w') { |file|
      uri.open { |f| 
        f.each_line { |line|
          file.write(line)
        }
      }
    }
  end
end

def processMatchDetails(matchQueryArr, array)
end