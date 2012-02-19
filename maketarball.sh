#!/bin/bash

#######################################################################
# This file is part of Pyblosxom.
#
# Copyright (C) 2003-2011 by the Pyblosxom team.  See AUTHORS.
#
# Pyblosxom is distributed under the MIT license.  See the file
# LICENSE for distribution details.
#######################################################################


USAGE="Usage: $0 -h | [-dr] REVISH

Creates a tarball of the repository at rev REVISH.  This can be a branch
name, tag, or commit sha.

Options:

   -d
      Adds date to the directory name.

   -h
      Shows help and exits.

Examples:

   ./maketarball v1.5
   ./maketarball -d master
"

REVISH="none"
PREFIX="none"
NOWDATE=""

while getopts ":dhr" opt;
do
    case "$opt" in
        h)
            echo "$USAGE"
            exit 0
            ;;
        d)
            NOWDATE=`date "+%Y-%m-%d-"`
            shift $((OPTIND-1))
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            echo "$USAGE" >&2
            ;;
    esac 
done

if [[ -z "$1" ]]; then
    echo "$USAGE";
    exit 1;
fi

REVISH=$1
PREFIX="$NOWDATE$REVISH"

# convert PREFIX to all lowercase and nix the v from tag names.
PREFIX=`echo "$PREFIX" | tr '[A-Z]' '[a-z]' | sed s/v//`

# build the filename base minus the .tar.gz stuff--this is also
# the directory in the tarball.
FNBASE="pyblosxom-$PREFIX"

STARTDIR=`pwd`

function cleanup {
    pushd $STARTDIR

    if [[ -e tmp ]]
    then
        echo "+ cleaning up tmp/"
        rm -rf tmp
    fi
    popd
}

echo "+ Building tarball from: $REVISH"
echo "+ Using prefix:          $PREFIX"
echo "+ Release?:              $RELEASE"

echo ""

if [[ -e tmp ]]
then
    echo "+ there's an existing tmp/.  please remove it."
    exit 1
fi

mkdir $STARTDIR/tmp
echo "+ generating archive...."
git archive \
    --format=tar \
    --prefix=$FNBASE/ \
    $REVISH > tmp/$FNBASE.tar

if [[ $? -ne 0 ]]
then
    echo "+ git archive command failed.  See above text for reason."
    cleanup
    exit 1
fi

echo "+ compressing...."
gzip tmp/$FNBASE.tar

echo "+ archive at tmp/$FNBASE.tar.gz"

echo "+ done."
