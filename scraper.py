# Funciones/Procedimientos relacionados con web scraping y miniaturas
import requests as curl
import re as regex
import http.cookiejar as cookiejar
import os
import json
import glom

import scraper_config as config
import paths

# Descargar un archivo
def curlFile(url, path):
	fileReq = curl.get(url)
	downFile = open(path, "wb")
	downFile.write(fileReq.content)
	downFile.close()

# Filtrar el JSON de youtube utilizando expresiones regulares
def htmlToJson(htmlResponse):
	# Explicación: "Selecciona todo lo que se encuentre entre los textos 'ytInitialData = ' y ';</script>'"
	stringJson = regex.search(r"(?<=ytInitialData = ).*?(?=;</script>)", htmlResponse.text).group(0)
	return json.loads(stringJson)

"""
# Hacer una petición con el archivo de cookies, y devolver un JSON ordenado
def getSubsData():
	url = "https://www.youtube.com/feed/subscriptions"
	cookiestxt =  cookiejar.MozillaCookieJar(paths.cookiesFile)
	cookiestxt.load()
	html = curl.get(url, cookies=cookiestxt)
	videoDict = subsHtmlToJson(html)
	position = "contents.twoColumnBrowseResultsRenderer.tabs.0.tabRenderer.content.sectionListRenderer.contents"
	tabCant = len(glom.glom(videoDict, position))
	vidList = []
	offset = 0
	for i in range(tabCant-1):
		tabPosition = position+"."+str(i)+".itemSectionRenderer.contents.0.shelfRenderer.content.gridRenderer.items"
		tabVidCant = len(glom.glom(videoDict, tabPosition))
		for j in range(tabVidCant):
			vidPosition = tabPosition+"."+str(j)+".gridVideoRenderer"
			vidList.append({})
			vidList[offset]['title'] = glom.glom(videoDict, vidPosition+".title.runs.0.text")
			vidList[offset]['channel'] = glom.glom(videoDict, vidPosition+".shortBylineText.runs.0.text")
			vidList[offset]['duration'] = glom.glom(videoDict, vidPosition+".thumbnailOverlays.0.thumbnailOverlayTimeStatusRenderer.text.simpleText")
			vidList[offset]['views'] = glom.glom(videoDict, vidPosition+".viewCountText.simpleText")
			vidList[offset]['date'] = glom.glom(videoDict, vidPosition+".publishedTimeText.simpleText")
			vidList[offset]['videoID'] = glom.glom(videoDict, vidPosition+".videoId")
			offset += 1
	return vidList

# Hacer una petición con el query, y devolver un JSON ordenado
def getSearchData(searchQuery):
	url = "https://yewtu.be/search?q=" + searchQuery
	html = curl.get(url)
	regexDict = {}
	regexDict['title'] = regex.findall(r"(?<=p dir=\"auto\">).*?(?=<)", html.text)
	regexDict['channel'] = regex.findall(r"(?<=channel-name\" dir=\"auto\">).*?(?=<)", html.text)
	regexDict['duration'] = regex.findall(r"(?<=class=\"length\">).*?(?=<)", html.text)
	regexDict['views'] = regex.findall(r"(?<=video-data\" dir=\"auto\">).*?(?= views)", html.text)
	regexDict['date'] = regex.findall(r"(?<=Shared ).*?(?=<)", html.text)
	regexDict['videoID'] = regex.findall(r"(?<=watch\?v=).*?(?=&listen)", html.text)
	vidList = []
	vidCant = len(regexDict['videoID'])
	for i in range(vidCant):
		vidList.append({})
		vidList[i]['title'] = regexDict['title'][i]
		vidList[i]['channel'] = regexDict['channel'][i]
		vidList[i]['duration'] = regexDict['duration'][i]
		vidList[i]['views'] = regexDict['views'][i]
		vidList[i]['date'] = regexDict['date'][i]
		vidList[i]['videoID'] = regexDict['videoID'][i]
	return vidList
"""

