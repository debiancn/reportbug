#
# rbtempfile module - Temporary file handling for reportbug
#   Written by Chris Lawrence <lawrencc@debian.org>
#   (C) 1999-2003 Chris Lawrence
#
# This program is freely distributable per the following license:
#
##  Permission to use, copy, modify, and distribute this software and its
##  documentation for any purpose and without fee is hereby granted,
##  provided that the above copyright notice appears in all copies and that
##  both that copyright notice and this permission notice appear in
##  supporting documentation.
##
##  I DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING ALL
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL I
##  BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
##  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
##  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
##  SOFTWARE.
#
# Version ##VERSION##; see changelog for revision history
#
# $Id: rbtempfile.py,v 1.1.1.1 2004-02-05 04:29:08 lawrencc Exp $

import os
import tempfile

template = 'reportbug-%d-' % os.getpid()

# Derived version of mkstemp that returns a Python file object
_text_openflags = os.O_RDWR | os.O_CREAT | os.O_EXCL
if hasattr(os, 'O_NOINHERIT'):
    _text_openflags |= os.O_NOINHERIT
if hasattr(os, 'O_NOFOLLOW'):
    _text_openflags |= os.O_NOFOLLOW

_bin_openflags = _text_openflags
if hasattr(os, 'O_BINARY'):
    _bin_openflags |= os.O_BINARY

# Safe open, prevents filename races in shared tmp dirs
# Based on python-1.5.2/Lib/tempfile.py
def open_write_safe(filename, mode='w+b', bufsize=-1):
    if 'b' in mode:
        fd = os.open(filename, _bin_openflags, 0600)
    else:
        fd = os.open(filename, _text_openflags, 0600)

    try:
        return os.fdopen(fd, mode, bufsize)
    except:
        os.close(fd)
        raise

# Wrapper for mkstemp; main difference is that text defaults to True, and it
# returns a Python file object instead of an os-level file descriptor
def TempFile(suffix="", prefix=template, dir=None, text=True,
             mode="w+", bufsize=-1):
    fh, filename = tempfile.mkstemp(suffix, prefix, dir, text)
    fd = os.fdopen(fh, mode, bufsize)
    return (fd, filename)
