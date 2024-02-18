# from django.test import TestCase
# from django.urls import reverse
#
# from .models import Card
#
#
# class CardTests(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.card = Card.objects.create(
#             title='Test card',
#             description='Test description',
#             price='1000.00',
#         )
#
#     def test_card_listing(self):
#         self.assertEqual(f'{self.card.title}', 'Test card')
#         self.assertEqual(f'{self.card.description}', 'Test description')
#         self.assertEqual(f'{self.card.price}', '1000.00')
#
#     def test_card_list_view(self):
#         response = self.client.get(reverse('card_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Test card')
#         self.assertTemplateUsed(response, 'cards/card_list.html')
#
#     def test_card_detail_view(self):
#         resource = self.client.get(self.card.get_absolute_url())
#         no_response = self.client.get('/cards/12345/')
#         self.assertEqual(resource.status_code, 200)
#         self.assertEqual(no_response.status_code, 404)
#         self.assertContains(response, 'Test card')
#         self.assertTemplateUsed(response, 'cards/card_detail.html')
