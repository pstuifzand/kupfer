# -*- coding: UTF-8 -*-
__kupfer_name__ = _("Fastmail")
__kupfer_sources__ = ("FastmailSource",)
__kupfer_actions__ = ()
__description__ = _("Fastmail new mail")
__version__ = "2020-11-15"
__author__ = "Peter Stuifzand <peter@p83.nl>"

from kupfer import utils
from kupfer.objects import RunnableLeaf, Source


class ComposeMail(RunnableLeaf):
    def __init__(self):
        RunnableLeaf.__init__(self, name=_("Compose New Email"))

    def run(self):
        utils.show_url('https://www.fastmail.com/mail/compose')

    def get_description(self):
        return _("Compose a new message in Fastmail")

    def get_icon_name(self):
        return "mail-message-new"


class FastmailSource(Source):
    def __init__(self):
        super().__init__(_("Fastmail"))

    def get_items(self):
        yield ComposeMail()

    def get_description(self):
        return None

    def get_icon_name(self):
        return "mail-message-new"
