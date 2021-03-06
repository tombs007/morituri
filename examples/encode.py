# -*- Mode: Python; test-case-name: morituri.test.test_header -*-
# vi:si:et:sw=4:sts=4:ts=4

# Morituri - for those about to RIP

# Copyright (C) 2009 Thomas Vander Stichele

# This file is part of morituri.
# 
# morituri is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# morituri is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with morituri.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import optparse
import tempfile
import pickle
import shutil

import gobject
gobject.threads_init()

import gst

import gtk


from morituri.common import task, taskgtk, common, encode

def gtkmain(runner, taskk):
    runner.connect('stop', lambda _: gtk.main_quit())

    window = gtk.Window()
    window.add(runner)
    window.show_all()

    runner.run(taskk)

    gtk.main()

def climain(runner, taskk):
    runner.run(taskk)

class Listener(object):
    def __init__(self, persister):
        self._persister = persister

    def progressed(self, task, value):
        pass

    def described(self, task, description):
        pass

    def started(self, task):
        pass

    def stopped(self, task):
        self._persister.object[task.path] = task.trm
        print task.path, task.trm
        self._persister.persist()


def main(argv):
    parser = optparse.OptionParser()

    default = 'cli'
    parser.add_option('-r', '--runner',
        action="store", dest="runner",
        help="runner ('cli' or 'gtk', defaults to %s)" % default,
        default=default)

    options, args = parser.parse_args(argv[1:])

    taglist = gst.TagList()
    taglist[gst.TAG_ARTIST] = 'Thomas'
    taglist[gst.TAG_TITLE] = 'Yes'
    taskk = encode.EncodeTask(args[0], args[1], taglist=taglist)

    if options.runner == 'cli':
        runner = task.SyncRunner()
        function = climain
    elif options.runner == 'gtk':
        runner = taskgtk.GtkProgressRunner()
        function = gtkmain

    function(runner, taskk)

main(sys.argv)
