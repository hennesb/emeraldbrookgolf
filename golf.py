from datetime import datetime, date, time
import sqlite3


max_holes = 18

pars = [4,4,4,4,5,3,5,4,3,5,3,5,4,4,4,3,4,4]
hole_index= [7,3,1,9,15,13,11,5,17,14,6,16,8,18,2,12,10,4]

def get_points(diff):
    stableford_points = {2:0, 1:1, 0:2, -1:3, -2:4, -3:5, -4:6, -5:7, -6:8, -7:9, -8:10, -9:11,  -10:12, -11:13, -12:14, -13:15}
    if (diff > 2):
        return 0
    else:
        if diff in stableford_points:
            return stableford_points.get(diff)
        else:
            raise Exception('Something has gone wrong here with the number of points. Or maybe your stableford points are really high')



def print_all(scores, hole_index, points_allowed_dict):
    for index, score in enumerate(scores):
        print 'Scored ' + str(score) + ' :Index '  + str(hole_index[index]) + ':Stblford  ' +  ':Par ' \
        + str(pars[index])



def print_hole_index(hole_index):
    print type(hole_index)
    for hole_number, i in enumerate(hole_index):
         print 'Hole number is ' + str(hole_number + 1) + ' has an index of ' + str(i) 


def isnumeric(string):
    try:
        integer = int(string)
        return 1
    except ValueError, TypeError:
        return 0


def ask_for_player_name():
    name=raw_input('Please enter a name or email =>')
    if (len(name) > 1):
        return name
    else:
       print 'You have not entered a name'
       return ask_for_player_name()


def ask_for_number_of_players():
    number_of_players=raw_input('How many players do you have =>')
    if isnumeric(number_of_players):
        return number_of_players
    else:
        print 'Please enter a number for the number of players'
        return ask_for_number_of_players()


def ask_for_handicap(name):
    handicap=raw_input('Please provide a handicap for '+ name + '=>')
    if isnumeric(handicap):
        return handicap
    else:
        print 'Please enter a number for the handicap'
        return ask_for_handicap(name)


def recursiveInput(scores):
    if (len(scores) == max_holes):
        return
    else:
        score=raw_input('Enter score for hole ' + str(len(scores)+1) +' =>')
        if isnumeric(score):
           if (int(score)< 0):
               print 'Score cannot be less than 0'
               return recursiveInput(scores)
           else:
               scores.append(int(score))
               return recursiveInput(scores)
        else:
           print 'Please enter a numeric score'
           return recursiveInput(scores)


def points_based_on_hole_index(handicap):
    stableford_hashmap = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0}
    decreasing_counter = int(handicap)
    new_points = 0

    while (decreasing_counter > 0):
        for i in range(18):
            new_points = 0
            if (decreasing_counter < 1):
                break
            else:
                current_allowed_points = stableford_hashmap.get(i+1)
                new_points = current_allowed_points + 1
                stableford_hashmap[i+1] = new_points
                decreasing_counter = decreasing_counter - 1

    return stableford_hashmap


def get_new_par_based_on_stableford_rules(stableford_points_per_index, pars, hole_index):  
    new_pars = []   
    for index,par in enumerate(pars):
        difficulty_index = hole_index[index]
        revised_par = par + stableford_points_per_index.get(difficulty_index)
        new_pars.append(revised_par)
    return new_pars


def calculate_overall_points(scores ,new_pars):
    final_stableford_points = []
    for index,score in enumerate(scores):
        if (score > 0):
            par = new_pars[index]
            diff = score - par
            points = get_points(diff)
            final_stableford_points.append(points)
        else:
            final_stableford_points.append(0)
    return final_stableford_points



def is_existing_user(player_name):
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) from scores where upper(player_name)=?"
    params = []
    params.append(player_name.upper())
    cursor.execute(sql, params)
    result=cursor.fetchone()
    number_of_rows=result[0]
    if int(number_of_rows) > 0:
        return 1
    else:
        return 0