# Descargar una miniatura a partir del ID del video
def downloadThumbnail(videoId):
	thumbPath = os.path.join(paths.thumbFolder, videoId)
	if (not os.path.isfile(thumbPath+'.jpg')) and (not os.path.isfile(thumbPath+'_bad.jpg')):
		thumbUrl = "https://img.youtube.com/vi/"+videoId+"/maxresdefault.jpg"
		curlFile(thumbUrl, thumbPath+'.jpg')
		if os.path.getsize(thumbPath+'.jpg') < 1200: # Youtube no tiene miniaturas de buena calidad en algunos videos
			os.remove(thumbPath+'.jpg')
			thumbUrl = "https://img.youtube.com/vi/"+videoId+"/0.jpg" # En vez de eso, se guarda una de baja calidad
			curlFile(thumbUrl, thumbPath+'_bad.jpg')

# Eliminar todas las miniaturas
def delThumbnails():
	import glob
	files = glob.glob(os.path.join(paths.thumbFolder, "*"))
	for i in files:
		os.remove(i)
	
# Limpiar miniaturas al iniciar si el usuario lo configuró
if config.getConfig("del-thumb-cache", "bool"):
	delThumbnails(paths.thumbFolder)



# PyJQ solo funciona en linux :(
import pyjq
# Formato que pyjq usará para filtrar el JSON de youtube y crear otro JSON ordenado
jqJsonFormat = "{ title: .title.runs[0].text, channel: .shortBylineText.runs[0].text, duration: .thumbnailOverlays[0].thumbnailOverlayTimeStatusRenderer.text.simpleText, views: .viewCountText.simpleText, date: .publishedTimeText.simpleText, videoID: .videoId }"

# Hacer una petición con el query, y devolver un JSON ordenado
def getSearchData(searchQuery):
	url = "https://www.youtube.com/results?search_query=" + searchQuery
	html = curl.get(url)
	videoDict = htmlToJson(html)
	return pyjq.all('.contents|..|.videoRenderer? | select(. !=null) | '+jqJsonFormat, videoDict)

# Hacer una petición con el archivo de cookies, y devolver un JSON ordenado
def getSubsData():
	url = "https://www.youtube.com/feed/subscriptions"
	cookiestxt =  cookiejar.MozillaCookieJar(paths.cookiesFile)
	cookiestxt.load()
	html = curl.get(url, cookies=cookiestxt)
	videoDict = htmlToJson(html)
	return pyjq.all('.contents.twoColumnBrowseResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents[].itemSectionRenderer.contents[0].shelfRenderer.content.gridRenderer.items[]? | select(. !=null) | .gridVideoRenderer | '+jqJsonFormat, videoDict)
"""
def newGetSearchData(searchQuery):
	url = "https://www.youtube.com/results?search_query=" + searchQuery
	html = curl.get(url)
	videoDict = htmlToJson(html)
	position = "contents.twoColumnSearchResultsRenderer.primaryContents.sectionListRenderer.contents.0.itemSectionRenderer.contents"
	tabVidCant = len(glom.glom(videoDict, position))
	try:
		try: # Con
			for i in range(tabVidCant-1):
				vidPosition = position+"."+str(i)+".videoRenderer"
				print(glom.glom(videoDict, vidPosition+".videoId"))
		except:
			vidPosition = position+"."+str(i)+".shelfRenderer.content.verticalListRenderer.items"
			subTabVidCant = len(glom.glom(videoDict, vidPosition))
			for j in range(subTabVidCant):
				print(glom.glom(videoDict, vidPosition+"."+str(j)+".videoRenderer.videoId"))
	except:
		vidPosition = position+".1.shelfRenderer.content.verticalListRenderer.items"
		subSubTabVidCant= len(glom.glom(videoDict, vidPosition))
		for k in range(subSubTabVidCant):
			print(glom.glom(videoDict, vidPosition+"."+str(k)+".videoRenderer.videoId"))
		vidPosition = position
		newLen =len(glom.glom(videoDict, vidPosition))
		print(glom.glom(videoDict, vidPosition+".8.videoRenderer.videoId"))
"""


