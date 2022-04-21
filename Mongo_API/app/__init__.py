"""This is init module."""

from sanic import Sanic

# Place where app is defined
app = Sanic(__name__)

from app import usersData
