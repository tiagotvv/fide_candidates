import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import chess 
import chess.pgn
import chess.svg
import base64
import math
import textwrap

st.title('FIDE Candidates Tournament 2022')
st.write('Analyzing the games for the FIDE Candidates Tournament of 2022. The tournament winner becomes the challenger for the FIDE World Championship and faces the reigning World Champion Magnus Carlsen in a match in 2023.')
st.markdown('Eight players take part: **Ian Nepomniachtchi** (2021 Match runner up), \
**Jan-Krzysztof Duda** (World Cup winner), **Alireza Firouzja**  (Grand Swiss winner), **Fabiano Caruana** (Grand Swiss runner up)\
, **Hikaru Nakamura**  (Grand Prix winner), **Richard Rapport** (Grand Prix runner up), **Ding Liren** (highest rating in May 2022) and \
**Teimour Radjabov** (FIDE wild card)')
@st.cache
def load_data():
    games = pd.read_csv('games.csv', encoding='utf-8')
    detailed_games = pd.read_csv('detailed_games.csv', encoding='utf-8')
    all_evals = pd.read_csv('all_evals.csv', encoding='utf-8')
    all_times = pd.read_csv('all_times.csv', encoding='utf-8')

    return games, detailed_games, all_evals, all_times

games, detailed_games, all_evals, all_times = load_data()

def mmss(seconds):
    if seconds == 0:
        return 'N/A'
    else:
        a = int(seconds/60)
        b = int(60*(seconds/60 - a))
        return str(a)+'min '+str(b)+'s'
idx = -1
#st.write(games.head())

dict_games = {-1:' ',
0: 'Round 1: Jan-Krzysztof Duda vs Richard Rapport',
 1: 'Round 1: Ding Liren vs Ian Nepomniachtchi',
 2: 'Round 1: Fabiano Caruana vs Hikaru Nakamura',
 3: 'Round 1: Teimour Radjabov vs Alireza Firouzja',
 4: 'Round 2: Richard Rapport vs Alireza Firouzja',
 5: 'Round 2: Hikaru Nakamura vs Teimour Radjabov',
 6: 'Round 2: Ian Nepomniachtchi vs Fabiano Caruana',
 7: 'Round 2: Jan-Krzysztof Duda vs Ding Liren',
 8: 'Round 3: Ding Liren vs Richard Rapport',
 9: 'Round 3: Fabiano Caruana vs Jan-Krzysztof Duda',
 10: 'Round 3: Teimour Radjabov vs Ian Nepomniachtchi',
 11: 'Round 3: Alireza Firouzja vs Hikaru Nakamura',
 12: 'Round 4: Richard Rapport vs Hikaru Nakamura',
 13: 'Round 4: Ian Nepomniachtchi vs Alireza Firouzja',
 14: 'Round 4: Jan-Krzysztof Duda vs Teimour Radjabov',
 15: 'Round 4: Ding Liren vs Fabiano Caruana',
 16: 'Round 5: Fabiano Caruana vs Richard Rapport',
 17: 'Round 5: Teimour Radjabov vs Ding Liren',
 18: 'Round 5: Alireza Firouzja vs Jan-Krzysztof Duda',
 19: 'Round 5: Hikaru Nakamura vs Ian Nepomniachtchi',
 20: 'Round 6: Teimour Radjabov vs Richard Rapport',
 21: 'Round 6: Alireza Firouzja vs Fabiano Caruana',
 22: 'Round 6: Hikaru Nakamura vs Ding Liren',
 23: 'Round 6: Ian Nepomniachtchi vs Jan-Krzysztof Duda',
 24: 'Round 7: Richard Rapport vs Ian Nepomniachtchi',
 25: 'Round 7: Jan-Krzysztof Duda vs Hikaru Nakamura',
 26: 'Round 7: Ding Liren vs Alireza Firouzja',
 27: 'Round 7: Fabiano Caruana vs Teimour Radjabov',
 28: 'Round 8: Richard Rapport vs Jan-Krzysztof Duda',
 29: 'Round 8: Ian Nepomniachtchi vs Ding Liren',
 30: 'Round 8: Hikaru Nakamura vs Fabiano Caruana',
 31: 'Round 8: Alireza Firouzja vs Teimour Radjabov',
 32: 'Round 9: Alireza Firouzja vs Richard Rapport',
 33: 'Round 9: Teimour Radjabov vs Hikaru Nakamura',
 34: 'Round 9: Fabiano Caruana vs Ian Nepomniachtchi',
 35: 'Round 9: Ding Liren vs Jan-Krzysztof Duda',
 36: 'Round 10: Richard Rapport vs Ding Liren',
 37: 'Round 10: Jan-Krzysztof Duda vs Fabiano Caruana',
 38: 'Round 10: Ian Nepomniachtchi vs Teimour Radjabov',
 39: 'Round 10: Hikaru Nakamura vs Alireza Firouzja',
 40: 'Round 11: Hikaru Nakamura vs Richard Rapport',
 41: 'Round 11: Alireza Firouzja vs Ian Nepomniachtchi',
 42: 'Round 11: Teimour Radjabov vs Jan-Krzysztof Duda',
 43: 'Round 11: Fabiano Caruana vs Ding Liren',
 44: 'Round 12: Richard Rapport vs Fabiano Caruana',
 45: 'Round 12: Ding Liren vs Teimour Radjabov',
 46: 'Round 12: Jan-Krzysztof Duda vs Alireza Firouzja',
 47: 'Round 12: Ian Nepomniachtchi vs Hikaru Nakamura',
 48: 'Round 13: Ian Nepomniachtchi vs Richard Rapport',
 49: 'Round 13: Hikaru Nakamura vs Jan-Krzysztof Duda',
 50: 'Round 13: Alireza Firouzja vs Ding Liren',
 51: 'Round 13: Teimour Radjabov vs Fabiano Caruana',
 52: 'Round 14: Richard Rapport vs Teimour Radjabov',
 53: 'Round 14: Fabiano Caruana vs Alireza Firouzja',
 54: 'Round 14: Ding Liren vs Hikaru Nakamura',
 55: 'Round 14: Jan-Krzysztof Duda vs Ian Nepomniachtchi'}

