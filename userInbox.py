import mysql.connector
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDIconButton

# Kivy Builder String for the custom content layout
KV = '''

<TwoPartLabel@BoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    padding: 1

    MDLabel:
        id: label_prefix
        font_name: "BPoppins"
        halign: "left"  
        size_hint_y: None
        text: ""
        font_size: "15sp"

    MDLabel:
        id: label_dynamic
        font_name: "MPoppins"
        halign: "center"  
        size_hint_y: None
        text: ""
        font_size: "14sp"
        

<Separator@MDSeparator>:
    height: "1dp"

<Button@MDRaisedButton>:
    size_hint: 0.66, 0.065
    background_color: 0, 0, 0, 0
    font_name: "BPoppins"
    canvas.before:
        Color:
            rgba: 52/255, 0, 231/255, 255/255
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [5] 

<DialogContent>:
    orientation: "vertical"
    size_hint_y: None
    height: "400dp"

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height  # Adjust the height to fit the content
        
        MDLabel:
            text: "Report History"
            font_name: "BPoppins"
            font_size: "22sp"
            size_hint_y: None
            height: self.texture_size[1]

    ScrollView:
        size_hint_y: None
        height: 500  # Adjust based on your dialog box size

        GridLayout:
            cols: 1
            size_hint_y: None
            size_hint_x: 1  # Take full width of the ScrollView
            height: self.minimum_height
            spacing: "15dp"
            padding: [0, 20, 30, 30]  # Padding: [left, top, right, bottom]
            pos_hint: {'center_x': 0.5, 'top': 1}  # Adjust pos_hint as needed

            Separator:

            TwoPartLabel:
                id: username
                
            Separator:

            TwoPartLabel:
                id: title

            Separator:
                
            TwoPartLabel:
                id: checklist

            Separator:
            
            TwoPartLabel:
                id: image_path
            
            Separator:
                
            TwoPartLabel:
                id: details

            Separator:
                
            TwoPartLabel:
                id: urgency

            Separator:
            
            TwoPartLabel:
                id: status

            Separator:
            
            TwoPartLabel:
                id: dateCreated

            Separator:

            GridLayout:
                cols: 2
                spacing: "10sp"
                padding: [0, 10, 0, 0]
                size_hint_y: None
                height: "48dp"  # Fixed height for the button area

    
'''

class CustomTwoLineListItem(TwoLineListItem):
    def __init__(self, primary_font_name="BPoppins", secondary_font_name="MPoppins", primary_font_size=20, secondary_font_size=16, primary_color=[0, 0, 0, 1], secondary_color=[0, 0, 0, 1], **kwargs):
        super().__init__(**kwargs)
        # Override primary label properties
        self.ids._lbl_primary.font_name = primary_font_name
        self.ids._lbl_primary.font_size = primary_font_size 
        self.ids._lbl_primary.color = primary_color

        # Override secondary label properties
        self.ids._lbl_secondary.font_name = secondary_font_name
        self.ids._lbl_secondary.font_size = secondary_font_size
        self.ids._lbl_secondary.color = secondary_color

# Custom content class for the dialog
class DialogContent(BoxLayout):
    pass

host = "sql12.freesqldatabase.com"
user = "sql12662532"
password = "viDRIhzYSq"
database = "sql12662532"

db = mysql.connector.connect(
    host = "sql12.freesqldatabase.com",
    user = "sql12662532",
    password = "viDRIhzYSq",
    database = "sql12662532",
    )

cursor = db.cursor()

Window.size = (360, 600)

