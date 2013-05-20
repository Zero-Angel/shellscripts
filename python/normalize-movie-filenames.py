#!/usr/bin/env python
'''
todo:
    --acr option to not rename specified acronyms
    support for subtitle files in the same dir before cleaning up
    work with single file args too not just dirs
    detect series = more than 3 movie files in a dir
    fetch date if missing
    detect duplicate files with date and no date
    detect multicd files that have been concatenated
    limit option for easier review
    skip option for easier review
'''

import os
import re
import argparse

nameformat_re_str = r'([A-Z0-9][\w,\-\']*)(( -)|( [A-Z0-9][\w,\-\']*))*( \{\d\d\d\d\})?( CD\d)?$'
year_re = re.compile(r'\b\d{4}\b')
year_re = re.compile(r'\d{4}\b')
remove_year_re = re.compile(r'\W*\d{4}\W*')
cdformat_re = re.compile(r'^cd[12]$', re.IGNORECASE)

# all lowercase!
garbages = (
    'axxo',
    'bdrip',
    'dvd.screener',
    'dvdrip',
    'dvdscr',
    'jaybob',
    'maxspeed',
    'proper',
    'readnfo',
    'xvid',
    '^sparks-',
    )

# all lowercase!
blahdirs = (
    '.unwanted',
    'sample',
    'subs',
    )

# all lowercase!
mov_extensions = ('.avi', '.mp4', '.mkv', )
sub_extensions = ('.srt', '.sub', )

unmatched = []


def sanitize(name):
    for garbage in garbages:
        name = re.sub('\W*%s.*' % garbage, '', name, flags=re.IGNORECASE)

    tmp = year_re.findall(name)
    if tmp:
        year = tmp[0]
        name = remove_year_re.sub('', name)
    else:
        year = None

    name = name.replace('_', ' ')
    name = re.sub(r'[^\w,\-\']+', ' ', name).title().replace("'S", "'s")

    if year:
        return '%s {%s}' % (name, year)
    return name


def print_rename(filepath, newname):
    print 'mv "%s" "%s"' % (filepath, newname)


def print_cleanup(dirpath):
    print 'rm -f "%s"/*' % dirpath
    print 'rmdir "%s"' % dirpath


def sanitize_path(args, path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for dirname in dirnames:
            if dirname.lower() in blahdirs:
                dirnames.remove(dirname)
                print 'rm -fr "%s/%s"' % (dirpath, dirname)
                print
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            (basename, ext) = os.path.splitext(filename)
            if ext.lower() in mov_extensions + sub_extensions:
                if ext.lower() in sub_extensions:
                    (tmp_basename, tmp_ext) = os.path.splitext(basename)
                    if tmp_ext.lower() in mov_extensions:
                        basename = tmp_basename
                oldname = basename + ext
                if nameformat_re.match(basename):
                    if not args.quiet:
                        print '# %s' % oldname
                        print
                else:
                    sanitized_by_name = sanitize(basename)
                    if not args.quiet:
                        print '# sanitized by name:', sanitized_by_name

                    dirname = os.path.basename(dirpath)
                    if cdformat_re.match(dirname):
                        cdname = dirname
                        dirname = os.path.basename(os.path.dirname(dirpath))
                    else:
                        cdname = None
                    sanitized_by_dir = sanitize(dirname)
                    if cdname:
                        sanitized_by_dir += ' ' + cdname
                    if not args.quiet:
                        print '# sanitized by dir:', sanitized_by_dir

                    if nameformat_re.match(sanitized_by_dir):
                        newname = sanitized_by_dir + ext.lower()
                        print_rename(filepath, newname)
                        if dirpath != path:
                            print_cleanup(dirpath)
                    elif nameformat_re.match(sanitized_by_name):
                        newname = sanitized_by_name + ext.lower()
                        print_rename(filepath, newname)
                        if dirpath != path:
                            print_cleanup(dirpath)
                    else:
                        print '# ERROR: could not sanitize "%s"' % filepath
                        print '# -> "%s" ?' % sanitized_by_name
                        print '# -> "%s" ?' % sanitized_by_dir
                    print
            else:
                unmatched.append(filepath)

parser = argparse.ArgumentParser(description='Normalize movie filenames')
parser.add_argument('paths', nargs='+')
parser.add_argument('--quiet', '-q', action='store_true')
parser.add_argument('--ignorecase', '-i', action='store_true')

args = parser.parse_args()

if args.ignorecase:
    nameformat_re_flags = re.IGNORECASE
else:
    nameformat_re_flags = 0
nameformat_re = re.compile(nameformat_re_str, nameformat_re_flags)

for path in args.paths:
    sanitize_path(args, path)

for path in unmatched:
    print '# unmatched:', path

# eof
