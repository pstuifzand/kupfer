__kupfer_name__ = _("Join API")
__kupfer_sources__ = ("JoinDevicesSource",)
__kupfer_actions__ = (
    "JoinSendUrlAction",
    "JoinSendCommandAction",
    "JoinSendClipboardAction",
)
__description__ = _("Join API devices")
__version__ = "2020-11-17"
__author__ = "Peter Stuifzand <peter@p83.nl>"

import urllib.request, urllib.parse
import json

from kupfer import plugin_support
from kupfer.obj.objects import TextLeaf
from kupfer.objects import Source, Leaf, Action
from kupfer.objects import UrlLeaf

__kupfer_settings__ = plugin_support.PluginSettings(
    {
        "key": "api_key",
        "label": _("Join API key"),
        "type": str,
        "value": "",
    },
)


class JoinDeviceLeaf(Leaf):
    def get_description(self):
        return _("Join Device")


class JoinSendUrlAction(Action):
    def __init__(self):
        super(JoinSendUrlAction, self).__init__(_("Send URL"))

    def activate(self, obj, iobj=None, ctx=None):
        api_key = __kupfer_settings__["api_key"]
        query = {"url": obj.object, "deviceId": iobj.object['deviceId'], "apikey": api_key}
        path = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?' + urllib.parse.urlencode(query)
        resp = urllib.request.urlopen(path)
        if resp.status != 200:
            raise ValueError('Invalid response %d, %s' % (resp.status, resp.reason))

    def requires_object(self):
        return True

    def item_types(self):
        yield UrlLeaf
        yield TextLeaf

    def object_types(self):
        yield JoinDeviceLeaf


class JoinSendCommandAction(Action):
    def __init__(self):
        super(JoinSendCommandAction, self).__init__(_("Send Join Command"))

    def activate(self, obj, iobj=None, ctx=None):
        api_key = __kupfer_settings__["api_key"]
        query = {"text": obj.object, "deviceId": iobj.object['deviceId'], "apikey": api_key}
        path = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?' + urllib.parse.urlencode(query)
        resp = urllib.request.urlopen(path)
        if resp.status != 200:
            raise ValueError('Invalid response %d, %s' % (resp.status, resp.reason))

    def requires_object(self):
        return True

    def item_types(self):
        yield UrlLeaf
        yield TextLeaf

    def object_types(self):
        yield JoinDeviceLeaf


class JoinSendClipboardAction(Action):
    def __init__(self):
        super(JoinSendClipboardAction, self).__init__(_("Send To Clipboard"))

    def activate(self, obj, iobj=None, ctx=None):
        api_key = __kupfer_settings__["api_key"]
        query = {"clipboard": obj.object, "deviceId": iobj.object['deviceId'], "apikey": api_key}
        path = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?' + urllib.parse.urlencode(query)
        resp = urllib.request.urlopen(path)
        if resp.status != 200:
            raise ValueError('Invalid response %d, %s' % (resp.status, resp.reason))

    def requires_object(self):
        return True

    def item_types(self):
        yield UrlLeaf
        yield TextLeaf

    def object_types(self):
        yield JoinDeviceLeaf


class JoinDevicesSource(Source):
    def __init__(self):
        super().__init__(_("Join Devices"))
        self.api_key = __kupfer_settings__["api_key"]
        path = 'https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices?apikey={}'
        self.path = path.format(self.api_key)

    def get_items(self):
        resp = urllib.request.urlopen(self.path)
        if resp.status != 200:
            raise ValueError('Invalid response %d, %s' % (resp.status, resp.reason))

        result = resp.read()
        body = result.strip().decode("utf-8")
        data = json.loads(body)

        for device in data['records']:
            yield JoinDeviceLeaf(device, device['deviceName'])

    def get_description(self):
        return _("Index of Join devices")

    def get_gicon(self):
        return self.get_leaf_repr() and self.get_leaf_repr().get_gicon()

    def provides(self):
        yield JoinDeviceLeaf
