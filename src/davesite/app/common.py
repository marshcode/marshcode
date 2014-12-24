__author__ = 'david'

from davesite.templates.widgets import HeaderLink
from flask import request, current_app

import logging
logger = logging.getLogger()

def inject_header_link(blueprint):

    def inner():

        headerLinkMap = current_app.config.get('HEADER_LINKS')

        headerLink = None
        if(headerLinkMap and blueprint.name in headerLinkMap):
            headerLink = headerLinkMap[blueprint.name]

        return dict(headerLink=headerLink)

    blueprint.context_processor(inner)