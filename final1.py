import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim, Circle
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
import random

### DIALOG BOX ROUTINE ###
exp_info = {
    'participant_nr': '',
    'age': '',
    'mood_rating (1=very bad, 5=very good)': '',
    'anxiety_rating (1=very low, 5=very high)': ''
}
dlg = DlgFromDict(exp_info)

###make it to numbers
mood_rating = int(exp_info['mood_rating (1=very bad, 5=very good)'])
anxiety_rating = int(exp_info['anxiety_rating (1=very low, 5=very high)'])

# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
win=Window(size=(1080, 800), fullscr=False)

# Also initialize a mouse, although we're not going to use it
mouse = Mouse(visible=True)

# Initialize a (global) clock
clock = Clock()

# Initialize Keyboard
kb = Keyboard()
kb.clearEvents()

##Deep breath
if mood_rating < 2 or anxiety_rating > 3:
    support_txt = TextStim(win, text="Please take a deep breath. Remember, you can pause anytime if you feel uncomfortable.",
                           color='white', height=0.07, wrapWidth=1.5)
    support_txt.draw()
    win.flip()
    wait(3)

### START BODY OF EXPERIMENT ###


### WELCOME ROUTINE ###
# Create a welcome screen and show for 2 seconds
welcome_txt_stim = TextStim(win, text="Welcome to this experiment!", color=(1, 0, -1), font='Calibri')
welcome_txt_stim.draw() #everytime we need the text to display, we need to draw it
win.flip()
wait(2.0)

### INSTRUCTION ROUTINE ### the 3""" makes the instruction display line by line
instruct_txt = instruct_txt = """ 
In this experiment, you have 3 blocks, and you will first see a number. Please remember it carefully.

Then, you will see emotional faces (either happy or angry) with a word above the image (either “happy” or “angry”).

Your task is to respond to the EXPRESSION of the face and ignore the word. Use the arrow keys:
    
    HAPPY expression = left arrow
    ANGRY expression = right arrow

After finishing all the trials, you will be asked to type the number you remembered.

Press ‘enter’ to start when you are ready!
"""

# Show instructions and wait until response (return)
instruct_txt = TextStim(win, instruct_txt, alignText='left', height=0.080)
instruct_txt.draw()
win.flip()

# Initialize keyboard and wait for response
kb = Keyboard()
while True:
    keys = kb.getKeys()
    if 'return' in keys:
        # The for loop was optional
        for key in keys:
            print(f"The {key.name} key was pressed within {key.rt:.3f} seconds for a total of {key.duration:.3f} seconds.")
        break  # break out of the loop!


### TRIAL LOOP ROUTINE ###
# Read in conditions file
original_df = pd.read_excel('emo_conditions.xlsx')
master_df = pd.DataFrame()  #create a new dataframe


###3 blocks
num_blocks = 3

for block in range(num_blocks):
    cond_df = original_df.sample(frac=1)#random order,1 means everything
    ### each block need to memorize certain numbers ###
    memory_item = random.randint(10000, 99999)
    memory_stim = TextStim(win, text=f"Block {block+1}: Please remember this number: {memory_item}", height=0.1)
    memory_stim.draw()
    win.flip()
    wait(2.0)


    ### create column in data ###
    cond_df['mood_rating'] = ''
    cond_df['anxiety_rating'] = ''
    cond_df['task_difficulty'] = ''
    cond_df['self_performance'] = ''
    cond_df['fatigue_level']=''
    cond_df['additional_comments'] = ''
    cond_df['block'] = block + 1
    cond_df['memory_item'] = memory_item

