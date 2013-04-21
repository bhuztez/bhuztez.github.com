#!/usr/bin/env python2

from __future__ import unicode_literals

import sys
import time

import itertools


from strawman.generators.composite import composite_generator, depends_on
from strawman.generators.storage import storage_generator
from strawman.generators.annotate import annotate
from strawman.generators.aggregate import aggregator
from strawman.generators.filter import filter_by
from strawman.generators.order import order_by

from strawman.storages.fs import FileSystemStorage

from strawman.markups.markdown import Markdown

from strawman.writers.fs import file_system_writer
from strawman.writers.dulwich import dulwich_writer

from strawman.flavours.jekyll import *
from strawman.flavours.strawman import *
from strawman.contrib.github_pages import nojekyll


site = {
    "domain": "bhuztez.github.io",
    "me": "https://github.com/bhuztez",
    "time": time,
}



from jinja2 import Environment, FileSystemLoader

env = Environment(
    autoescape = True,
    loader = FileSystemLoader('layouts'))


def render_page(metadata):
    t = env.get_template(metadata['layout']+'.html')

    ctx = {
        "site": site,
        "page": metadata,
        "ROOT_URL": get_root_path(metadata.path),
        "content": metadata.content}

    return t.render(ctx)


def render_archive(metadata):
    t = env.get_template(metadata['layout']+'.html')

    ctx = {
        "site": site,
        "page": metadata,
        "ROOT_URL": get_root_path(metadata.path),
        "posts": metadata.posts}

    return t.render(ctx)


def get_parser(metadata):
    p = Markdown()
    p.converter.registerExtensions(['codehilite(css_class=highlight)', 'extra'], {})
    p.converter.reset()
    return p



def main_generator():

    @annotate(
        annotate_attribute(path=lambda m: m.source_filename))
    @apply
    def static():
        return storage_generator(
            FileSystemStorage('.'),
            exclude(glob("*~")),
            include(glob('/404.html')),
            include(glob('/robots.txt')),
            include_directory(
                '/css',
                include(glob("*"))))


    @annotate(
        parse_markup(get_parser),
        apply_template(render_page),
        encode())
    @filter_by(published)
    @annotate(
        decode(),
        post_filename_metadata,
        yaml_front_matter,
        permalink("/$year/$month/$title.html"),
        annotate_attribute(id=lambda m: m.path[:-5]))
    @apply
    def posts():
        return storage_generator(
            FileSystemStorage('posts'),
            exclude(glob("*~")),
            include(glob("*")))

    @annotate(
        decode(),
        yaml_front_matter,
        parse_markup(get_parser),
        annotate_attribute(
            path = lambda m: m.source_filename[:-9]+'.html',
            id = lambda m: m.source_filename[:-9]),
        apply_template(render_page),
        encode())
    @apply
    def pages():
        return storage_generator(
            FileSystemStorage('pages'),
            include(glob('/*.markdown')))


    @depends_on(posts)
    @annotate(
        annotate_metadata(
            layout=lambda m: "posts",
            title=lambda m: "POSTS"),
        annotate_attribute(path=lambda m: "/index.html"),
        apply_template(render_archive),
        encode())
    @order_by(key=lambda m:m["date"], reverse=True)
    @apply
    def archive():
        return aggregator("posts")


    return composite_generator(**locals())



if __name__ == '__main__':
    generator = main_generator()

    if sys.argv[1] == 'draft':
        def get_root_path(path):
            level = path.count('/', 1)

            if level == 0:
                return '.'

            return '/'.join(['..']*level)

        site["publish"] = False

        writer = file_system_writer('_site')

    elif sys.argv[1] == 'publish':
        generator = itertools.chain([nojekyll], generator)

        def get_root_path(path):
            return ""

        site["publish"] = True

        writer = dulwich_writer(
            '.', 'refs/heads/master',
            'bhuztez <bhuztez@gmail.com>', int(time.time()), -time.timezone,
            'bhuztez <bhuztez@gmail.com>', int(time.time()), -time.timezone,
            'utf-8', 'Initial commit')

    else:
        exit(1)

    writer(generator)
