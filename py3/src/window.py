# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 4; tab-width: 4 -*-
#
# Copyright (c) 2013 Giovanni Campagna <scampa.giovanni@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the GNOME Foundation nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from gi.repository import GLib, GObject, Gtk

import util

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, title=None, default_width=640, default_height=480, **kw):
        if not title:
            title = GLib.get_application_name()
        super().__init__(title=title,
                         default_width=default_width, default_height=default_height,
                         **kw)

        util.init_actions(self,
                          [{ 'name': 'about',
                             'activate': self._about }])

        builder = Gtk.Builder()
        builder.add_from_resource('@PACKAGE_DBUS_PATH@/main.ui')

        self.set_titlebar(builder.get_object('main-header'))

        grid = builder.get_object('main-grid')
        self.add(grid)

    def _about(self, action, parameter):
        aboutDialog = Gtk.AboutDialog(
            authors=[ '@PACKAGE_AUTHOR@ <@PACKAGE_EMAIL@>' ],
            translator_credits=_("translator-credits"),
            program_name=_("@APPLICATION_NAME@"),
            comments=_("@APPLICATION_COMMENT@"),
            copyright='Copyright @YEAR@ The @APPLICATION_NAME@ developers',
            license_type=Gtk.License.GPL_2_0,
            logo_icon_name=pkg.name,
            version=pkg.version,
            website='@PACKAGE_URL@',
            wrap_license=True,
            modal=True,
            transient_for=self
        )

        aboutDialog.show()
        aboutDialog.connect('response', lambda dialog, id: dialog.destroy())
