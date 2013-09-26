#!/usr/bin/python3

import os, sys
import subprocess

has_libgd = True
all_files = []

def gen_binary_name(name):
    components = name.lower().split('.')

    if components[-1] == 'application':
        return '-'.join(components[1:-1])
    else:
        return '-'.join(components[1:])

def gen_file(to, _from=None):
    if _from is None:
        _from = to

    all_files.append(to)
    to = os.path.join(binary_name, to)
    _from = os.path.join(template_dir, _from)

    os.makedirs(os.path.dirname(to), exist_ok=True)

    print('generating %s from %s' % (to, _from))
    with open(to, 'bw') as outf:
        subprocess.check_call(['sed',
                               '-e', 's/@PACKAGE_NAME@/' + pkg_name + '/g',
                               '-e', 's/@PACKAGE_TARNAME@/' + binary_name + '/g',
                               _from], stdout=outf)

def main():
    global pkg_name, binary_name, template_dir

    pkg_name = sys.argv[1]
    binary_name = gen_binary_name(pkg_name)
    template_dir = './template'

    os.mkdir(binary_name)
    subprocess.Popen(['git', 'init'], cwd=binary_name).wait()

    FILES = [
        'autogen.sh',
        'configure.ac',
        'Makefile.am',
        'src/Makefile.am',
        'src/main.js',
        'data/Makefile.am',
        'data/icons/Makefile.am',
        'data/application.css',
        'data/app-menu.ui',
        'data/main.ui',
        'po/POTFILES.in',
        'po/POTFILES.skip',
        'git.mk',
    ]

    for f in FILES:
        gen_file(f)

    gen_file('src/' + pkg_name + '.in', 'src/app.in')
    gen_file('src/' + binary_name + '.in', 'src/launcher.in')
    gen_file('data/' + pkg_name + '.gresource.xml', 'data/gresource.xml')
    # FIXME: needs generating
    gen_file('data/' + pkg_name + '.appdata.xml.in', 'data/appdata.xml.in')
    # FIXME: needs generating
    gen_file('data/' + pkg_name + '.desktop.in.in', 'data/desktop.in.in')
    gen_file('data/' + pkg_name + '.gschema.xml.in', 'data/gschema.xml.in')
    gen_file('data/' + pkg_name + '.service.in', 'data/service.in')
    gen_file(binary_name + '.anjuta', 'project.anjuta')

    subprocess.Popen(['git', 'add'] + all_files, cwd=binary_name).wait()
    subprocess.Popen(['git', 'commit', '-m', 'Initial commit'], cwd=binary_name).wait()

if __name__ == '__main__':
    main()
