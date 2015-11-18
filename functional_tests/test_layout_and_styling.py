from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):      
    def untest_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
             inputbox.location['x'] + inputbox.size['width'] / 2,
             512,delta=5
        )

        #check background color
        bodytag = self.browser.find_element_by_id('body')
        #print(bodytag.value_of_css_property('background-color'))
        self.assertEqual(
                bodytag.value_of_css_property('background-color'),
                'rgba(255, 255, 255, 1)'
        )
