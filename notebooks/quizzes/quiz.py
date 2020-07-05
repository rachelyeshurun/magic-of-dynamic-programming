import ipywidgets as widgets

from IPython.display import clear_output
from IPython.display import display
from ipywidgets import Button, Layout

import json

import sys, getopt

def main(argv):
    json_file = sys.argv[1]
    with open(json_file) as f:
        quiz_dict = json.load(f)

    options_for_display = [option['answer'] for option in quiz_dict['options']]
    options_dict = {option['id']: widgets.Checkbox(description=option['answer'], value=False, style={'description_width': 'initial'}) for option in quiz_dict['options']}
    #print(options_dict)
    checkboxes = list(options_dict.values())

    # for each option, create a feedback box on the left and a checkbox on the right
    vertical = []
    for cb in checkboxes:
        new_hbox = widgets.HBox([widgets.Label(value='', layout=Layout(width='100px', border='1px dotted blue')), cb] )
        vertical.append(new_hbox)

        #options_widget.children = tuple(list(options_widget.children) + list(new_hbox))

    submit_button = Button(description='Submit', layout=Layout(color='lightblue'))
    vertical.append(submit_button)
    submit_button.style.button_color = 'lightblue'
    options_widget = widgets.VBox(vertical)
    options_widget.box_style = 'info'
    display(options_widget)

    #print(options_widget.children[1])

    # question text will be in markdown before the quiz (for now) - easily allows interesting questions with code, formulas etc.

    #Add Submit button


    #display(submit_button)

    # compare checkbox value with original

    # red border + 'incorrect' for incorrectly checked
    # green border + 'correct!' for correctly checked
    # grey border + text 'correct answer' for incorrectly unchecked
    # nothing for correctly unchecked - try to even disable

    def check_answers():

        #run through each option
        return

    submit_button.on_click(check_answers)

# main function takes json file as input. acc. to type creates the widget and displays it
if __name__ == "__main__":
    main(sys.argv[1:])