def update_database(player_name, handicap, points, scores, day):
    params = []   
    params.append(handicap)
    params.append(sum(points[:9]))
    params.append(sum(points[9:]))
    params.append(sum(points))
    params.append(player_name.upper())

    if (day==1):
        sql = "insert into scores(handicap_1, front_day_1,back_day_1,total_day_1,player_name) values (?,?,?,?,?)"
    else:
        sql = "update scores set handicap_2 =? , front_day_2 = ?, back_day_2 = ?, total_day_2 = ? where upper(player_name) = ?"

    
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)

    for hole_number, score in enumerate(scores):
        params_2 = []
        params_2.append(player_name.upper())
        params_2.append(hole_number+1)
        params_2.append('MOUNT WOLSELEY')  
        params_2.append(score)
        params_2.append(points[hole_number])        
        params_2.append(day)   
        sql2="insert into player_performance(player_name, hole_number, course, score, points, day) values (?,?,?,?,?,?)"   
        cursor.execute(sql2, params_2)

    conn.commit()



def print_and_write_summary(name, handicap, final_score):
    print '-------------------------------' 
    print 'Score Summary for =>' + name 
    print 'Total points      =>' + str(sum(final_score))
    print 'Front 9 points    =>' + str(sum(final_score[:9]))
    print 'Back 9 points     =>' + str(sum(final_score[9:]))
    print 'Final points      =>' + str(final_score)

    with open("results.txt", "a") as f:
        now = datetime.now()
        f.write('------' + now.strftime('%Y-%m-%d-%s') + '-------\n')
        f.write('Score Summary for =>' + name + '\n')
        f.write('Handicap          =>' + handicap + '\n')
        f.write('Total points      =>' + str(sum(final_score)) + '\n')
        f.write('Front 9 points    =>' + str(sum(final_score[:9])) + '\n')
        f.write('Back 9 points     =>' + str(sum(final_score[9:])) + '\n')
        f.close()



    


def write_diagnostics(name, handicap ,scores, allowed_stableford_points, pars, new_pars, final_points):
    with open("diagnostic.txt","a") as f:
        f.write('-------- Diagnostic Report --------------' + '\n')
        f.write('Name is      =>' + name + '\n')
        f.write('Handicap is  =>' + str(handicap) + '\n')
        f.write('Points       =>' + str(sum(final_points)) + '\n')
        f.write('Scores       =>' + str(scores) + '\n')
        f.write('Points       =>' + str(final_points) + '\n')
        f.write('Pars         =>' + str(pars) + '\n')
        f.write('New Pars     =>' + str(new_pars) + '\n')
        f.write('Addional Pts =>' + str(allowed_stableford_points) + '\n')
        f.close()




def recursive_input_for_day():
    day_number=raw_input('Enter if this is day 1 or 2 =>')
    if isnumeric(day_number):
        if int(day_number) < 1 or int(day_number) > 2:
            print 'Day number must be 1 or 2 . Please reenter'
            return recursive_input_for_day()
        else:
            return int(day_number)
    else:
        print 'Please enter a number for the number of players'
        return recursive_input_for_day()


def confirm_update():
    confirm_flag=raw_input('Do you wish to submit these details. Press (Y/N) =>')
    if (confirm_flag.upper() not in ('Y','N')):
        print 'You have not answered Y/N to this question'
        return confirm_update()
    else: 
        return confirm_flag.upper()


def print_submitted_cards(day):
    params =[]
    params.append(day)
    sql = "select count(distinct player_name) from player_performance where day=?"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result=cursor.fetchone()
    count_last_day_submitted_cards=result[0]
    print 'Number of submitted cards for this day ' + str(count_last_day_submitted_cards)

