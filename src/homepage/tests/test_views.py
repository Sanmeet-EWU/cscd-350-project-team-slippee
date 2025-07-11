from django.test import TestCase, Client
from django.urls import reverse
import pytest


@pytest.mark.skip(reason="Don't want pytest trying to run this class")
class ViewsTestCase(TestCase):
   
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_guide_body_view(self):
        response = self.client.get(reverse('guide_body'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/guide_body.html')

    def test_index_body_view(self):
        response = self.client.get(reverse('index_body'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/index_body.html')

    def test_test_page_view(self):
        response = self.client.get(reverse('test_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/test_page.html')

    # This test needs to be changed to handle the new file upload and download method
    # def test_translate_view(self):
    #     response = self.client.post(reverse('translate'), {
    #         'from': 'bizhawk',
    #         'to': 'ares',
    #         'file-input': 'test_file.txt'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, '<p>(\'emu1\', \'emu2\', \'test_file.txt\')</p>')
