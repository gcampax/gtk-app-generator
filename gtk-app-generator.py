#!/usr/bin/python3

import os, sys, time
import subprocess
import argparse
import shutil

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
    to = os.path.join(destdir, to)
    _from = os.path.join(template_dir, _from)

    os.makedirs(os.path.dirname(to), exist_ok=True)

    print('generating %s from %s' % (to, _from))
    with open(to, 'bw') as outf:
        args = ['sed']
        for key, value in sed_subst.items():
            args += ['-e', 's|' + key + '|' + value + '|g']
        args.append(_from)
        subprocess.check_call(args, stdout=outf)
        shutil.copystat(_from, to)

def main():
    global destdir, template_dir, sed_subst

    parser = argparse.ArgumentParser()
    parser.add_argument('pkg_name', metavar='PKG_NAME',
                        help='The application name, in reverse DNS notation (eg. com.example.Foo)')
    parser.add_argument('-o', dest='output', default='.',
                        help='Where to create the resulting repository')
    parser.add_argument('-B', '--binary-name', dest='binary_name',
                        help='The repository name and launcher binary (if not '
                        'provided, will be computed from the application name')
    parser.add_argument('-N', '--name', dest='app_name', required=True,
                        help='The human readable application name')
    parser.add_argument('--summary', dest='app_comment', default='', 
                        help='A short (one line) description of the application')
    parser.add_argument('--email', dest='email',
                        help='The author email (optional, will ask git if not provided)')
    parser.add_argument('--author-name', dest='author_name',
                        help='The author name (optional, will ask git if not provided)')
    parser.add_argument('--url', dest='url', required=True,
                        help='The application home page')
    parser.add_argument('-T', '--template', dest='template', default='js',
                        help='Which template to use (defaults to js)')

    opt = parser.parse_args(sys.argv[1:])

    pkg_name = opt.pkg_name
    binary_name = opt.binary_name or gen_binary_name(pkg_name)
    email = opt.email or subprocess.check_output(['git', 'config', 'user.email']).decode().strip()
    author_name = opt.author_name or subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
    sed_subst = { '@PACKAGE_NAME@': pkg_name,
                  '@PACKAGE_DBUS_PATH@': '/' + pkg_name.replace('.', '/'),
                  '@PACKAGE_TARNAME@': binary_name,
                  '@APPLICATION_NAME@': opt.app_name,
                  '@APPLICATION_COMMENT@': opt.app_comment,
                  '@PACKAGE_EMAIL@': email,
                  '@PACKAGE_AUTHOR@': author_name,
                  '@PACKAGE_URL@': opt.url,
                  '@YEAR@': str(time.localtime().tm_year)}

    destdir = os.path.join(opt.output, binary_name)
    template_dir = os.path.join('.', opt.template)

    with open(os.path.join(template_dir, 'template.manifest')) as tmpl:
        os.mkdir(destdir)
        subprocess.Popen(['git', 'init'], cwd=destdir).wait()

        for f in tmpl:
            f = f.strip()
            if not f or f.startswith('#'):
                continue

            if ':' in f:
                _to, _from = f.split(':')
                _to = _to.replace('@PACKAGE_NAME@', pkg_name)
                _to = _to.replace('@PACKAGE_TARNAME@', binary_name)

                gen_file(_to, _from)
            else:
                gen_file(f)

    subprocess.Popen(['git', 'add'] + all_files, cwd=destdir).wait()
    subprocess.Popen(['git', 'commit', '-m', 'Initial commit'], cwd=destdir).wait()

if __name__ == '__main__':
    main()
