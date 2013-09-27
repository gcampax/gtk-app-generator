# Copyright 2012 Giovanni Campagna
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# This module provides a set of convenience APIs for building packaged
# applications.

from gi.repository import GLib, GIRepository, Gio
import sys
import gettext

# < public >
name = None
version = None
appFlags = 0
prefix = None
datadir = None
libdir = None
pkgdatadir = None
pkglibdir = None
moduledir = None
localedir = None

# < private >
_base = None
_requires = None

def _runningFromSource():
    fileName = sys.argv[0]
    prgName = GLib.path_get_basename(fileName)

    binary = Gio.File.new_for_path(fileName)
    sourceBinary = Gio.File.new_for_path('./src/' + prgName)
    return binary.equal(sourceBinary);

def init(_name, _version, _prefix, _libdir, _flags=0):
    """
    @params: package parameters

    Initialize directories and global variables. Must be called
    before any of other API in Package is used.
    @params must be an object with at least the following keys:
    - name: the package name ($(PACKAGE_NAME) in autotools)
    - version: the package version
    - prefix: the installation prefix

    init() will take care to check if the program is running from
    the source directory or not, by looking for a 'src' directory.

    At the end, the global variable 'pkg' will contain the
    Package module (imports.package). Additionally, the following
    module variables will be available:
    - name, version: same as in @params
    - prefix: the installation prefix (as passed in @params)
    - datadir, libdir: the final datadir and libdir when installed;
                       usually, these would be prefix + '/share' and
                       and prefix + '/lib' (or '/lib64')
    - pkgdatadir: the directory to look for private data files, such as
                  images, stylesheets and UI definitions;
                  this will be datadir + name when installed and
                  './data' when running from the source tree
    - pkglibdir: the directory to look for private typelibs and C
                 libraries;
                 this will be libdir + name when installed and
                 './lib' when running from the source tree
    - moduledir: the directory to look for JS modules;
                 this will be pkglibdir when installed and
                 './src' when running from the source tree
    - localedir: the directory containing gettext translation files;
                 this will be datadir + '/locale' when installed
                 and './po' in the source tree

    All paths are absolute and will not end with '/'.

    As a side effect, init() calls GLib.set_prgname().
    """

    import builtins
    builtins.__dict__['pkg'] = sys.modules[__name__]

    global name, version, appFlags, prefix, libdir, datadir
    global pkglibdir, libpath, pkgdatadir, localedir, moduledir
    global _base

    name = _name
    version = _version
    appFlags = _flags

    # Must call it first, because it can only be called
    # once, and other library calls might have it as a
    # side effect
    GLib.set_prgname(name)

    prefix = _prefix
    libdir = _libdir
    datadir = GLib.build_filenamev([prefix, 'share'])

    if _runningFromSource():
        print('Running from source tree, using local files')

        # Running from source directory
        _base = GLib.get_current_dir()
        pkglibdir = GLib.build_filenamev([_base, 'lib'])
        libpath = GLib.build_filenamev([pkglibdir, '.libs'])
        girpath = pkglibdir
        pkgdatadir = GLib.build_filenamev([_base, 'data'])
        localedir = GLib.build_filenamev([_base, 'po'])
        moduledir = GLib.build_filenamev([_base, 'src'])
    else:
        appFlags |= Gio.ApplicationFlags.IS_SERVICE

        _base = prefix
        pkglibdir = GLib.build_filenamev([libdir, name])
        libpath = pkglibdir
        girpath = GLib.build_filenamev([pkglibdir, 'girepository-1.0'])
        pkgdatadir = GLib.build_filenamev([datadir, name])
        localedir = GLib.build_filenamev([datadir, 'locale'])
        moduledir = pkgdatadir

    sys.path.insert(0, moduledir)
    GIRepository.Repository.prepend_search_path(girpath)
    GIRepository.Repository.prepend_library_path(libpath)

def start(args=None, **kw):
    """
    @params: see init()

    This is a convenience function if your package has a
    single entry point.
    You must define a main(ARGV) function inside a main.js
    module in moduledir.
    """

    args = args or sys.argv
    init(**kw)

    import main
    return main.main(args)

def init_gettext():
    gettext.install(name, localedir=localedir)

def init_submodule(name):
    if moduledir != pkgdatadir:
        # Running from source tree, add './name' to search paths

        submoduledir = GLib.build_filenamev([_base, name])
        libpath = GLib.build_filenamev([submoduledir, '.libs'])
        GIRepository.Repository.prepend_search_path(submoduledir)
        GIRepository.Repository.prepend_library_path(libpath)
    else:
        # Running installed, submodule is in $(pkglibdir), nothing to do
        pass

def init_resources():
    resource = Gio.Resource.load(GLib.build_filenamev([pkgdatadir,
                                                       name + '.gresource']))
    resource._register()

# Launcher support

def _launcherUsage(_flags):
    print('Usage:')

    name = GLib.path_get_basename(sys.argv[0])
    if flags & Gio.ApplicationFlags.HANDLES_OPEN:
        print('  ' + name + ' [OPTION...] [FILE...]\n')
    else:
        print('  ' + name + ' [OPTION...]\n')

    print('Options:')
    print('  -h, --help   Show this help message')
    print('  --version    Show the application version')

def _parseLaunchArgs(args, _name, _version, _flags):
    newArgs = []

    for arg in args:
        if arg == '--':
            newArgs.concat(args.slice(i))
            return newArgs

        elif arg in ('--help', '-h'):
            _launcherUsage(params.flags)
            sys.exit(0)

        elif arg == '--version':
            print(params.name + ' ' + params.version)
            sys.exit(0)
            break

        else:
            newArgs.append(arg)

    return newArgs

def launch(_name, _version, _prefix, _libdir, _flags=0):
    args = _parseLaunchArgs(sys.argv, _name=_name, _version=_version, _flags=_flags)

    if _runningFromSource():
        return start(args, _name=_name, _version=_version,
                     _flags=_flags, _prefix=_prefix, _libdir=_libdir)
    else:
        _flags |= Gio.ApplicationFlags.IS_LAUNCHER

        app = Gio.Application(application_id=_name, flags=_flags)
        return app.run(args)
