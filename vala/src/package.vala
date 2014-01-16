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

namespace Package
{
    public GLib.ApplicationFlags app_flags;
    public string prefix;
    public string datadir;
	public string libdir;
    public string pkgdatadir;
    public string pkglibdir;
    public string pkglibexecdir;
    private string _localedir;
    public bool from_source;

    private bool running_from_source(string argv0)
    {
        var prgname = GLib.Path.get_basename(argv0);

        var binary = GLib.File.new_for_path(argv0);
        var source = GLib.File.new_for_path("./src/" + prgname);

        return binary.equal(source);
    }

    public void	init(string[] argv)
    {
        app_flags = 0;

        GLib.Environment.set_prgname(Config.PACKAGE_NAME);

        prefix = Config.PREFIX;
        libdir = Config.LIBDIR;
        datadir = GLib.Path.build_filename(prefix, "share");

        if (running_from_source(argv[0])) {
            message("Running from source tree, using local files");

            from_source = true;
            var _base = GLib.Environment.get_current_dir();
            pkglibdir = GLib.Path.build_filename(_base, "lib");
            pkgdatadir = GLib.Path.build_filename(_base, "data");
            pkglibexecdir = GLib.Path.build_filename(_base, "src");
            _localedir = GLib.Path.build_filename(_base, "po");
		} else {
            app_flags |= GLib.ApplicationFlags.IS_SERVICE;

            pkglibdir = GLib.Path.build_filename(libdir, Config.PACKAGE_NAME);
            pkgdatadir = GLib.Path.build_filename(datadir, Config.PACKAGE_NAME);
            pkglibexecdir = GLib.Path.build_filename(prefix, "lib", Config.PACKAGE_NAME);
			_localedir = GLib.Path.build_filename(datadir, "locale");
        }
    }

    public void init_gettext() {
        GLib.Intl.bindtextdomain(Config.PACKAGE_NAME, _localedir);
        GLib.Intl.textdomain(Config.PACKAGE_NAME);
    }
}
