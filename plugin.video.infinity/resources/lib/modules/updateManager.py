# -*- coding: UTF-8 -*-

"""
    Infinity Add-on (C) 2019
    Credits to Lastship, Placenta and Covenant; our thanks go to their creators

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    UpdateManager (C) 2019 by kasi modo
	
"""

import os
import json
import requests
from requests.auth import HTTPBasicAuth

import xbmc
from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING
from xbmc import translatePath
from xbmcgui import Dialog
from xbmcaddon import Addon as addon

## Android K18 ZIP Fix.
if xbmc.getCondVisibility('system.platform.android') and int(xbmc.getInfoLabel('System.BuildVersion')[:2]) >= 18:
    import fixetzipfile as zipfile
else:
    import zipfile

# Text/Überschrift im Dialog
PLUGIN_NAME = addon().getAddonInfo('name')  # ist z.B. 'INFINITY'
PLUGIN_ID = addon().getAddonInfo('id')  # ist z.B. 'plugin.video.infinity'


## URLRESOLVER
def urlResolverUpdate(silent=False):
    username = 'streamxstream'            ### Repo
    plugin_id = 'script.module.urlresolver'
    branch = 'master'
    token = 'ZmY3OGNmMGU0NjgzOWQ2ODA0ZTgwNTZkZDM3MTllNWEzMTQ1OTM2Yw=='

    try:
        return Update(username, plugin_id, branch, token, silent)

    except Exception as e:
        xbmc.log('Exception Raised: %s' % str(e), xbmc.LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return

## INFINITY
def pluginVideoInfinity(silent=False):
    username = 'deepship'
    plugin_id = 'plugin.video.infinity'
    branch = 'nightly'
    token = ''

    try:
        return Update(username, plugin_id, branch, token, silent)

    except Exception as e:
        xbmc.log('Exception Raised: %s' % str(e), LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False

# Update Funktion Github
def Update(username, plugin_id, branch, token, silent):
    REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/%s/%s/commits/%s" % (username, plugin_id, branch)
    REMOTE_PLUGIN_DOWNLOADS = "https://api.github.com/repos/%s/%s/zipball/%s" % (username, plugin_id, branch)
    auth = HTTPBasicAuth(username, token.decode('base64'))

    xbmc.log('%s - Search for update ' % plugin_id, LOGNOTICE)
    try:
        ADDON_DIR = translatePath(addon(plugin_id).getAddonInfo('profile')).decode('utf-8')
        LOCAL_PLUGIN_VERSION = os.path.join(ADDON_DIR, "update_sha")
        LOCAL_FILE_NAME_PLUGIN = os.path.join(ADDON_DIR, 'update-' + plugin_id + '.zip')
        if not os.path.exists(ADDON_DIR): os.mkdir(ADDON_DIR)
#ka - Update erzwingen
        if addon().getSetting('enforceUpdate') == 'true':
            if silent == False and os.path.exists(LOCAL_PLUGIN_VERSION): os.remove(LOCAL_PLUGIN_VERSION)

        path = addon(plugin_id).getAddonInfo('Path')
        commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS, auth)
        if commitXML:
            isTrue = commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, path, plugin_id,
                                  LOCAL_FILE_NAME_PLUGIN, silent, auth)
            if isTrue == True:
                xbmc.log('%s - Update successful.' % plugin_id, LOGNOTICE)
                if silent == False: Dialog().ok(PLUGIN_NAME, plugin_id + " - Update erfolgreich.")
                return True
            elif isTrue == None:
                xbmc.log('%s - no new update ' % plugin_id, LOGNOTICE)
                if silent == False: Dialog().ok(PLUGIN_NAME, plugin_id + " - Kein Update verfügbar.")
                return None

        xbmc.log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False
    except:
        xbmc.log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)

