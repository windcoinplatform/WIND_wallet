import math
import axolotl_curve25519 as curve
import os
import crypto as crypto
import time
import struct
import json
import base58
import base64
import logging
import requests

DEFAULT_TX_FEE = 100000
DEFAULT_BASE_FEE = DEFAULT_TX_FEE
DEFAULT_SMART_FEE = 400000
DEFAULT_ASSET_FEE = 100000000
DEFAULT_MATCHER_FEE = 300000
DEFAULT_LEASE_FEE = 100000
DEFAULT_ALIAS_FEE = 100000
DEFAULT_SPONSOR_FEE = 100000000
DEFAULT_SCRIPT_FEE = 100000
DEFAULT_ASSET_SCRIPT_FEE = 100000000
DEFAULT_SET_SCRIPT_FEE = 1000000
DEFAULT_INVOKE_SCRIPT_FEE = 500000
DEFAULT_CURRENCY = 'WAVES'
VALID_TIMEFRAMES = (5, 15, 30, 60, 240, 1440)
MAX_WDF_REQUEST = 100
THROW_EXCEPTION_ON_ERROR = False
OFFLINE = False
NODE = 'http://144.91.84.27:6869'
ADDRESS_VERSION = 1
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

CHAIN = 'custom'
CHAIN_ID = 'R'

class PyWindException(ValueError):
    pass

def throw_error(msg):
    if THROW_EXCEPTION_ON_ERROR:
        raise PyWindException(msg)

def setThrowOnError(throw=True):
    global THROW_EXCEPTION_ON_ERROR
    THROW_EXCEPTION_ON_ERROR = throw


def setOffline():
    global OFFLINE
    OFFLINE = True

def setOnline():
    global OFFLINE
    OFFLINE = False

def wrapper(api, postData='', host='', headers=''):
    global OFFLINE
    if OFFLINE:
        offlineTx = {}
        offlineTx['api-type'] = 'POST' if postData else 'GET'
        offlineTx['api-endpoint'] = api
        offlineTx['api-data'] = postData
        return offlineTx
    if not host:
        host = NODE
    if postData:
        req = requests.post('%s%s' % (host, api), data=postData, headers={'content-type': 'application/json'}).json()
    else:
        req = requests.get('%s%s' % (host, api), headers=headers).json()
    return req

def height():
    return wrapper('/blocks/height')['height']


def lastblock():
    return wrapper('/blocks/last')

def block(n):
    return wrapper('/blocks/at/%d' % n)

def tx(id):
    return wrapper('/transactions/info/%s' % id)

def validateAddress(address):
    addr = crypto.bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != CHAIN_ID:
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False



class Asset(object):
    def __init__(self, assetId):
        self.assetId='' if assetId == DEFAULT_CURRENCY else assetId
        self.issuer = self.name = self.description = ''
        self.quantity = self.decimals = 0
        self.reissuable = False
        if self.assetId=='':
            self.quantity=100000000e8
            self.decimals=8
        else:
            self.status()

    def __str__(self):
        return 'status = %s\n' \
               'assetId = %s\n' \
               'issuer = %s\n' \
               'name = %s\n' \
               'description = %s\n' \
               'quantity = %d\n' \
               'decimals = %d\n' \
               'reissuable = %s' % (self.status(), self.assetId, self.issuer, self.name, self.description, self.quantity, self.decimals, self.reissuable)

    __repr__ = __str__

    def status(self):
        if self.assetId!=DEFAULT_CURRENCY:
            try:
                req = wrapper('/transactions/info/%s' % self.assetId)
                if req['type'] == 3:
                    self.issuer = req['sender']
                    self.quantity = req['quantity']
                    self.decimals = req['decimals']
                    self.reissuable = req['reissuable']
                    self.name = req['name'].encode('ascii', 'ignore')
                    self.description = req['description'].encode('ascii', 'ignore')
                    return 'Issued'
            except:
                pass

    def isSmart(self):
        req = wrapper('/transactions/info/%s' % self.assetId)

        if ('script' in req and req['script']):
            return True
        else:
            return False

class AssetPair(object):
    def __init__(self, asset1, asset2):
        self.asset1 = asset1
        self.asset2 = asset2
        self.a1 = DEFAULT_CURRENCY if self.asset1.assetId == '' else self.asset1.assetId
        self.a2 = DEFAULT_CURRENCY if self.asset2.assetId == '' else self.asset2.assetId

    def __str__(self):
        return 'asset1 = %s\nasset2 = %s' % (self.asset1.assetId, self.asset2.assetId)

    def refresh(self):
        self.asset1.status()
        self.asset2.status()


    def first(self):
        if len(self.asset1.assetId) < len(self.asset2.assetId):
            return self.asset1
        elif self.asset1.assetId < self.asset2.assetId:
            return self.asset1
        else:
            return self.asset2

    def second(self):
        if len(self.asset1.assetId) < len(self.asset2.assetId):
            return self.asset2
        if self.asset1.assetId < self.asset2.assetId:
            return self.asset2
        else:
            return self.asset1

    def orderbook(self):
        req = wrapper('/matcher/orderbook/%s/%s' % (self.a1, self.a2), host=MATCHER)
        return req

    def ticker(self):
        return wrapper('/api/ticker/%s/%s' % (self.a1, self.a2), host=DATAFEED)

    def last(self):
        return str(self.ticker()['24h_close'])

    def open(self):
        return str(self.ticker()['24h_open'])

    def high(self):
        return str(self.ticker()['24h_high'])

    def low(self):
        return str(self.ticker()['24h_low'])

    def close(self):
        return self.last()

    def vwap(self):
        return str(self.ticker()['24h_vwap'])

    def volume(self):
        return str(self.ticker()['24h_volume'])

    def priceVolume(self):
        return str(self.ticker()['24h_priceVolume'])

    def _getMarketData(self, method, params):
        return wrapper('%s/%s/%s/%s' % (method, self.a1, self.a2, params), host=DATAFEED)

    def trades(self, *args):
        if len(args)==1:
            limit = args[0]
            if limit > 0 and limit <= MAX_WDF_REQUEST:
                return self._getMarketData('/api/trades/', '%d' % limit)
            else:
                msg = 'Invalid request. Limit must be >0 and <= 100'
                throw_error(msg)
                return logging.error(msg)
        elif len(args)==2:
            fromTimestamp = args[0]
            toTimestamp = args[1]
            return self._getMarketData('/api/trades', '%d/%d' % (fromTimestamp, toTimestamp))

    def candles(self, *args):
        if len(args)==2:
            timeframe = args[0]
            limit = args[1]
            if timeframe not in VALID_TIMEFRAMES:
                msg = 'Invalid timeframe'
                throw_error(msg)
                return logging.error(msg)
            elif limit > 0 and limit <= MAX_WDF_REQUEST:
                return self._getMarketData('/api/candles', '%d/%d' % (timeframe, limit))
            else:
                msg = 'Invalid request. Limit must be >0 and <= 100'
                throw_error(msg)
                return logging.error(msg)
        elif len(args)==3:
            timeframe = args[0]
            fromTimestamp = args[1]
            toTimestamp = args[2]
            if timeframe not in VALID_TIMEFRAMES:
                msg = 'Invalid timeframe'
                throw_error(msg)
                return logging.error(msg)
            else:
                return self._getMarketData('/api/candles', '%d/%d/%d' % (timeframe, fromTimestamp, toTimestamp))

    __repr__ = __str__