option = st.selectbox(
     'Select the game:',
     (' ','Round 1: Jan-Krzysztof Duda vs Richard Rapport',
 'Round 1: Ding Liren vs Ian Nepomniachtchi',
 'Round 1: Fabiano Caruana vs Hikaru Nakamura',
 'Round 1: Teimour Radjabov vs Alireza Firouzja',
 'Round 2: Richard Rapport vs Alireza Firouzja',
 'Round 2: Hikaru Nakamura vs Teimour Radjabov',
 'Round 2: Ian Nepomniachtchi vs Fabiano Caruana',
 'Round 2: Jan-Krzysztof Duda vs Ding Liren',
 'Round 3: Ding Liren vs Richard Rapport',
 'Round 3: Fabiano Caruana vs Jan-Krzysztof Duda',
 'Round 3: Teimour Radjabov vs Ian Nepomniachtchi',
 'Round 3: Alireza Firouzja vs Hikaru Nakamura',
 'Round 4: Richard Rapport vs Hikaru Nakamura',
 'Round 4: Ian Nepomniachtchi vs Alireza Firouzja',
 'Round 4: Jan-Krzysztof Duda vs Teimour Radjabov',
 'Round 4: Ding Liren vs Fabiano Caruana',
 'Round 5: Fabiano Caruana vs Richard Rapport',
 'Round 5: Teimour Radjabov vs Ding Liren',
 'Round 5: Alireza Firouzja vs Jan-Krzysztof Duda',
 'Round 5: Hikaru Nakamura vs Ian Nepomniachtchi',
 'Round 6: Teimour Radjabov vs Richard Rapport',
 'Round 6: Alireza Firouzja vs Fabiano Caruana',
 'Round 6: Hikaru Nakamura vs Ding Liren',
 'Round 6: Ian Nepomniachtchi vs Jan-Krzysztof Duda',
 'Round 7: Richard Rapport vs Ian Nepomniachtchi',
 'Round 7: Jan-Krzysztof Duda vs Hikaru Nakamura',
 'Round 7: Ding Liren vs Alireza Firouzja',
 'Round 7: Fabiano Caruana vs Teimour Radjabov',
 'Round 8: Richard Rapport vs Jan-Krzysztof Duda',
 'Round 8: Ian Nepomniachtchi vs Ding Liren',
 'Round 8: Hikaru Nakamura vs Fabiano Caruana',
 'Round 8: Alireza Firouzja vs Teimour Radjabov',
 'Round 9: Alireza Firouzja vs Richard Rapport',
 'Round 9: Teimour Radjabov vs Hikaru Nakamura',
 'Round 9: Fabiano Caruana vs Ian Nepomniachtchi',
 'Round 9: Ding Liren vs Jan-Krzysztof Duda',
 'Round 10: Richard Rapport vs Ding Liren',
 'Round 10: Jan-Krzysztof Duda vs Fabiano Caruana',
 'Round 10: Ian Nepomniachtchi vs Teimour Radjabov',
 'Round 10: Hikaru Nakamura vs Alireza Firouzja',
 'Round 11: Hikaru Nakamura vs Richard Rapport',
 'Round 11: Alireza Firouzja vs Ian Nepomniachtchi',
 'Round 11: Teimour Radjabov vs Jan-Krzysztof Duda',
 'Round 11: Fabiano Caruana vs Ding Liren',
 'Round 12: Richard Rapport vs Fabiano Caruana',
 'Round 12: Ding Liren vs Teimour Radjabov',
 'Round 12: Jan-Krzysztof Duda vs Alireza Firouzja',
 'Round 12: Ian Nepomniachtchi vs Hikaru Nakamura',
 'Round 13: Ian Nepomniachtchi vs Richard Rapport',
 'Round 13: Hikaru Nakamura vs Jan-Krzysztof Duda',
 'Round 13: Alireza Firouzja vs Ding Liren',
 'Round 13: Teimour Radjabov vs Fabiano Caruana',
 'Round 14: Richard Rapport vs Teimour Radjabov',
 'Round 14: Fabiano Caruana vs Alireza Firouzja',
 'Round 14: Ding Liren vs Hikaru Nakamura',
 'Round 14: Jan-Krzysztof Duda vs Ian Nepomniachtchi'))