class UserInbox(Screen):
    user_id = None  # Add a user_id attribute comg from main.py
    
    dropdown = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

        # Layout for Back Button and ScrollView
        layout = BoxLayout(orientation='vertical')

        # Back Button
        back_button = MDIconButton(
            icon="arrow-left",
            font_size="30sp",
            theme_text_color="Custom",
            text_color=(26/255, 24/255, 58/255, 255/255),
            on_release=self.go_back,
        )
        
        # Add Back Button to Layout
        layout.add_widget(back_button)
        # ScrollView and List View for Reports
        scroll = ScrollView()
        self.list_view = MDList()
        self.list_view.clear_widgets()
        scroll.add_widget(self.list_view)
        layout.add_widget(scroll)
        
        self.add_widget(layout)  # Add the layout to the screen

    def go_back(self, instance):
        # Switch to home screen
        self.manager.current = 'homescreen'
    
    def on_enter(self, *args):
        super(UserInbox, self).on_enter(*args)
        self.refresh_list()


    def refresh_list(self):
        self.list_view.clear_widgets()  # Clear the current list
        self.populate_list()  # Repopulate the list with fresh data

    def populate_list(self):
        # Clear the existing list items before repopulating
        self.list_view.clear_widgets()

        # SQL query to select only reports with status not equal to 'resolved' or 'False Report'
        query = "SELECT ReportId, Title FROM report WHERE ProfileID = %s"
        cursor.execute(query, (self.user_id,))
        rows = cursor.fetchall()

        red_color = [1, 0, 0, 1]  # Red color in RGBA
        black_color = [0, 0, 0, 1]  # Black color in RGBA

        for row in rows:
            color = red_color if row[1] == 'SOS' else black_color

            item = CustomTwoLineListItem(
                text='Report ID: ' + str(row[0]),
                secondary_text='Title: ' + row[1],
                primary_color=color,
                on_release=lambda x, row=row: self.open_dialog(row)
            )
            self.list_view.add_widget(item)

    # Method to update the text for TwoPartLabel
    def set_two_part_label_text(self, label_id, prefix, data_text):
        setattr(self.dialog_content.ids[label_id].ids.label_prefix, 'text', prefix)
        setattr(self.dialog_content.ids[label_id].ids.label_dynamic, 'text', str(data_text))


    def open_dialog(self, row):
        self.selected_report_id = row[0]  # Store the selected ReportId

        # Fetch data for the selected report
        cursor.execute("SELECT Title, Checklist, image_Path, Details, Urgency, Status, ProfileID, dateCreated FROM report WHERE ReportId = %s", (self.selected_report_id,))
        data = cursor.fetchone()

        # Create dialog content
        self.dialog_content = DialogContent()

        if data:
            # Update label texts
            self.set_two_part_label_text('title', "Title:", data[0])
            self.set_two_part_label_text('checklist', "Checklist:", data[1])
            self.set_two_part_label_text('image_path', "Image Path:", data[2])
            self.set_two_part_label_text('details', "Details:", data[3])
            self.set_two_part_label_text('urgency', "Urgency:", data[4])
            self.set_two_part_label_text('status', "Status:", data[5])
            self.set_two_part_label_text('dateCreated', "Report Date :", data[7])


            # Fetch username for the selected report
            self.selected_profile_id = data[6]
            cursor.execute("SELECT Username FROM UserProfiles WHERE ProfileID = %s", (self.selected_profile_id,))
            data2 = cursor.fetchone()

            if data2:
                self.set_two_part_label_text('username', "Reported by:", str(data2[0]))
            else:
                self.set_two_part_label_text('username', "Reported by:", "Unknown")

        self.dialog = MDDialog(type="custom",
                            content_cls=self.dialog_content,
                            size_hint=(0.8, None),
                            buttons=[
                                MDRaisedButton(
                                    text="Close",
                                    font_name="BPoppins",
                                    font_size="14sp",
                                    theme_text_color="Custom",
                                    text_color=(1, 1, 1, 1),
                                    md_bg_color=(76/255, 175/255, 80/255, 1),
                                    on_release=self.dismiss_dialog
                                )
                            ])
        self.dialog.open()
        

    def menu_callback(self):
        self.dropdown.open()

    # For Cancel Button
    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