# Create fixation target (a plus sign)
    fix_target = TextStim(win, '+')
    trial_clock = Clock()
    clock.reset() # START exp clock

    fix_target.draw()
    win.flip()
    wait(1)

    for idx, row in cond_df.iterrows():
        # Extract current word and smiley, current row take by the row 'word'
        curr_word = row['word']
        curr_smil = row['smiley']

        # Create and draw text/img
        stim_txt = TextStim(win, curr_word, pos=(0, 0.4), height=0.25)
        stim_img = ImageStim(win, curr_smil + '.png')
        stim_img.size *= 0.5

        # Initially, onset is undefined (create a new column for the file, and add the value -1 in that 最后一行)
        cond_df.loc[idx, 'onset'] = -1

        trial_clock.reset() #reset to 0
        kb.clock.reset()
        while trial_clock.getTime() < 2:
            if trial_clock.getTime() < 0.5:
                stim_txt.draw()
                stim_img.draw()
            else:
                fix_target.draw()

            win.flip()
            if cond_df.loc[idx, 'onset'] == -1:
                cond_df.loc[idx, 'onset'] = clock.getTime()  #it is measuring the time the image is showing

            resp = kb.getKeys()
            if resp:
                if 'q' in resp:
                    quit()
                cond_df.loc[idx, 'rt'] = resp[-1].rt
                cond_df.loc[idx, 'resp'] = resp[-1].name

                if resp[-1].name == 'left' and curr_smil == 'happy':
                    cond_df.loc[idx, 'correct'] = 1
                elif resp[-1].name == 'right' and curr_smil == 'angry':
                    cond_df.loc[idx, 'correct'] = 1
                else:
                    cond_df.loc[idx, 'correct'] = 0

    effect = cond_df.groupby('congruence').mean()
    rt_con = effect.loc['congruent', 'rt']
    rt_incon = effect.loc['incongruent', 'rt']
    acc = cond_df['correct'].mean()

    txt = f"""
    Block {block+1} done!

    Congruent RT: {rt_con:.3f}
    Incongruent RT: {rt_incon:.3f}
    Accuracy: {acc:.3f}
    """
    result = TextStim(win, txt)
    result.draw()
    win.flip()
    wait(4)

    ### Recall the memory###
    memory_recall = {'What was the number you remembered?': ''}
    dlg = DlgFromDict(memory_recall)
    if memory_recall['What was the number you remembered?'] == str(memory_item):
        feedback_txt = TextStim(win, text="Correct!", color='green', height=0.15)
        memory_correct = 1
    else:
        feedback_txt = TextStim(win, text=f"Incorrect! Correct was {memory_item}", color='red', height=0.15)
        memory_correct = 0
    feedback_txt.draw()
    win.flip()
    wait(2)

    cond_df['memory_recall'] = memory_recall['What was the number you remembered?']
    cond_df['memory_correct'] = memory_correct

    ### merge to master_df ###
    master_df = pd.concat([master_df, cond_df], ignore_index=True)

# feedback after complete all blocks===
feedback_txt_stim = TextStim(win, text="Do you like this experiment? Green: Yes; Red: No", color=(1, 0, -1), font='Calibri', height=0.1)
feedback_txt_stim.draw()
win.flip()
wait(2.0)

red_circle = Circle(win=win, units="pix", radius=50, fillColor=[1, 0, 0], pos=(50, 0))
green_circle = Circle(win=win, units="pix", radius=50, fillColor=[0, 1, 0], pos=(-50, 0))
green_circle.draw()
red_circle.draw()
win.flip()

feedback = "NA"

while True:
    if mouse.isPressedIn(green_circle):  ###green
        feedback = "green"
        wait(1)
        post_feedback = {
            'task_difficulty (1=very easy, 5=very hard)': '',
            'self_performance (1=very poor, 5=very good)': '',
            'fatigue_level (1=not tired, 5=very tired)': ''
        }
        dlg = DlgFromDict(post_feedback)
        break
    elif mouse.isPressedIn(red_circle):   ####red
        feedback = "red"
        more_feedback = {
            'additional_comments': ''
        }
        dlg = DlgFromDict(more_feedback)
        break

if feedback == 'green':
    master_df['task_difficulty'] = post_feedback['task_difficulty (1=very easy, 5=very hard)']
    master_df['self_performance'] = post_feedback['self_performance (1=very poor, 5=very good)']
    master_df['fatigue_level'] = post_feedback['fatigue_level (1=not tired, 5=very tired)']
elif feedback == 'red':
    master_df['additional_comments'] = more_feedback['additional_comments']

master_df['feedback'] = feedback
###save the result
master_df.to_csv(f"sub-{exp_info['participant_nr']}_results.csv", index=False)
##window colse
win.close()
quit()