board = chess.Board() 


ply = 0
if option == ' ':
    pass
else:
    

    st.markdown('#### Replay Game')

    idx = [key for key, value in dict_games.items() if value == option]
    idx = idx[0]
    white = (games.query('GameID == @idx')['White'].values)[0]
    black = (games.query('GameID == @idx')['Black'].values)[0]
    result = (games.query('GameID == @idx')['Result'].values)[0]
    moves =  detailed_games.query('GameID == @idx').reset_index(drop=True)


    st.markdown('**'+ option + ': ' + result + '**')
    #st.write(white, black)
    time = all_times.query('GameID == @idx')[['White', 'Black']].reset_index(drop=True)
    evaluation_ply = all_evals.query('GameID == @idx')['evaluation'].reset_index(drop=True)

    ply = st.slider('Halfmove Slider', 0, evaluation_ply.shape[0], 0)
    

    ppp=0
    lastmove = None
    while ppp<=ply-1:
        if ppp%2 == 0:
            lastmove = board.parse_san(moves['White'][int(ppp/2)])
            board.push_san(moves['White'][int(ppp/2)])
        else:
            lastmove = board.parse_san(moves['Black'][int(ppp/2)])
            board.push_san(moves['Black'][int(ppp/2)])     
        ppp = ppp+1
    
    pp=chess.svg.board(board, lastmove=lastmove, size=400)

    c1,c2 = st.columns([2,1])
    def render_svg(svg):
        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        c1.write(html, unsafe_allow_html=True)

    c1.markdown('Black: **'+black+'**')
    render_svg(pp)
    c1.markdown('White: **'+white+'**')
    c2.markdown('\n\n\n\n')
    c2.markdown('\n\n\n\n')

    
    if ply > 0:
        if ply%2 == 0:
            ev = moves['Eval Black'][int((ply-1)/2)]
            c2.markdown('**Position after** '+str(int(ply/2))+'... '+moves['Black'][int((ply-1)/2)])
            c2.markdown('**Evaluation:** '+str(ev))
            c2.markdown('**Expected Score:** '+str(round(1/(1+10**(-0.25*ev)),2))+'-'+str(round(1-(1/(1+10**(-0.25*ev))),2)))
            c2.markdown('**Black Clock:** '+moves['RemTime Black'].fillna(0).apply(mmss)[int((ply-1)/2)])
            c2.markdown('**White Clock:** '+str(moves['RemTime White'].fillna(0).apply(mmss)[int((ply-1)/2)]))

        else:
            ev = moves['Eval White'][int((ply-1)/2)]
            c2.markdown('**Position after** '+str(int(ply/2)+1)+'. '+moves['White'][int((ply-1)/2)])
            c2.markdown('**Evaluation:** '+str(ev))
            c2.markdown('**Expected Score:** '+str(round(1/(1+10**(-0.25*ev)),2))+'-'+str(round(1-(1/(1+10**(-0.25*ev))),2)))
            if ply == 1:
                c2.markdown('**Black Clock:** '+mmss(7200))
            else:
                c2.markdown('**Black Clock:** '+str(moves['RemTime Black'].fillna(0).apply(mmss)[int((ply-1)/2)-1]))
            c2.markdown('**White Clock:** '+str(moves['RemTime White'].fillna(0).apply(mmss)[int((ply-1)/2)]))




    st.subheader(' ')

    st.markdown('#### White and Black clock times')
    st.write('The time control for each game is 120 minutes for the first 40 moves, followed by 60 minutes\
     for the next 20 moves and then 15 minutes for the rest of the game with an increment of 30 seconds per move starting from move 61. ')
    fig, ax = plt.subplots()
    ax.set_facecolor('lightgray')

    time.plot(figsize=(14,8),ax=ax, color=['w','k'], linewidth=3)
    mo = time.index.shape[0]
    ticks = range(4,mo,5)
    ax.set_xticks([0]+[k for k in ticks])
    ax.set_xticklabels([1]+[k+1 for k in ticks], fontsize=12)

    ax.set_yticks([7200,5400,3600,1800,900,0,-900,-1800,-3600,-5400,-7200]) 
    ax.set_yticklabels(['2h','1h30','1h','30m','15m','0','15m','30m','1h','1h30','2h'], fontsize=14)
    ax.axhline(y = 0, color = 'gray', linestyle = '-')
    ax.grid(linewidth=0.3)
    ax.set_ylabel('Time Remaining', fontsize=14)
    ax.set_xlabel('Move Number', fontsize=14)
    ax.legend([white,black],facecolor="darkgray", fontsize=14)

    titulo = white + ' vs ' + black + ': ' + result
    ax.set_title(titulo, fontsize=16)
    ax.set_xlim(left=0, right=mo-1)
    st.pyplot(fig)


    st.markdown('#### Game Evaluation')
    st.write('The game evaluation is a computer engine assessment of the current position.\
    It is shown in terms of white perspective, i.e, a positive score means white is better and a negative score means a black is better. The score is in terms of \
    pawns, so a +0.5 score means that white has roughly half a pawn worth of advantage.')
    fig2, ax2 = plt.subplots()

    ax2.axhspan(-1, 1, facecolor='black', alpha=0.125)
    ax2.axhspan(1, 3, facecolor='black', alpha=0.05)
    ax2.axhspan(-3, -1, facecolor='black', alpha=0.35)
    ax2.axhspan(-3, -50, facecolor='black', alpha=0.5)
    ax2.axhspan(3, 50, facecolor='white', alpha=0.6)


    mo = evaluation_ply.index.shape[0]
    evaluation_ply.plot(figsize=(14,8), ax=ax2, color='darkblue', linewidth=3)
    ax2.grid(linewidth=0, color='black')

    ticks = range(9,mo,10)
    ax2.set_xticks([0]+[k for k in ticks])
    ax2.set_xticklabels([1]+[k+1 for k in ticks], fontsize=12)
    ax2.set_ylabel('Game Evaluation (white perspective)', fontsize=14)
    ax2.set_xlabel('Half-Move Number', fontsize=14)
    ax2.legend(['Game Evaluation'], facecolor="lightgray", fontsize=14)
    ax2.set_xlim(left=0, right=mo-1)

    if (evaluation_ply.max()>=10):
        ticks = [-2, 0, 2, 5, 10]
        ax2.set_ylim(-2,10)
    elif (evaluation_ply.max()>=5):
        ticks = [-6,-4,-2, 0, 2, 4, 6]
        ax2.set_ylim(-6,6)
    elif (evaluation_ply.min()<=-10):
        ticks = [-10, -5, -2, 0, 2]
        ax2.set_ylim(-10,2)
    elif (evaluation_ply.min()<=-5):
        ticks = [-6, -4, -2, 0, 2,4,6]
        ax2.set_ylim(-6,6)
    elif (evaluation_ply.max()>=2):
        ticks = [-4,-2, -1, 0, 1, 2, 4]
        ax2.set_ylim(-4,4)
    elif (evaluation_ply.min()<=-2):
        ticks = [-4, -2, -1, 0, 1, 2,4]
        ax2.set_ylim(-4,4)
    else:
        ticks = [-2, -1, 0, 1, 2] 
        ax2.set_ylim(-2,2)
        print(ticks)
    ax2.set_yticks(ticks)
    ax2.set_yticklabels(ticks, fontsize=14)

    titulo = white + ' vs ' + black + ': ' + result
    ax2.set_title(titulo, fontsize=16)
    ax2.axhline(y = 0, color = 'gray', linestyle = '-')
    st.pyplot(fig2)

    move_stat_white = moves.groupby('Piece-Action White')['Time White'].agg(['mean', 'count','min','max']).sort_values(by=['count','mean'], ascending=[False,False])
    move_stat_black = moves.groupby('Piece-Action Black')['Time Black'].agg(['mean', 'count','min','max']).sort_values(by=['count','mean'], ascending=[False,False])


    move_stat_white['avg time'] = move_stat_white['mean'].apply(mmss)
    move_stat_white['min'] = move_stat_white['min'].apply(mmss)
    move_stat_white['max'] = move_stat_white['max'].apply(mmss)

    move_stat_black['avg time'] = move_stat_black['mean'].apply(mmss)
    move_stat_black['min'] = move_stat_black['min'].apply(mmss)
    move_stat_black['max'] = move_stat_black['max'].apply(mmss)

    st.markdown('#### Thinking time and Piece-Action analysis')
    st.write('A breakdown of how many times the players moved each of their pieces, what kind of action was taken and the amount of time spent.')
    c1, c2 = st.columns(2)
    c1.markdown('**'+white+'**')
    c1.write(move_stat_white[['count', 'avg time', 'max']])
    c2.markdown('**'+black+'**')
    c2.write(move_stat_black[['count', 'avg time', 'max']])

st.caption('PGN file used here were download from lichess.org at https://lichess.org/api/broadcast/kAvAGI7N.pgn and annotated by https://lichess.org/@/loepare')