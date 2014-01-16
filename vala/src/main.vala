// -*- Mode: vala; indent-tabs-mode: nil; c-basic-offset: 4; tab-width: 4 -*-
//
// Copyright (c) 2013 Giovanni Campagna <scampa.giovanni@gmail.com>
//
// Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are met:
//   * Redistributions of source code must retain the above copyright
//     notice, this list of conditions and the following disclaimer.
//   * Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//   * Neither the name of the GNOME Foundation nor the
//     names of its contributors may be used to endorse or promote products
//     derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

internal Main.Application getApp()
{
    return (Main.Application)GLib.Application.get_default();
}

namespace Main
{

class Application : Gtk.Application
{
    const GLib.ActionEntry[] action_entries = {
        { "quit", on_quit }
    };

    public Application()
    {
        Object(application_id: Config.PACKAGE_NAME,
               flags: Package.app_flags);

        if ((this.flags & GLib.ApplicationFlags.IS_SERVICE) != 0)
            this.inactivity_timeout = 60000;

        GLib.Environment.set_application_name(_("@APPLICATION_NAME@"));
    }

    private void on_quit()
    {
        this.quit();
    }

    private void init_app_menu()
    {
        var builder = new Gtk.Builder();
        try {
            builder.add_from_resource("@PACKAGE_DBUS_PATH@/app-menu.ui");
        } catch(GLib.Error e) {
            assert_not_reached();
        }

        var menu = builder.get_object("app-menu") as GLib.Menu;
        this.set_app_menu(menu);
    }

    protected override void startup()
    {
        base.startup();

        Util.load_style_sheet("@PACKAGE_DBUS_PATH@/application.css");

        this.add_action_entries(action_entries, this);
        this.init_app_menu();
    }

    protected override void activate()
    {
        (new Window.MainWindow(this)).show();
    }

    protected override void shutdown()
    {
        base.shutdown();
    }
}

}

int main(string[] argv)
{
    Package.init(argv);
    Package.init_gettext();

    return (new Main.Application()).run(argv);
}
