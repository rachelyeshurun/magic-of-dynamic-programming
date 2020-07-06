import ipywidgets as widgets

from IPython.display import display
from ipywidgets import Button, Layout, Label

import json
import sys

def create_multi_answer_widget(options):

    options_dict = {option['id']: widgets.Checkbox(description=option['answer'], value=False, layout=Layout(width='1000px'), style={'description_width': 'initial'}) for option in options}
    checkboxes = list(options_dict.values())

    # for each option, create a feedback box on the left and a checkbox on the right
    vertical = []
    for cb in checkboxes:
        new_hbox = widgets.HBox([widgets.Label(value=''), cb])
        vertical.append(new_hbox)

    # vertically laid out options with feedback on the left
    option_widget = widgets.VBox(vertical)
    option_widget.box_style = 'info'

    # submit button with (empty) score label on the left
    submit_button = Button(description='Submit')
    submit_button.style.button_color = 'lightblue'
    score = Label(value='')
    score_widget = widgets.HBox([score, submit_button])
    score_widget.box_style = 'info'

    # stack options and score area to make the final widget
    multi_answer = widgets.VBox([option_widget, score_widget])
    multi_answer.box_style = 'info'

    # question text will be in markdown before the quiz (for now) - easily allows interesting questions with code, formulas etc.
    # compare checkbox value with original

    def check_answers(b):

        #run through each option, compare expected answer (checked/unchecked) with actual student answer
        num_options = len(options)
        lost_points = 0

        option_widget = multi_answer.children[0]
        score_widget = multi_answer.children[1]

        # Remove the submit button
        score_widget.children[1].layout.display = 'none'

        score_label = score_widget.children[0]
        score_label.layout = Layout(width='100px')

        for i in range(num_options):

            opt = option_widget.children[i]


            lbl = opt.children[0]
            cb = opt.children[1]

            actual_answer = cb.value
            expected_answer = options[i]['correct']

            # clear feedback before giving new feedback
            #opt.box_style = 'info'
            lbl.value = ''
            lbl.layout=Layout(width='100px')
            cb.disabled = True

            # feedback logic copied from Canvas quizzes
            # red border + 'incorrect' for incorrectly checked
            # green border + 'correct!' for correctly checked
            # grey border + text 'correct answer' for incorrectly unchecked
            # nothing for correctly unchecked - try to even disable
            if (expected_answer and actual_answer):
                #opt.box_style = 'success'
                opt.layout = Layout(border='2px solid green')
                lbl.value = 'Correct!'
            if (expected_answer and not actual_answer):
                #opt.box_style = 'warning'
                lbl.value = 'Correct answer'
                opt.layout = Layout(border='3px solid gray')
                lost_points += 1
            if (not expected_answer and actual_answer):
                #opt.box_style = 'danger'
                lbl.value = 'Incorrect'
                opt.layout = Layout(border='2px solid red')
                lost_points += 1

        # update the score label
        text = 'Score:  ' + str(num_options - lost_points) + '/' + str(num_options) + ' pts'
        if lost_points == 0:
            score_label.value = text + ' ;-)'
            #$\ddot\smile$'
            option_widget.box_style = 'success'
            score_widget.box_style = 'success'
            multi_answer.box_style = 'success'
        else:
            option_widget.box_style = 'danger'
            score_widget.box_style = 'danger'
            multi_answer.box_style = 'danger'
            score_label.value = text

    submit_button.on_click(check_answers)
    return(multi_answer)


def main(argv):
    json_file = sys.argv[1]
    with open(json_file) as f:
        quiz_dict = json.load(f)

    # assuming for now, just one type of quiz: multi-answer multiple choice
    w = create_multi_answer_widget(quiz_dict['options'])
    display(w)


# main function takes json file as input. acc. to type creates the widget and displays it
if __name__ == "__main__":
    main(sys.argv[1:])














