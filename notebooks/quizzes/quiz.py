import ipywidgets as widgets

from IPython.display import display, HTML
from ipywidgets import Button, Layout, Label, AppLayout, Checkbox, HBox, VBox, Text

import json
import sys
import random

def create_question_widget(question):
    q = HBox([Label(value=question)], layout=Layout(display='flex', flex_flow='row wrap', align_items='stretch', width='100%', margin='0 0 30px 0'))
    return q

def create_score_widget(colour, submit_text = 'Submit', show_text = 'Show answer'):

    box = HBox([], layout=Layout(display='flex', flex_flow='row wrap', align_items='stretch', margin='30px 0 0 0'))

    submit_button = Button(description=submit_text)
    submit_button.style.button_color = colour
    box.children += (submit_button,)

    score = Label(value='', layout=Layout(width='50%', height='50%', margin='0 0 0 30px'))
    box.children += (score,)

    show_button = Button(description=show_text)
    show_button.style.button_color = colour
    show_button.disabled = True
    show_button.layout.display = 'none'
    box.children += (show_button,)

    return box


def generate_feedback(quiz_widget, score_widget, style = 'info', feedback_text = '', show_show_answer_btn=False):
    # On success, turn everything green, disable Submit button. If first try. show message x, else show y
    submit_btn = score_widget.children[0]
    score_label = score_widget.children[1]
    show_btn = score_widget.children[2]

    quiz_widget.box_style = style
    #clear current feedback
    score_label.value = ''
    show_btn.disabled = True

    style_colour = {'success':'lightgreen', 'danger':'pink', 'info':'lightblue', }
    submit_btn.style.button_color = style_colour[style]
    show_btn.style.button_color = style_colour[style]

    if style == 'success':
        submit_btn.disabled = True
        if feedback_text == '':
            feedback_text += random.choice(
                ['Perfect!', 'Your\'re on a roll!', 'Keep up the good work!', 'All correct!', 'Correct!', 'Correct! Looks like you\'re having fun!',
                 'Success!', '100%', 'Perfect ;-) ', 'Excellent!', 'You got it!', 'You\'re the best!', 'You\'re doing very well!',
                 'You got an A+', 'Nice job, rock star!', 'Hurray for you!', 'Great work!', 'Very, very nice!', 'Great!',
                 'Nice, you got it on your first try!', 'Nice one!', 'One hundred percent!', 'Awesome!', 'Brilliant!'])
    # On failure: turn everything red/pink, change Submit to submit again, show try again text, show Show Answer button
    elif style == 'danger':
        submit_btn.description = 'Submit again'
        submit_btn.disabled = False
        if feedback_text == '':
            feedback_text += 'Try again!'
        if show_show_answer_btn == True:
            show_btn.layout.display = 'flex'
            show_btn.disabled = False
    elif style == 'info':
        submit_btn.disabled = True

    score_label.value = feedback_text

def create_multi_answer_widget(question, options):

    question_widget = create_question_widget(question)

    # Need to make my own checkbox out of checkbox + label because LaTeX not displaying nicely in checkbox built in description label
    labels = [Label(value = option['answer'], layout=Layout(width='1000px')) for option in options]
    checkboxes = [HBox((Checkbox(value=False, style={'description_width': 'initial'}, layout=Layout(width='30px')), lbl)) for lbl in labels]

    # for each option, create a feedback box on the left and a checkbox on the right
    vertical = []
    for cb in checkboxes:
        new_hbox = widgets.HBox([Label(value=''), cb])
        #new_hbox.box_style = 'info'
        vertical.append(new_hbox)

    # vertically laid out options with feedback on the left
    option_widget = widgets.VBox(vertical)
    score_widget = create_score_widget('lightblue')
    multi_answer = AppLayout(header=question_widget,
              left_sidebar=option_widget,
              center=None,
              right_sidebar=None,
              footer=score_widget)

    multi_answer.box_style = 'info'

    # compare checkbox value with original
    def check_answers(b):

        #run through each option, compare expected answer (checked/unchecked) with actual student answer
        num_options = len(options)
        incorrect = 0
        missing = 0

        option_widget = multi_answer.children[2]
        score_widget = multi_answer.children[1]

        submit_button = score_widget.children[0]

        for i in range(num_options):

            opt = option_widget.children[i]

            lbl = opt.children[0]
            cb = opt.children[1].children[0]

            actual_answer = cb.value
            expected_answer = options[i]['correct']

            # clear feedback before giving new feedback
            opt.layout = Layout(border=None)
            lbl.value = ''
            lbl.layout=Layout(width='100px')

            # red border + 'incorrect' for incorrectly checked
            # green border + 'correct!' for correctly checked
            if (expected_answer and actual_answer):
                opt.layout = Layout(border='2px solid green')
                lbl.value = 'Correct!'
            if (expected_answer and not actual_answer):
                missing += 1
            if (not expected_answer and actual_answer):
                lbl.value = 'Incorrect'
                opt.layout = Layout(border='2px solid red')
                incorrect += 1

        # update the score label
        if incorrect + missing == 0:
            # Success! So disable checkboxes
            for i in range(num_options):
                opt = option_widget.children[i]
                cb = opt.children[1].children[0]
                cb.disabled = True

            if submit_button.description == 'Submit':
                text = ''
            else:
                text = 'Now you got it!'

            generate_feedback(multi_answer, score_widget, style='success', feedback_text = text, show_show_answer_btn = False)
            submit_button.layout.disable = True
        else:
            #Some incorrect answers, write feedback so they can try again
            if missing > 0:
                text = 'You missed some correct options, try again!'
            else:
                text = ''

            generate_feedback(multi_answer, score_widget, style='danger', feedback_text=text, show_show_answer_btn=False)

    submit_button = score_widget.children[0]
    submit_button.on_click(check_answers)

    return(multi_answer)


