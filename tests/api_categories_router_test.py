import unittest
from unittest.mock import patch
from routers.api.categories import (
    view_categories, view_category, view_category_topics,
    create_category, update_privacy, lock_category
)
from common.responses import NotFound, NoContent, Created, Unauthorized

class CategoryRouterShould(unittest.TestCase):

    def test_view_categories():
        pass
    def test_view_category_returns_category_if_member():
        pass

    def test_view_category_unauthorized_if_not_member():
        pass

    def test_view_category_topics_returns_list():
        pass

    def test_create_category_success():
        pass

    def test_update_privacy_success():
        pass

    def test_lock_category_success():
        pass
