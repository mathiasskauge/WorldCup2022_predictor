import pandas as pd

import warnings
warnings.filterwarnings("ignore")

#Found out which cells contain scores by testing

#Each groupstage round is for example row in 12, 17, 22 ... 37
#Home and away teams number of goals are in columns 1,2 4,5 7,8 ... 22,23


def points_calculator(correct_df, guesser_df):
    """ 
    Calculate a guessers points in 'Tippekonk VM 2022'

    :param correct_df: The pandas dataframe of the correct scores
    :param guesser_df: The pandas dataframe of the guessers predictions

    :return: The guessers points
    :rtype: int
    """

    #Point-counter
    points = 0

    ### GROUPSTAGE COUNTER ###

    #x is the group
    #y is the individual game

    for x in range(12, 42, 5):
        for y in range(1, 25, 3):
            #Finding true result for the game
            home_true = correct_df.iloc[x][y]
            #Using y+1 to find awayteams score
            away_true = correct_df.iloc[x][y+1]

            #Finding guessed result for the game
            home_guess = guesser_df.iloc[x][y]
            away_guess = guesser_df.iloc[x][y+1]

            #Checking who won the game or tie (1X2) for FASIT
            result_true = 0
            if home_true > away_true:
                result_true = 1
            elif home_true < away_true:
                result_true = -1

            #Checking who won the game or tie (1X2) for the guesser
            result_guess = 0
            if home_guess > away_guess:
                result_guess = 1
            elif home_guess < away_guess:
                result_guess = -1

            #Adding 5 points for correct score, 3 points for only correct 1X2, 0 points if all wrong
            if home_true == home_guess and away_true == away_guess:
                points += 5
            elif result_true == result_guess:
                points += 3



    ### KNOCKOUT STAGE COUNTER ###

    ## ROUND OF 16 ##
    #Finding correct teams in round of 16
    r16_teams = []
    for y in range(1, 25, 3):
        r16_teams.append(correct_df.iloc[48][y])
        r16_teams.append(correct_df.iloc[48][y+1])
        

    #Finding guessed teams in round of 16
    guessed_r16 = []
    for y in range(1, 25, 3):
        guessed_r16.append(guesser_df.iloc[48][y])
        guessed_r16.append(guesser_df.iloc[48][y+1])
        

    #Adding 5 points for each correct team guessed in quarterfinals
    points += len(set(r16_teams) & set(guessed_r16)) * 5


    ## QUARTERFINALS ##

    #Finding correct teams in quarterfinals
    qf_teams = []
    for y in range(2, 26, 6):
        qf_teams.append(correct_df.iloc[58][y])
        qf_teams.append(correct_df.iloc[58][y+2])

    #Finding guessed teams in quarterfinals
    guessed_qf = []
    for y in range(2, 26, 6):
        guessed_qf.append(guesser_df.iloc[58][y])
        guessed_qf.append(guesser_df.iloc[58][y+2])

    #Adding 10 points for each correct team guessed in quarterfinals
    points += len(set(qf_teams) & set(guessed_qf)) * 10


    ## SEMIFINALS ##

    #Finding correct teams in semifinals
    semi_teams = []
    for y in range(5, 29, 12):
        semi_teams.append(correct_df.iloc[68][y])
        semi_teams.append(correct_df.iloc[68][y+2])

    #Finding guessed teams in semifinals
    guessed_semi = []
    for y in range(5, 29, 12):
        guessed_semi.append(guesser_df.iloc[68][y])
        guessed_semi.append(guesser_df.iloc[68][y+2])


    #Adding 15 points for each correct team guessed in semifinal
    points += len(set(semi_teams) & set(guessed_semi)) * 15


    ## FINAL ##

    #Finding correct teams in the final
    final_teams = []
    final_teams.append(correct_df.iloc[86][11])
    final_teams.append(correct_df.iloc[86][13])

    #Finding guessed teams in the final
    guessed_final = []
    guessed_final.append(guesser_df.iloc[86][11])
    guessed_final.append(guesser_df.iloc[86][13])
    
    #Adding 20 points for each correct team guessed in the final
    points += len(set(final_teams) & set(guessed_final)) * 20

    #Checking if the correct winner is guessed
    #Finding the winner
    home = correct_df.iloc[86][11]
    away = correct_df.iloc[86][13]
    if correct_df.iloc[87][11] > correct_df.iloc[87][13]:
        winner = home
    else:
        winner = away
    guessed_home = guesser_df.iloc[86][11]
    guessed_away = guesser_df.iloc[86][13]

    #Finding guessed winner
    if guesser_df.iloc[87][11] > guesser_df.iloc[87][13]:
        guessed_winner = guessed_home
    elif guesser_df.iloc[87][11] == guesser_df.iloc[87][13]:
        #FInding winner if guesser predicted the final to go to penalties
        if guesser_df.iloc[89][11] > guesser_df.iloc[89][13]:
            guessed_winner = guessed_home  
        else:
            guessed_winner = guessed_away
    else:
        guessed_winner = guessed_away
    #Adding 35 points if the correct winner is guessed
    if winner == guessed_winner and str(correct_df.iloc[87][11]) != 'nan':
        points += 35

    return points


#########################################################################

#Add paths to your friend groups excel sheets here
friends = ['My_guesses.xlsx']

'''
ls = [
    'Skauge-Tippekonk-VM-2022.xlsx',
    'Buer-Tippekonk-VM-2022.xlsx',
    'Dennis-Tippekonk-VM-2022.xlsx',
    'Gran-Tippekonk-VM-2022.xlsx',
    'Jakob-Tippekonk-VM-2022.xlsx',
    'Nys-Tippekonk-VM-2022.xlsx',
    'Sandberg-Tippekonk-VM-2022.xlsx',
    'Trym-Tippekonk-VM-2022.xlsx',
]

kollektivet = [
    'Skauge-Tippekonk-VM-2022.xlsx',
    'MathiasSJ-Tippekonk-VM-2022.xlsx',
    'Maria-Tippekonk-VM-2022.xlsx',
]
'''

#Choose group to show results from (ls/kollektivet)
guesser_paths = friends

fasit_path = 'Correct_results.xlsx'
sheet = 'World Cup'

correct_df = pd.read_excel(io=fasit_path, sheet_name=sheet)

#Looping through all guesser files and adding the scores to a dictionary
scores = {}
for i in range(len(guesser_paths)):
    guesser_path = guesser_paths[i]
    guesser_df = pd.read_excel(io=guesser_path, sheet_name=sheet)
    scores[guesser_path.split('-')[0]] = points_calculator(correct_df, guesser_df)
   
#Sort scores from highest to lowest
sorted_scores = dict(sorted(scores.items(), key=lambda x:x[1], reverse=True))

#Printing all scores
for key, value in sorted_scores.items():
    print(f"{key}: {value}")