def print_overall_first_second():
    sql = "select player_name as overall_winner, ifnull(total_day_1,0) + ifnull(total_day_2,0) as points from scores \
           order by points desc limit 2"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    for index,r in enumerate(result):
        if (index):
            print 'Second place overall ' + r[0] + ' with ' + str(r[1]) + ' points'
        else:
            check_sql="select count(*) from scores where ifnull(total_day_1,0) + ifnull(total_day_2,0) = ?"
            params = []
            params.append(r[1])
            cursor.execute(check_sql,params)
            result=cursor.fetchone()
            count=result[0]
            if (count > 1):
                print 'ALERT We have a tie break for overall winner. Please inspect cards manually'
                return
            else:
                print 'First place overall WINNER IS ' + r[0] + ' with ' + str(r[1]) + ' points'
    

def print_winner_front_day_1():
    sql = "select player_name,ifnull(front_day_1,0) as front_day_1 from scores order by front_day_1 desc limit 1"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    for index,r in enumerate(result):
        dup_sql="select count(*) from scores where front_day_1=?"
        params = []
        params.append(r[1])
        cursor.execute(dup_sql,params)
        result=cursor.fetchone()
        count=result[0]
        if count > 1:
            print 'ALERT !! Front 9 day 1 is drawn by ' + str(count) + ' players. Please calculate manually' 
        else:
            print 'Front 9 day 1 won by ' + r[0] + ' with ' + str(r[1]) + ' points'


def print_winner_front_day_2():
    sql = "select player_name,ifnull(front_day_2,0) as front_day_2 from scores order by front_day_2 desc limit 1"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    for index,r in enumerate(result):
        dup_sql="select count(*) from scores where front_day_2=?"
        params = []
        params.append(r[1])
        cursor.execute(dup_sql,params)
        result=cursor.fetchone()
        count=result[0]
        if count > 1:
            print 'ALERT !! Front 9 day 2 is drawn by ' + str(count) + ' players. Please calculate manually' 
        else:
            print 'Front 9 day 2 won by ' + r[0] + ' with ' + str(r[1]) + ' points'

def print_winner_back_day_1():
    sql = "select player_name,ifnull(back_day_1,0) as back_day_1 from scores order by back_day_1 desc limit 1"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    for index,r in enumerate(result):
        dup_sql="select count(*) from scores where back_day_1=?"
        params = []
        params.append(r[1])
        cursor.execute(dup_sql,params)
        result=cursor.fetchone()
        count=result[0]
        if count > 1:
            print 'ALERT !! Back 9 day 1 is drawn by ' + str(count) + ' players. Please calculate manually' 
        else:
            print 'Back 9 day 1 won by ' + r[0] + ' with ' + str(r[1]) + ' points'



def print_winner_back_day_2():
    sql = "select player_name,ifnull(back_day_2,0) as back_day_2 from scores order by back_day_2 desc limit 1"
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    for index,r in enumerate(result):
        dup_sql="select count(*) from scores where back_day_2=?"
        params = []
        params.append(r[1])
        cursor.execute(dup_sql,params)
        result=cursor.fetchone()
        count=result[0]
        if count > 1:
            print 'ALERT !! Back 9 day 2 is drawn by ' + str(count) + ' players. Please calculate manually' 
        else:
            print 'Back 9 day 2 won by ' + r[0] + ' with ' + str(r[1]) + ' points'


day=recursive_input_for_day()

while 1:
    player_name=ask_for_player_name() 
    handicap=ask_for_handicap(player_name)
    scores=[]  
    recursiveInput(scores)
    stableford_points_per_index=points_based_on_hole_index(handicap)
    new_pars=get_new_par_based_on_stableford_rules(stableford_points_per_index, pars ,hole_index)
    final_points=calculate_overall_points(scores, new_pars)
    confirm=confirm_update()
    if (confirm=='Y'):
        print_and_write_summary(player_name, handicap, final_points)
        write_diagnostics(player_name, handicap, scores, stableford_points_per_index, pars, new_pars, final_points)
        update_database(player_name, handicap, final_points, scores,day)
        print ' '
        print '******** Summary Overall **********'
        print_submitted_cards(day)
        print_overall_first_second()
        print_winner_front_day_1()
        print_winner_back_day_1()
        print_winner_front_day_2()
        print_winner_back_day_2()
        
    else:
        print 'Details have not been saved'
  







