import unittest
import os

from flask_testing import TestCase

from packtools.webapp import app


class TestWebAppTests(TestCase):


    def create_app(self):
        return app.create_app("packtools.webapp.config.default.TestingConfig")

    def test_packtools_stylechecker(self):

        response = self.client.get("/stylechecker")
        self.assertIn("SciELO Style Checker",response.data.decode("utf-8"))

    def test_packtools_preview_html(self):

        response = self.client.get("/previews")
        self.assertIn("SciELO HTML Previewer",response.data.decode("utf-8"))


