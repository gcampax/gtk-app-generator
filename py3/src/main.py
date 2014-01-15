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

pkg.init_gettext()

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gio', '2.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gio, GLib, Gtk

import util, window

def init_environment():
    import builtins
    builtins.__dict__['getApp'] = lambda: Gio.Application.get_default()

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=pkg.name, flags=pkg.appFlags)

        if self.get_flags() & Gio.ApplicationFlags.IS_SERVICE:
            self.set_inactivity_timeout(60000)

        GLib.set_application_name(_("@APPLICATION_NAME@"))

    def _on_quit(self, action, parameter):
        self.quit()

    def _init_app_menu(self):
        builder = Gtk.Builder()
        builder.add_from_resource('@PACKAGE_DBUS_PATH@/app-menu.ui')

        menu = builder.get_object('app-menu')
        self.set_app_menu(menu)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        util.load_style_sheet('@PACKAGE_DBUS_PATH@/application.css')

        util.init_actions(self,
                          [{ 'name': 'quit',
                             'activate': self._on_quit }])
        self._init_app_menu()

    def do_activate(self):
        (window.MainWindow(application=self)).show()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

def main(argv):
    init_environment()

    return (Application()).run(argv)
