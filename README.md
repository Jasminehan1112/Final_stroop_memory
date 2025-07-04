# Final_stroop_memory
It is Yunwei Han's final assignment. The experiment combines an emotional Stroop task with a working memory component and includes mood and anxiety self-reports.

#Aim
This experiment combines a classic emotional Stroop task with a simple working memory component and collects self-reported mood and anxiety scores from each participant.  
The goal is to explore how working memory interference affects reaction time and accuracy, while adding an individual difference perspective (mood/anxiety).

###Main festures
The main features are:
- 3 blocks of trials.
- Each block starts with a random 5-digit number to remember.
- Participants respond to the **expression** (happy/angry) of faces while ignoring words.
- After each block, participants recall the number.
- Immediate feedback on memory accuracy.
- Final feedback survey about task difficulty and self-performance.
  
###Detailed Procedures
When participating in this experiment, each participant will first enter their demographic questions, including their age and participant number. Then they will be asked to report their anxiety level scores and current mood scores. If their anxiety level is high (which is greater than 3 in this experiment) or their mood scores are low (lower than 2), a supportive comment would appear to comfort the participants. 
After seeing the instructions, participants would undergo three blocks of trials. In each block, each participant is required to memorise a five-digit number. Then they would undergo the traditional emotional stroop task (Respond to the expression (happy/angry) while ignoring words. After that, they would be required to recall the numbers they had been asked to remember at first, immediate feedback of the recall would apperar on the screen.
After three blocks of trials, there would be a final feedback asking participants whether they liked the experiment or not. If they choose "Yes", they would be asked about their task difficulty, self-performance (1=very poor, 5=very good), and fatigue level. If they choose "No", a space would appear to let them write some comments on the experiment. 

###How to Run
Make sure you have the condition file 'emo_conditions.xlsx,' 'angry.png,' and 'happy.png' in the same folder as the Python script.
Run the script

###Packages and Dependencies
-Psychopy
-Panda

###Summary of Result
After taking the experiment, there will be a file named like sub-001_results.csv in the directory. 
This file includes:
-Reaction times and accuracy for each trial.
-Congruence condition per trial.
-Block number.
-Memorized number and participant recall.
-Whether the memory recall was correct (1) or incorrect (0).
-Participant mood and anxiety ratings.
-Final feedback ratings on task difficulty and self-performance, or additional comments.
