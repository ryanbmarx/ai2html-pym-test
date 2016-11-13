# -*- coding: utf-8 -*-
import os
import locale

from clint.textui import colored
import ftfy
import markdown
import shutil
from tarbell.hooks import register_hook
from tarbell.utils import puts

import p2p

from tribune_viztools.tarbell.blueprint import TribuneTarbellBlueprint
from tribune_viztools.tarbell.hooks import (
    copy_front_end_build_script_templates,
    create_front_end_files,
    create_readme,
    create_unfuddle_project,
    newproject_add_excludes,
    merge_extra_context,
    newproject_share_spreadsheet,
)

NAME = "Chicago Tribune DataViz: P2P"
P2P_DATA_KICKER_ID = 3681

blueprint = TribuneTarbellBlueprint('blueprint', __name__)

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except locale.Error:
    puts(colored.red("Locale error"))


NEWPROJECT_HOOKS = (
    copy_front_end_build_script_templates,
    create_front_end_files,
    create_readme,
    create_unfuddle_project,
    newproject_add_excludes,
    newproject_share_spreadsheet
)

GENERATE_HOOKS = (
    merge_extra_context,
)

PUBLISH_HOOKS = [
]

for f in NEWPROJECT_HOOKS:
    register_hook('newproject')(f)

for f in GENERATE_HOOKS:
    register_hook('generate')(f)

for f in PUBLISH_HOOKS:
    register_hook('publish')(f)

# Custom hooks

@register_hook('newproject')
def copy_templates(site, git):
    """
    Copy custom templates from blueprint to new project

    This is needed because Tarbell ignores the templates that start with
    '_' when copying template files from the blueprint.

    """
    filenames = [
      "_content.html",
      "_htmlstory.html",
    ]

    for filename in filenames:
        path = os.path.join(site.path, '_blueprint', filename)
        shutil.copy2(path, site.path)

def is_production_bucket(bucket_url, buckets):
    for name, url in buckets.items():
        if url == bucket_url and name == 'production':
            return True

    return False

def p2p_publish_htmlstory(site, s3):
    if not is_production_bucket(s3.bucket, site.project.S3_BUCKETS):
        puts(colored.red(
            "\nNot publishing to production bucket. Skipping P2P publiction."))
        return

    content = _get_published_content(site, s3)
    context = site.get_context(publish=True)

    try:
        p2p_slug = context['p2p_slug']
    except KeyError:
        puts("No p2p_slug defined in the spreadsheet or DEFAULT_CONTEXT. "
             "Skipping P2P publication.")
        return

    try:
        title = context['headline']
    except KeyError:
        title = context['title']
    p2p_conn = p2p.get_connection()
    content_item = {
        'slug': p2p_slug,
        'content_item_type_code': 'htmlstory',
        'title': title,
        'body': content,
        'seotitle': context['seotitle'],
        'seodescription': context['seodescription'],
        'seo_keyphrase': context['keywords'],
        'byline': context['byline'],
        'custom_param_data': {
            'story-summary': markdown.markdown(context['story_summary']),
        },
    }

    created, response = p2p_conn.create_or_update_content_item(content_item)
    if created:
        # If we just created the item, set its state to 'working'
        p2p_conn.update_content_item({
            'slug': p2p_slug,
            'content_item_state_code': 'working',
            'kicker_id': P2P_DATA_KICKER_ID,
        })

    puts("\n" + colored.green("Published to P2P with slug {}".format(p2p_slug)))


def _get_published_content(site, s3):
    template = site.app.jinja_env.get_template('_htmlstory.html')
    context = site.get_context(publish=True)
    rendered = template.render(**context)

    if u'“' in rendered or u'”' in rendered:
        # HACK: Work around P2P API's weird handling of curly quotes where it
        # converts the first set to HTML entities and converts the rest to
        # upside down quotes
        msg = ("Removing curly quotes because it appears that the P2P API does "
               "not handle them correctly.")
        puts("\n" + colored.red(msg))
        rendered = ftfy.fix_text(rendered, uncurl_quotes=True)

    return rendered


@register_hook('publish')
def p2p_publish(site, s3):
    try:
        p2p_publish_hook = site.project.P2P_PUBLISH_HOOK
    except AttributeError:
        p2p_publish_hook = p2p_publish_htmlstory

    p2p_publish_hook(site, s3)
