__kupfer_name__ = _("Brotab")
__kupfer_sources__ = ("TabSource",)
__kupfer_actions__ = ("TabActivate", "TabClose",)
__description__ = _("Firefox Tabs")
__version__ = "2020.1"
__author__ = "Peter Stuifzand <peter@p83.nl>"

import os

from kupfer import utils, scheduler
from kupfer.objects import Source, Leaf, Action


def get_tabs():
    pipe = os.popen("brotab list")
    output = pipe.read()
    for line in output.splitlines():
        fields = line.split("\t")
        if len(fields) == 3:
            tab_id, title, url = fields
            yield tab_id, title, url


class TabLeaf(Leaf):
    """
    Tab leaf

    This Leaf represents a tab from Brotab in Firefox
    """

    def __init__(self, tab_id, title, url):
        self.title = title
        self.url = url
        super(TabLeaf, self).__init__(tab_id, title)

    def get_description(self):
        return self.url


class ActiveTabLeaf(TabLeaf):
    qf_id = "active-tab"

    def __init__(self):
        TabLeaf.__init__(self, None, "Active Tab", "")

    def _get_object(self):
        pipe = os.popen("brotab active")
        output = pipe.read()
        for line in output.splitlines():
            fields = line.split("\t")
            return fields[0]
        return None

    def _set_object(self, obj):
        pass

    object = property(_get_object, _set_object)

    def get_description(self):
        return "The active tab"


class TabSource(Source):
    """
    Tab source

    This Source contains all Tabs from Firefox (as given by Brotab)
    """
    source_use_cache = False
    task_update_interval_sec = 5

    def __init__(self, name=None):
        super().__init__(name or _("Firefox Tabs"))
        self._cache = []
        self._timer = None

    def initialize(self):
        self._timer = scheduler.Timer()

    def finalize(self):
        self._timer = None
        self._cache = []

    def _get_tabs_finished(self, acommand, stdout, stderr):
        self._cache = []
        for line in stdout.split(b'\n'):
            line = line.decode("utf-8", "replace").strip()
            fields = line.split("\t")
            if len(fields) == 3:
                tab_id, title, url = fields
                self._cache.append(TabLeaf(tab_id, title, url))
        self.mark_for_update()

    def _get_tabs_start(self):
        utils.AsyncCommand(['brotab', 'list'],
                           self._get_tabs_finished, 60, env=[])

    def get_items(self):
        yield ActiveTabLeaf()

        for tab in self._cache:
            yield tab
        update_wait = self.task_update_interval_sec if self._cache else 0
        # update after a few seconds
        self._timer.set(update_wait, self._get_tabs_start)

    def get_description(self):
        return _("Firefox browser tabs")

    def provides(self):
        yield ActiveTabLeaf
        yield TabLeaf


class TabActivate(Action):

    def __init__(self):
        super().__init__(_("Activate Tab"))

    def activate(self, obj, iobj=None, ctx=None):
        utils.spawn_async(['brotab', 'activate', obj.object])

    def item_types(self):
        yield TabLeaf


class TabClose(Action):

    def __init__(self):
        super().__init__(_("Close Tab"))

    def activate(self, obj, iobj=None, ctx=None):
        utils.spawn_async(['brotab', 'close', obj.object])

    def item_types(self):
        yield TabLeaf