def create_fill_in_the_blanks_widget(question, sections):

    question_widget = create_question_widget(question)
    num_sections = len(sections)

    paragraph = HBox([], layout=Layout(display='flex', flex_flow='row wrap', align_items='stretch', width='auto'))
    for i in range(num_sections):
        section = sections[i]
        prefix = Label(value = section['prefix'], layout=Layout(width='auto'))
        blank = Text(value='', placeholder='', description='',
                             disabled=False, layout=(Layout(width='auto')))

        suffix = Label(value=section['suffix'], layout=Layout(width='auto'))

        new_hbox = widgets.HBox([prefix, blank, suffix],
                                layout=Layout(display='flex', flex_flow='row wrap', align_items='stretch', width='auto'))

        # new_hbox.box_style = 'info'
        paragraph.children += (new_hbox,)

    score_widget = create_score_widget('lightblue')
    fill_in = AppLayout(header=question_widget,
                             left_sidebar=paragraph,
                             center=None,
                             right_sidebar=None,
                             footer=score_widget, layout=Layout(display='flex', flex_flow='column', align_items='stretch', width='100%'))
    fill_in = VBox([question_widget, paragraph, score_widget], layout=Layout(display='flex', flex_flow='column', align_items='stretch', width='100%'))

    fill_in.box_style = 'info'


    # compare checkbox value with original
    def check_answers(b):
        # run through each option, compare expected answer (checked/unchecked) with actual student answer
        num_sections = len(sections)
        incorrect = 0
        missing = 0

        paragraph_widget = fill_in.children[1]
        feedback_widget = fill_in.children[2]

        submit_button = feedback_widget.children[0]

        for i in range(num_sections):
            blank = paragraph_widget.children[i].children[1]

            actual_answer = blank.value
            expected_answer = sections[i]['answer']

            # clear feedback before giving new feedback
            blank.layout = Layout(border='None', width='auto', height='32px')

            # red border + 'incorrect' for incorrectly checked
            # green border + 'correct!' for correctly checked
            if (actual_answer == ''):
                missing += 1
            elif (expected_answer == actual_answer):
                blank.layout = Layout(border='2px solid green', width='auto', height='32px')
            else:
                blank.layout = Layout(border='2px solid red', width='auto', height='32px')
                incorrect += 1

        # update the score label
        if incorrect + missing == 0:
            # Success! So disable checkboxes
            for i in range(num_sections):
                blank = paragraph_widget.children[i].children[1]
                blank.disabled = True

            if submit_button.description == 'Submit':
                text = ''
            else:
                text = 'Now you got it!'

            generate_feedback(fill_in, score_widget, style='success', feedback_text=text,
                              show_show_answer_btn=False)
            submit_button.layout.disable = True
        else:
            # Some incorrect answers, write feedback so they can try again
            if missing > 0:
                text = 'Fill in all the blanks!'
            else:
                text = ''

            generate_feedback(fill_in, score_widget, style='danger', feedback_text=text,
                              show_show_answer_btn=True)

    def show_answers(b):
        num_sections = len(sections)

        paragraph_widget = fill_in.children[1]
        feedback_widget = fill_in.children[2]
        submit_button = feedback_widget.children[0]

        for i in range(num_sections):

            blank = paragraph_widget.children[i].children[1]
            # clear feedback before giving the answers
            blank.value = ''
            blank.layout = Layout(border='None', width='auto', height='32px')

            blank.placeholder = sections[i]['answer']

        generate_feedback(fill_in, score_widget)

    submit_button = score_widget.children[0]
    submit_button.on_click(check_answers)
    show_answer_button = score_widget.children[2]
    show_answer_button.on_click(show_answers)

    return (fill_in)

def main(argv):
    json_file = sys.argv[1]
    with open(json_file) as f:
        quiz_dict = json.load(f)

    if quiz_dict['type'] == "multi-answer":
        w = create_multi_answer_widget(quiz_dict['question'], quiz_dict['options'])
    elif quiz_dict['type'] == "blanks":
        w = create_fill_in_the_blanks_widget(quiz_dict['question'], quiz_dict['sections'])
    else:
        return

    display(w)


# main function takes json file as input. acc. to type creates the widget and displays it
if __name__ == "__main__":
    main(sys.argv[1:])














