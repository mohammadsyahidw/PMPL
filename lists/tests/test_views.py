from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  #1
        response = home_page(request)  #2
        
        items = Item.objects.all()
        counter = items.count()
        status = "oh tidak"
        if counter == 0:
           status = "yey, waktunya berlibur"
        elif counter < 5:
           status = "sibuk tapi santai"
        else:
           status = "oh tidak"

        expected_html = render_to_string('home.html',{'status': status})
        self.assertEqual(response.content.decode(), expected_html)
        #self.assertTrue(response.content.startswith(b'<html>'))  #3
        #self.assertIn(b'<title>To-Do lists</title>', response.content)  #4
        #self.assertTrue(response.content.strip().endswith(b'</html>'))  #5
    
    def test_home_page_empty(self):
        list_ = List.objects.create()
        request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIn('yey, waktunya berlibur', response.content.decode())
    
    def test_home_page_less_than_five(self):
        list_ = List.objects.create()
        #Item.objects.create(text='1 : entri 1')
        Item.objects.create(text='1', list=list_)
        request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIn('sibuk tapi santai', response.content.decode())
    
    def test_home_page__greater_than_four(self):
        list_ = List.objects.create()
        Item.objects.create(text='1 : entri 1', list=list_)
        Item.objects.create(text='2 : entri 2', list=list_)
        Item.objects.create(text='3 : entri 3', list=list_)
        Item.objects.create(text='4 : entri 4', list=list_)
        Item.objects.create(text='5 : entri 5', list=list_)
        request = HttpRequest()
        #response = home_page(request)
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIn('oh tidak', response.content.decode())
    """
    """
    """
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
   
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
    
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    """


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))