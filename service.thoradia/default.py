import os.path
import subprocess
import xbmc
import xbmcaddon
import xbmcgui
import xml.etree.ElementTree as etree


KNOWN_REPOSITORIES = [
    'repository.libreelec.tv',
    'repository.coreelec',
    'repository.rbrepo',
    ]

URL = 'https://raw.githubusercontent.com/thoradia/thoradia/master/{}/{}/{}/'


def get_addon_xml(*id):
   return os.path.join(xbmcaddon.Addon(*id).getAddonInfo('path'), 'addon.xml')


if __name__ == '__main__':
    strings = xbmcaddon.Addon().getLocalizedString
    vpa_old = xbmcaddon.Addon().getSetting('vpa')
    xbmcaddon.Addon().setSetting('le', strings(30010))
    xbmcaddon.Addon().setSetting('vpa', strings(30010))

    release = None
    for repository in KNOWN_REPOSITORIES:
        try:
            release = etree.parse(get_addon_xml(repository)).iter(tag='datadir').next().text.strip('/').split('/')[-3:]
            break
        except:
            pass

    if release is not None:
        xbmcaddon.Addon().setSetting('le', strings(30011).format(*release))
        if release[2] == 'aarch64':
            if release[1] in ['WeTek_Hub', 'WeTek_Play_2']:
                release[1] = 'Odroid_C2'
        elif release[2] == 'arm':
            if release[1] in ['Odroid_C2', 'S905', 'S912', 'Slice3']:
                release[1] = 'RPi2'
            elif release[1] in ['Slice']:
                release[1] = 'RPi'
            elif release[1] in ['S805', 'WeTek_Core', 'WeTek_Hub', 'WeTek_Play_2']:
                release[1] = 'WeTek_Play'
            elif release[1] in ['MiQi', 'RK3399', 'TinkerBoard']:
                release[1] = 'RK3328'
        elif release[2] == 'x86_64':
            release[1] = 'Generic'

        url = URL.format(*release)
        xml = get_addon_xml()
        tree = etree.parse(xml)
        tag = tree.iter(tag='datadir').next()

        if tag.text == url:
            vpa_new = strings(30011).format(*release)
            xbmcaddon.Addon().setSetting('vpa', vpa_new)
            if vpa_new != vpa_old:
                xbmc.executebuiltin('UpdateAddonRepos')
        else:
            tag.text = url
            tree.iter(tag='info').next().text = url + 'addons.xml'
            tree.iter(tag='checksum').next().text = url + 'addons.xml.md5'
            tree.write(xml)
            xbmcaddon.Addon().setSetting('vpa', strings(30012).format(*release))
            if xbmcgui.Dialog().yesno(xbmcaddon.Addon().getAddonInfo('name'),
                                      strings(30013),
                                      nolabel=strings(30014),
                                      yeslabel=strings(30015)) == False:
                subprocess.call(['systemctl', 'restart', 'kodi'])
