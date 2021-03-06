#!/bin/sh
#
# SCRIPT: save-flash-mac.sh
# AUTHOR: Janos Gyerik <info@janosgyerik.com>
# DATE:   2011-08-24
# REV:    1.0.D (Valid are A, B, D, T and P)
#               (For Alpha, Beta, Dev, Test and Production)
#
# PLATFORM: Mac only
#
# PURPOSE: Locate and copy a flash movie (youtube.com, etc) cached by browsers.
#
# set -n   # Uncomment to check your syntax, without execution.
#          # NOTE: Do not forget to put the comment back in or
#          #       the shell script will not execute!
# set -x   # Uncomment to debug this shell script (Korn shell only)
#

usage() {
    test $# = 0 || echo $@
    echo "Usage: $0 [OPTION]... [ARG]..."
    echo
    echo 'Copy a flash movie (youtube.com, etc) saved by a browser in /private'
    echo
    echo Options:
    echo "  -n, --number NUMBER default = $number"
    echo
    echo "  -h, --help         Print this help"
    echo
    exit 1
}

args=
#arg=
#flag=off
#param=
number=
while [ $# != 0 ]; do
    case $1 in
    -h|--help) usage ;;
#    -f|--flag) flag=on ;;
#    --no-flag) flag=off ;;
#    -p|--param) shift; param=$1 ;;
    -n|--number) shift; number=$1 ;;
#    --) shift; while [ $# != 0 ]; do args="$args \"$1\""; shift; done; break ;;
    -) usage "Unknown option: $1" ;;
    -?*) usage "Unknown option: $1" ;;
    *) args="$args \"$1\"" ;;  # script that takes multiple arguments
#    *) test "$arg" && usage || arg=$1 ;;  # strict with excess arguments
#    *) arg=$1 ;;  # forgiving with excess arguments
    esac
    shift
done

eval "set -- $args"  # save arguments in $@. Use "$@" in for loops, not $@ 

#test $# -gt 0 || usage

searchdir='/private/var/folders'

if test "$number"; then
    file=$(find "$searchdir" 2>/dev/null | grep -i flash | sed -ne "$number p")
else
    file=$(find "$searchdir" 2>/dev/null | grep -i flash | head -n 1)
fi

if test -f "$file"; then
    test "$1" && cp "$file" "$1" && echo "cp $file $1" || echo $file
fi

# eof
