import ipywidgets as widgets

from IPython.display import display
from ipywidgets import Button, Layout, Label, AppLayout

import json
import sys
import random


def create_multi_answer_widget(question, options):

    question_widget = Label(value=question)
    options_dict = {option['id']: widgets.Checkbox(description=option['answer'], value=False, layout=Layout(width='1000px'), style={'description_width': 'initial'}) for option in options}
    checkboxes = list(options_dict.values())

    # for each option, create a feedback box on the left and a checkbox on the right
    vertical = []
    for cb in checkboxes:
        new_hbox = widgets.HBox([Label(value=''), cb])
        vertical.append(new_hbox)

    # vertically laid out options with feedback on the left
    option_widget = widgets.VBox(vertical)
    #option_widget.box_style = 'info'

    # submit button with (empty) score label on the left
    submit_button = Button(description='Submit')
    submit_button.style.button_color = 'lightblue'
    score = Label(value = '', layout = Layout(width='500px'))
    score_widget = widgets.HBox([submit_button, score])
    score_widget.box_style = 'info'

    # stack options and score area to make the final widget

    multi_answer = AppLayout(header=question_widget,
              left_sidebar=option_widget,
              center=None,
              right_sidebar=None,
              footer=score_widget)



    #multi_answer = widgets.VBox([option_widget, score_widget])
    multi_answer.box_style = 'info'

    # compare checkbox value with original
    def check_answers(b):

        #run through each option, compare expected answer (checked/unchecked) with actual student answer
        num_options = len(options)
        incorrect = 0
        missing = 0

        global first_try_flag
        option_widget = multi_answer.children[2]
        score_widget = multi_answer.children[1]

        submit_button = score_widget.children[0]
        score_label = score_widget.children[1]

        for i in range(num_options):

            opt = option_widget.children[i]

            lbl = opt.children[0]
            cb = opt.children[1]

            actual_answer = cb.value
            expected_answer = options[i]['correct']

            # clear feedback before giving new feedback
            opt.layout = Layout(border=None)
            cb.disabled = True
            lbl.value = ''
            lbl.layout=Layout(width='100px')


            # feedback logic copied from Canvas quizzes
            # red border + 'incorrect' for incorrectly checked
            # green border + 'correct!' for correctly checked
            # NOT DOING THIS: grey border + text 'correct answer' for incorrectly unchecked
            # nothing for correctly unchecked - try to even disable
            if (expected_answer and actual_answer):
                #opt.box_style = 'success'
                opt.layout = Layout(border='2px solid green')
                lbl.value = 'Correct!'
            if (expected_answer and not actual_answer):
                #opt.box_style = 'warning'
                #lbl.value = 'Correct answer'
                #opt.layout = Layout(border='3px solid gray')
                missing += 1
            if (not expected_answer and actual_answer):
                #opt.box_style = 'danger'
                lbl.value = 'Incorrect'
                opt.layout = Layout(border='2px solid red')
                incorrect += 1

        # update the score label
        if incorrect + missing == 0:
            option_widget.box_style = 'success'
            score_widget.box_style = 'success'
            multi_answer.box_style = 'success'
            submit_button.disabled = True
            submit_button.style.button_color = 'lightgreen'
            cb.disabled = True

            if submit_button.description == 'Submit':
                text = random.choice(['Perfect!', 'Your\'re on a roll!', 'Keep up the good work!', 'All correct!', 'Correct!',
                                  'Success!', '100% !!', 'Perfect ;-) ', 'Excellent!', 'You got it!', 'You\'re the best',
                                             'You got an A+', 'Nice job, rock star!', 'Hurray for you!', 'Great work!'])
            else:
                text = 'Very good'
        else:
            option_widget.box_style = 'danger'
            score_widget.box_style = 'danger'
            multi_answer.box_style = 'danger'
            submit_button.style.button_color = 'pink'

            submit_button.description = 'Submit again'
            for i in range(num_options):
                opt = option_widget.children[i]
                cb = opt.children[1]
                cb.disabled = False
            # clear rectangles
            if missing > 0:
                text = 'you missed some correct options, try again!'
            else:
                text = 'try again!'

        score_label.value = '~ ~ ~ ~ ~' + text + '~ ~ ~ ~ ~'

    submit_button.on_click(check_answers)

    return(multi_answer)


def main(argv):
    json_file = sys.argv[1]
    with open(json_file) as f:
        quiz_dict = json.load(f)

    # assuming for now, just one type of quiz: multi-answer multiple choice
    w = create_multi_answer_widget(quiz_dict['question'], quiz_dict['options'])
    display(w)


# main function takes json file as input. acc. to type creates the widget and displays it
if __name__ == "__main__":
    main(sys.argv[1:])