def commitUpdate(onlineFile, offlineFile, downloadLink, LocalDir, plugin_id, localFileName, silent, auth):
    try:
        jsData = json.loads(onlineFile)
        if not os.path.exists(offlineFile) or open(offlineFile).read() != jsData['sha']:
            xbmc.log('%s - start update ' % plugin_id, LOGNOTICE)
            isTrue = doUpdate(LocalDir, downloadLink, plugin_id, localFileName, auth)
            if isTrue == True:
                try:
                    open(offlineFile, 'w').write(jsData['sha'])
                    return True
                except:
                    return False
            else:
                return False
        else:
            return None

    except Exception as e:
        os.remove(offlineFile)
        xbmc.log("RateLimit reached")
        return False
        
def doUpdate(LocalDir, REMOTE_PATH, Title, localFileName, auth):
    try:
        response = requests.get(REMOTE_PATH, auth=auth)  # verify=False,
                                
        # Open our local file for writing
        # with open(localFileName,"wb") as local_file:
        # local_file.write(f.read())
        if response.status_code == 200:
            open(localFileName, "wb").write(response.content)
        else:
            return False
        updateFile = zipfile.ZipFile(localFileName)

        removeFilesNotInRepo(updateFile, LocalDir)

        for index, n in enumerate(updateFile.namelist()):
            if n[-1] != "/":
                dest = os.path.join(LocalDir, "/".join(n.split("/")[1:]))
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                if os.path.exists(dest):
                    os.remove(dest)
                f = open(dest, 'wb')
                f.write(data)
                f.close()
        updateFile.close()
        os.remove(localFileName)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        return True
    except:
        xbmc.log("do Update not possible due download error")
        return False
        
def removeFilesNotInRepo(updateFile, LocalDir):
    ignored_files = ['settings.xml']
    updateFileNameList = [i.split("/")[-1] for i in updateFile.namelist()]

    for root, dirs, files in os.walk(LocalDir):
        if ".git" in root or "pydev" in root or ".idea" in root:
            continue
        else:
            for file in files:
                if file in ignored_files:
                    continue
                if file not in updateFileNameList:
                    os.remove(os.path.join(root, file))

def _getXmlString(xml_url, auth):
    try:
        xmlString = requests.get(xml_url, auth=auth).content  # verify=False,
        if "sha" in json.loads(xmlString):
            return xmlString
        else:
            xbmc.log("Update-URL incorrect or bad credentials")
    except Exception as e:
        xbmc.log(e)

def log(msg, level=LOGDEBUG):
    DEBUGPREFIX = '[ ' + PLUGIN_ID + ' DEBUG ]'
    # override message level to force logging when addon logging turned on
    level = LOGNOTICE
    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))
        xbmc.log('%s: %s' % (DEBUGPREFIX, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except:
            pass  # just give up

# todo Verzeichnis packen -für zukünftige Erweiterung "Backup"
def zipfolder(foldername, target_dir):
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])
    zipobj.close()

def devAutoUpdates(silent=False):
    try:
        status1 = status2 = None
        if addon().getSetting('githubUpdateInfinity') == 'true':
            status1 = pluginVideoInfinity(silent)
        if addon().getSetting('githubUpdateUrlResolver') == 'true':
            status2 = urlResolverUpdate(silent)

        if status1 == status2:
            return status1
        elif status1 == False or status2 == False:
                return False
        elif (status1 == True or status2 == True) and (status1 == None or status2 == None):
            return True

    except Exception as e:
        xbmc.log(e)

# für manuelles Updates vorgesehen
def devUpdates(): 
    try:
        resolverupdate = False
        pluginupdate = False

        options = ['Beide', PLUGIN_NAME, 'URL Resolver']
        result = Dialog().select('Welches Update ausführen?', options)

        if result == 0:
            resolverupdate = True
            pluginupdate = True
        elif result == 1:
            pluginupdate = True
        elif result == 2:
            resolverupdate = True

        if pluginupdate == True:
            try:
                pluginVideoInfinity(False)
            except:
                pass
        if resolverupdate == True:
            try:
                urlResolverUpdate(False)
            except:
                pass
        #ka - reset enforce Update
        if addon().getSetting('enforceUpdate') == 'true': addon().setSetting('enforceUpdate', 'false')
        return
    except Exception as e:
        xbmc.log(e)
