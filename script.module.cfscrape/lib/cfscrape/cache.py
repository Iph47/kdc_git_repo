# -*- coding: UTF-8 -*-
import xbmc
import xbmcaddon
import xbmcvfs

import time
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from sqlite3 import dbapi2 as db, OperationalError
except ImportError:
    from pysqlite2 import dbapi2 as db, OperationalError

cache_table = 'cache'
dataPath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8')
cacheFile = os.path.join(dataPath, 'cache.db')


def setScraper(scraper, baseLink):
    if not _is_cache_valid(0.01, str(baseLink)):
        cache_delete(str(baseLink))

    cache_insert(str(baseLink), pickle.dumps(scraper, protocol=pickle.HIGHEST_PROTOCOL))


def getScraper(baseLink):
    cache_result = cache_get(str(baseLink))
    if cache_result:
        if _is_cache_valid(cache_result['date'], 1):
            return pickle.loads(cache_result['value'])
        else:
            cache_delete(str(baseLink))


def cache_get(key):
    # type: (str, str) -> dict or None
    try:
        cursor = _get_connection_cursor()
        cursor.execute("SELECT * FROM %s WHERE key = ?" % cache_table, [key])
        return cursor.fetchone()
    except OperationalError:
        return None


def cache_delete(key):
    # type: (str, str) -> dict or None
    try:
        cursor = _get_connection_cursor()
        cursor.execute("DELETE FROM %s WHERE key = ?" % cache_table, [key])
        cursor.connection.commit()
    except OperationalError:
        return None


def cache_insert(key, value):
    # type: (str, str) -> None
    cursor = _get_connection_cursor()
    now = int(time.time())
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS %s (key TEXT, value TEXT, date INTEGER, UNIQUE(key))"
        % cache_table
    )
    update_result = cursor.execute(
        "UPDATE %s SET value=?,date=? WHERE key=?"
        % cache_table, (value, now, key))

    if update_result.rowcount is 0:
        cursor.execute(
            "INSERT INTO %s Values (?, ?, ?)"
            % cache_table, (key, value, now)
        )

    cursor.connection.commit()


def _get_connection_cursor():
    conn = _get_connection(cacheFile)
    conn.text_factory = str
    return conn.cursor()


def _get_connection(filename):
    xbmcvfs.mkdir(dataPath)
    conn = db.connect(filename)
    conn.row_factory = _dict_factory
    return conn


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _is_cache_valid(cached_time, cache_timeout):
    now = int(time.time())
    diff = now - cached_time
    return (cache_timeout * 3600) > diff
