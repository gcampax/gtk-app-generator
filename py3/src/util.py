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

from gi.repository import Gdk, Gio, GObject, Gtk
import sys

def load_ui(resourcePath, objects=None):
    ui = Gtk.Builder()

    if objects:
        for o in objects:
            ui.expose_object(o, objects[o])

    ui.add_from_resource(resourcePath)
    return ui

def load_style_sheet(resource):
    provider = Gtk.CssProvider()
    provider.load_from_file(Gio.File.new_for_uri('resource://' + resource))
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                             provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def init_actions(actionMap, simpleActionEntries):
    for entry in simpleActionEntries:
        activate = None
        state_changed = None

        if 'activate' in entry:
            activate = entry['activate']
            del(entry['activate'])
        if 'state_changed' in entry:
            state_changed = entry['state_changed']
            del(entry['state_changed'])

        action = Gio.SimpleAction(**entry)

        if activate:
            action.connect('activate', activate)
        if state_changed:
            action.connect('state-changed', state_changed)

        actionMap.add_action(action)

def get_settings(schemaId, path=None):
    GioSSS = Gio.SettingsSchemaSource

    if pkg.moduledir != pkg.pkgdatadir:
        # Running from the source tree
        schemaSource = GioSSS.new_from_directory(pkg.pkgdatadir,
                                                 GioSSS.get_default(),
                                                 False)
    else:
        schemaSource = GioSSS.get_default()

    schemaObj = schemaSource.lookup(schemaId, True)
    if not schemaObj:
        print('Missing GSettings schema ' + schemaId)
        sys.exit(1)

    if not path:
        return Gio.Settings(settings_schema=schemaObj)
    else:
        return Gio.Settings(settings_schema=schemaObj,
                            path=path)

def load_icon(iconName, size):
    theme = Gtk.IconTheme.get_default()
    return theme.load_icon(iconName, size, Gtk.IconLookupFlags.GENERIC_FALLBACK)
