from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.floatlayout import *
from kivy.uix.boxlayout import *
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.text import *
from kivy.core.text.markup import *
from kivy.properties import *
from kivy.uix.popup import Popup
import os

class notepadApp(App):

    def __init__(self):
        App.__init__(self)
        
    def build(self):
        return MainWindow()

class OpenDialog(FloatLayout):

    open_file = ObjectProperty(None)
    cancel  = ObjectProperty(None)

class SaveDialog(FloatLayout):

    save_file = ObjectProperty(None)
    cancel  = ObjectProperty(None)

class MainWindow(BoxLayout):

    open_button = ObjectProperty()
    save_button = ObjectProperty()
    save_as_button = ObjectProperty()
    cut_button = ObjectProperty()
    copy_button = ObjectProperty()
    paste_button = ObjectProperty()
    delete_button = ObjectProperty()
    text_view = ObjectProperty()
    
    def __init__(self, **kwargs):

        super(MainWindow, self).__init__()
        self.clipboard_text = ""
        self.filepath = ""
        
    def on_open(self, *args):

        content = OpenDialog(open_file = self.open_file,
                             cancel = self.cancel_dialog)
        self._popup = Popup(title="Open File",content=content,
                            size_hint=(0.9,0.9))
        self._popup.open()

    def open_file(self,path,filename):
        
        self.filepath = filename[0]
        f = open(self.filepath,'r')
        s = f.read()
        self.text_view.text = s
        f.close()
        self.cancel_dialog()
        
    def cancel_dialog(self):
        self._popup.dismiss()
        
    def on_save(self, *args):

        if self.filepath == "":
            self.on_save_as()
        else:
            f = open(self.filepath,'w')
            f.write(self.text_view.text)
            f.close()
            
    def on_save_as(self, *args):

        content = SaveDialog(save_file = self.save_as_file,
                             cancel = self.cancel_dialog)
        self._popup = Popup(title="Save As File",content=content,
                            size_hint=(0.9,0.9))
        self._popup.open()

    def save_as_file(self, path,filename):

        self.filepath = os.path.join(path,filename)
        f = open(self.filepath,'w')
        f.write(self.text_view.text)
        f.close()        
        self.cancel_dialog()
        
    def on_copy(self, *args):

        if self.text_view.selection_text == "":
            return

        self.clipboard_text = self.text_view.selection_text

    def on_cut(self, *args):

        self.on_copy()
        self.on_delete()

    def on_paste(self, *args):

        self.text_view.insert_text(self.clipboard_text)

    def on_delete(self, *args):

        self.text_view.delete_selection()
    
if __name__ == '__main__':
    
    notepadApp().run()
