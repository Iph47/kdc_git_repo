import os
import sys
import time
import urllib
from urllib2 import HTTPError, URLError
import urlparse

from clouddrive.common.account import AccountManager
from clouddrive.common.exception import UIException
from clouddrive.common.remote.request import Request
from clouddrive.common.ui.dialog import DialogProgress, DialogProgressBG, QRDialogProgress
from clouddrive.common.ui.logger import Logger
from clouddrive.common.ui.utils import KodiUtils
from clouddrive.common.utils import Utils
import xbmcgui
import xbmcplugin
from datetime import timedelta, datetime


from resources.lib.modules.googledrive import GoogleDrive

class Drive():

    _DEFAULT_SIGNIN_TIMEOUT = 120
    _addon = None
    _addon_handle = None
    _addonid = None
    _addon_name = None
    _addon_params = None
    _addon_url = None
    _addon_version = None
    _common_addon = None
    _cancel_operation = False
    _content_type = None
    _dialog = None
    _child_count_supported = True
    _load_target = 0
    _load_count = 0
    _profile_path = None
    _progress_dialog = None
    _progress_dialog_bg = None
    _system_monitor = None
    _account_manager = None
    _ip_before_pin = None
    
    def __init__(self):
        self._addon = KodiUtils.get_addon()
        self._addonid = self._addon.getAddonInfo('id')
        self._addon_name = self._addon.getAddonInfo('name')
        self._addon_url = sys.argv[0]
        self._addon_version = self._addon.getAddonInfo('version')
        self._common_addon_id = 'script.module.clouddrive.common'
        self._common_addon = KodiUtils.get_addon(self._common_addon_id)
        self._common_addon_version = self._common_addon.getAddonInfo('version')
        self._dialog = xbmcgui.Dialog()
        self._profile_path = Utils.unicode(KodiUtils.translate_path(self._addon.getAddonInfo('profile')))
        self._progress_dialog = DialogProgress(self._addon_name)
        self._progress_dialog_bg = DialogProgressBG(self._addon_name)
        self._system_monitor = KodiUtils.get_system_monitor()
        self._account_manager = AccountManager(self._profile_path)
        self._pin_dialog = None
        self.provider = GoogleDrive()

    def cancel_operation(self):
        return self._system_monitor.abortRequested() or self._progress_dialog.iscanceled() or self._cancel_operation or (self._pin_dialog and self._pin_dialog.iscanceled())

    def get_provider(self):
        return self.provider

    def add_acc(self):
        request_params = {
            'waiting_retry': lambda request, remaining: self._progress_dialog_bg.update(
                int((request.current_delay - remaining)/request.current_delay*100),
                heading='Something happened with the request%s.' % ('' if request.current_tries == 1 else ' again'),
                message='Will try in %s seconds.' % str(int(remaining)) + ' ' +
                        'Attempt %s of %s.' % (str(request.current_tries + 1), str(request.tries))
            ),
            'on_complete': lambda request: (self._progress_dialog.close(), self._progress_dialog_bg.close()),
            'cancel_operation': self.cancel_operation,
            'wait': self._system_monitor.waitForAbort
        }
        provider = self.get_provider()
        self._progress_dialog.update(0, "Connecting with server, please wait...")
        
        self._ip_before_pin = Request(KodiUtils.get_signin_server() + '/ip', None).request()
        pin_info = provider.create_pin(request_params)
        self._progress_dialog.close()
        if self.cancel_operation():
            return
        if not pin_info:
            raise Exception('Unable to retrieve a pin code')

        tokens_info = {}
        request_params['on_complete'] = lambda request: self._progress_dialog_bg.close()
        self._pin_dialog = QRDialogProgress.create(self._addon_name,
                                      KodiUtils.get_signin_server() + '/signin/%s' % pin_info['pin'], 
                                      'Scan the QR code and sign in.', 
                                      'or[CR]Go to this URL: %s[CR]enter the code and sign in: %s' % ('[B]%s[/B]' % KodiUtils.get_signin_server(), '[B][COLOR lime]%s[/COLOR][/B]' % pin_info['pin']))
        self._pin_dialog.show()
        max_waiting_time = time.time() + self._DEFAULT_SIGNIN_TIMEOUT
        while not self.cancel_operation() and max_waiting_time > time.time():
            remaining = round(max_waiting_time-time.time())
            percent = int(remaining/self._DEFAULT_SIGNIN_TIMEOUT*100)
            self._pin_dialog.update(percent, line3='[CR]'+'Expires in %s seconds...' % str(int(remaining)))
            if int(remaining) % 5 == 0 or remaining == 1:
                tokens_info = provider.fetch_tokens_info(pin_info, request_params = request_params)
                if self.cancel_operation() or tokens_info:
                    break
            if self._system_monitor.waitForAbort(1):
                break
        self._pin_dialog.close()  
        
        if self.cancel_operation() or time.time() >= max_waiting_time:
            return
        if not tokens_info:
            raise Exception('Unable to retrieve the auth2 tokens')
        
        self._progress_dialog.update(25, self._common_addon.getLocalizedString(32064),' ',' ')
        try:
            account = provider.get_account(request_params = request_params, access_tokens = tokens_info)
        except Exception as e:
            raise UIException(32065, e)
        if self.cancel_operation():
            return
        
        self._progress_dialog.update(50, self._common_addon.getLocalizedString(32017))
        try:
            account['drives'] = provider.get_drives(request_params = request_params, access_tokens = tokens_info)
        except Exception as e:
            raise UIException(32018, e)
        if self.cancel_operation():
            return
        
        self._progress_dialog.update(75, self._common_addon.getLocalizedString(32020))
        try:
            account['access_tokens'] = tokens_info
            self._account_manager.add_account(account)
        except Exception as e:
            raise UIException(32021, e)
        if self.cancel_operation():
            return
        
        self._progress_dialog.update(90)
        try:
            accounts = self._account_manager.load()
            for drive in account['drives']:
                driveid = drive['id']
                Logger.debug('Looking for account %s...' % driveid)
                if driveid in accounts:
                    drive = accounts[driveid]['drives'][0]
                    Logger.debug(drive)
                    if drive['id'] == driveid and drive['type'] == 'migrated':
                        Logger.debug('Account %s removed.' % driveid)
                        self._account_manager.remove_account(driveid)
                        
        except Exception as e:
            pass
        if self.cancel_operation():
            return
        
        self._progress_dialog.close()
        KodiUtils.executebuiltin('Container.Refresh')

    def _get_display_name(self, account, drive=None, with_format=False):
        return self._account_manager.get_account_display_name(account, drive, self.get_provider(), with_format)
    
    def get_accounts(self, with_format=False):
        accounts = self._account_manager.load()
        for account_id in accounts:
            account = accounts[account_id]
            for drive in account['drives']:
                drive['display_name'] = self._get_display_name(account, drive, with_format)
        return accounts

    def list_accounts(self):
        accounts = self.get_accounts(with_format=True)
        listing = []
        for account_id in accounts:
            account = accounts[account_id]
            size = len(account['drives'])
            for drive in account['drives']:
                listing.append(( drive['id']))
        return listing


    def list_folder(self, driveid, item_driveid=None, item_id=None, path=None):
        self.get_provider().configure(self._account_manager, driveid)
        if self._child_count_supported:
            item = self.get_provider().get_item(item_driveid, item_id, path)
            if item:
                self._load_target = item['folder']['child_count']
       
        items = self.get_provider().get_folder_items(item_driveid, item_id, path, on_items_page_completed = 'None')
        return items

    def get_item_play_url(self, driveid, item_driveid=None, item_id=None):
        self.get_provider().configure(self._account_manager, driveid)
        return self.get_provider().get_item(item_driveid, item_id, include_download_info = True)
