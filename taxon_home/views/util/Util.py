import re
from datetime import datetime
import taxon_home.views.util.ErrorConstants as Errors

def getMultiListPost(request, name, default):
    dic = {}
    parts = []
    namePattern = re.compile(name + r'\[([0-9]+)\]')
    for k in request.POST.keys():
        match = namePattern.search(k)
        if (match):    
            parts.append({
                'entire' : match.group(0),
                'key' : match.group(1)
            })
    if parts:
        for part in parts:
            dic[int(part['key'])] = request.POST.getlist(part['entire'] + '[]')
            
        return dic
    else:
        return default

def getInt(queryDict, key, default):
    value = queryDict.get(key, '')
    if value.isdigit():
        value = int(value)
    else:
        value = default
        
    return value

def getDelimitedList(queryDict, key, delimiter=','):
    value = queryDict.get(key, None)
    if value:
        value = [item.strip() for item in value.split(delimiter)]
    return value

def getFilterByDate(dateString, paramName):
    action, dates = (item.strip() for item in dateString.split(':', 1))
    
    try:
        if action == 'after':
            date = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            return paramName + '__gt', date
        elif action == 'before':
            date = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            return paramName + '__lt', date
        elif action == 'range':
            first, second = (datetime.strptime(item, "%Y-%m-%d %H:%M:%S") for item in dates.split(',', 1))
            return paramName + '__range', [first, second]
        else: # on keyword or no keyword
            date = datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
            return paramName, date
    except ValueError:
        raise Errors.INVALID_SYNTAX.setCustom(paramName)       