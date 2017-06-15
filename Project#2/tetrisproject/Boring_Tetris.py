# 원본 
# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, os
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 420
WINDOWHEIGHT = 500
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = WHITE
TEXTCOLOR = BLACK
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)


TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5


S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}



def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONT2, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BASICFONT2 = pygame.font.Font('freesansbold.ttf', 30)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    pygame.display.set_caption('테트리스') #상태표시줄의 프로그램 명
    background_image = pygame.image.load("back.jpg").convert() #배경 이미지 설정
    pygame.mixer.music.load('Music/title.mid') 
    pygame.mixer.music.play(-1,0.0) # title.mid 배경음을 0.0초부터 반복해서 재생
    DISPLAYSURF.blit(background_image, [0, -50]) #배경 이미지가 나타나는 위치를 설정
    showTextScreen('Boring Tetris') # Boring Tetris라는 문자와 함께 textscreen을 출력

    while True:

        runGame() #게임 실행
        pygame.mixer.music.stop() #게임이 종료되면 재생중이던 음악을 정지
        pygame.mixer.music.load('Music/gameover.mp3') 
        pygame.mixer.music.play(1,0.0) # gameover.mp3 배경음을 0.0초부터 1번만 재생
        showTextScreen('Game Over') # Game Over라는 문자와 함께 textscreen을 출력

def runGame(): #메인 게임 함수
    background_image = pygame.image.load("back.jpg").convert()

    board = getBlankBoard() #보드(블럭이 쌓이는 곳)을 초기화
    lastMoveDownTime = time.time()  
    lastMoveSidewaysTime = time.time() 
    lastFallTime = time.time()         # 마지막으로 블럭이 움직인 시간을 설정
    movingDown = False #아래로 움직이는지 판단 기본은 false
    movingLeft = False #왼쪽으로 움직이는지 판단 기본은 false
    movingRight = False#오른쪽으로 움직이는지 판단 기본은 false
    tempscore = 0 #임시 점수, 4줄을 동시에 지웟을때 점수를 추가로 주기 위해 만듬
    score = 0 #실제 점수. 화면에 표시되고 레벨을 결정하는 점수
    level, fallFreq = calculateLevelAndFallFreq(score) #레벨과 블럭이 떨어지는 속도는 실제 점수를 레벨/속도 생성 함수로 결정
    pygame.mixer.music.load('Music/game.mid')
    pygame.mixer.music.play(-1,0.0) # game.mid 배경음을 0.0초부터 반복해서 재생
    savedPiece = None # 블럭 저장소. 처음은 비어있음
    tempPiece = None # 저장된 블럭을 교체할때 사용되는 임시 저장소
    saveOnce = False # 블럭 하나는 한번만 저장하도록 만드는 판단
    fallingPiece = getNewPiece() # 떨어지는 블럭을 생성
    nextPiece = getNewPiece() # 다음 블럭을 생성

    while True: #게임이 실행됨
        if fallingPiece == None: 
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()# 떨어지는 블럭이 없으면 다음 블럭을 떨어뜨리고 다음 블럭을 생성

            if not isValidPosition(board, fallingPiece): #블럭이 보드를 벗어나면 게임을 종료 
                return

        checkForQuit() #프로그램을  종료하는지 판단하는 함수. 게임 실행중 언제라도 실행가능.
        for event in pygame.event.get():
            if event.type == KEYUP: #해당 키가 눌렸다가 '떼질때' 실행
                if (event.key == K_LEFT):
                    movingLeft = False
                elif (event.key == K_RIGHT):
                    movingRight = False
                elif (event.key == K_DOWN):
                    movingDown = False        # 이상 3개는 왼쪽, 오른쪽, 아래 키를 떼면 그 방향으로 움직이는걸 중단
                elif event.key == K_p:        
                    showTextScreen('Paused')  
                    pygame.mixer.music.load('Music/game.mid') 
                    pygame.mixer.music.play(-1,0.0) # P가 떼어질때 Paused라는 문자와 함께 textscreen을 표시하고 그 textscreen이 종료되면 game.mid 배경음을 재생

            elif event.type == KEYDOWN: #해당 키가 눌렸을때 실행
                if (event.key == K_LEFT) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time() #왼쪽 키가 눌리면서 블럭의 위치가 보드 왼쪽 벽에 안닿으면 블럭을 왼쪽으로 한칸씩 이동.

                elif (event.key == K_RIGHT) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time() #오른쪽 키가 눌리면서 블럭의 위치가 보드 오른쪽 벽에 안닿으면 블럭을 오른쪽으로 한칸씩 이동.

                elif (event.key == K_DOWN): 
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time() #아래 키가 눌리면 떨어지는 속도에 추가로 블럭을 아래로 한칸씩 이동.

                elif (event.key == K_UP):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    effect = pygame.mixer.Sound('Sound/swap.wav')
                    effect.set_volume(.3)
                    effect.play() #위 키가 눌리면 블럭을 회전시키고 swap.wav 효과음을 재생. 만약 회전했을때 블럭이 벽을 뚫는다면 회전하지 않음.
                        
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1 #스페이스 바가 눌리면, 좌,우,하 입력을 모두 무시하고 바닥 혹은 다른 블럭에 닿을때까지 아래로 이동.

                elif event.key == K_s:
                    if saveOnce == False:
                        effect = pygame.mixer.Sound('Sound/save.wav')
                        effect.set_volume(.3)
                        effect.play() # S키가 눌렸을때, saveOnce가 False면 save.wav 효과음을 재생
                    else:
                        effect = pygame.mixer.Sound('Sound/aldsave.wav')
                        effect.set_volume(.3)
                        effect.play() # S키가 눌렸을때, saveOnce가 True면 aldsave.wav 효과음을 재생
                    if savedPiece == None and saveOnce == False:
                        savedPiece = fallingPiece
                        fallingPiece = None
                        saveOnce = True
                        break # S키가 눌렸을때, 저장된 블럭이 없고 SaveOnce가 False면 떨어지는 블럭을 저장.
                    elif savedPiece != None and saveOnce == False:
                        tempPiece = savedPiece
                        savedPiece = fallingPiece
                        fallingPiece = tempPiece
                        saveOnce = True
                        tempPiece = None
                        fallingPiece['y'] = -2
                        fallingPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
                        level, fallFreq = calculateLevelAndFallFreq(score)
                        break #S키가 늘렸을때, 저장된 블럭이 있지만 SaveOnce가 False면 떨어지는 블럭과 저장된 블럭을 교환하고 블럭을 맨 위에서 다시 떨어뜨림.
   
    
        if time.time() - lastFallTime > fallFreq: # 블럭이 떨어짐
            if not isValidPosition(board, fallingPiece, adjY=1): # 블럭이 바닥이나 다른 블럭과 닿으면
                addToBoard(board, fallingPiece) #이미지로만 보여주던 떨어지던 블럭을 실제 보드 위치에 설정
                tempscore = removeCompleteLines(board)*10 #보드를 확인해서 완성된 줄이 있으면 제거하고 줄 하나당 임시 점수 10점을 부여
                if tempscore == 0:
                    effect = pygame.mixer.Sound('Sound/down.wav')
                    effect.set_volume(.3)
                    effect.play()
                    score += 5 #블럭이 떨어졌지만 완성된 줄이 없으면 down.wav 효과음을 재생하고 실제 점수 5점 추가
                elif tempscore == 10:
                    effect = pygame.mixer.Sound('Sound/1line.wav')
                    effect.set_volume(.3)
                    effect.play()
                    score += tempscore
                    tempscore = 0 
                elif tempscore == 20:
                    effect = pygame.mixer.Sound('Sound/2line.wav')
                    effect.set_volume(.3)
                    effect.play()
                    score += tempscore
                    tempscore = 0
                elif tempscore == 30:
                    effect = pygame.mixer.Sound('Sound/3line.wav')
                    effect.set_volume(.3)
                    effect.play()
                    score += tempscore
                    tempscore = 0       #완성된 줄이 1~3 줄이면, 완성된 줄에 따른 효과음 1line.wav, 2line.wav, 3line.wav를 각각 재생하고 실제 점수를 임시 점수만큼 추가. 그 후 임시 점수 초기화.
                elif tempscore == 40:
                    score += 100
                    tempscore = 0
                    effect = pygame.mixer.Sound('Sound/tetris.wav')
                    effect.set_volume(.3)
                    effect.play()
                    showTetristext()
                    pygame.time.delay(500)  #완성된 줄이 4줄이면, tetris.wav 효과음을 재생하고 실제 점수를 100점 추가. 그 후 임시 점수를 초기화 한뒤 Tetistext를 띄움.               
                level, fallFreq = calculateLevelAndFallFreq(score) # 현재 실제 점수를 바탕으로 레벨과 떨어지는 속도를 결정
                saveOnce = False # 블럭이 떨어지면, 다음 블럭이 저장소와 연동할 수 있게 saveOnce를 초기화.
                fallingPiece = None # 새 블럭을 요청
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time() # 블럭이 바닥이나 쌓은 블럭에 닿기 전까지 계속 떨어짐
        
        DISPLAYSURF.fill(BGCOLOR) 
        DISPLAYSURF.blit(background_image, [-200, -50]) #배경색을 채우고 그 위에 배경이미지를 출력
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        drawSavedPiece(savedPiece) # 보드(블럭이 떨어지고 쌓이는 부분), 상태(레벨과 점수), 다음 블럭, 저장된 블럭을 화면에 그림
        if fallingPiece != None:
            drawPiece(fallingPiece) #떨어지는 블럭이 있으면 화면에 떨어지는 블럭을 그림.

        pygame.display.update() # 화면을 계속해서 업데이트. 이게 없으면 화면은 정지해서 알 수 없음
        FPSCLOCK.tick(FPS) # FPS 설정

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect() #문자 상태를 결정하는 함수, 내용, 폰트정류, 글씨색을 정함.

def terminate():
    pygame.quit()
    sys.exit() # 프로그램 종료를 위한 함수, pygame을 종료하면서 시스템적으로 실행중인 프로그램을 종료시키는 요청도 같이 한다.

def checkForKeyPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None #자판 입력을 확인하는 함수, 아무 키를 누르는것과 떼는것을 모두 감지한다. 그와 함께 게임을 종료하는 판정도 다시 해본다.

def showTextScreen(text):
    if text == 'Paused':
        pygame.mixer.music.stop()
        effect = pygame.mixer.Sound('Sound/pause.wav')
        effect.set_volume(.3)
        effect.play()
    
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()  # textscreen을 나타내는 함수, text와 함께 Press a key to play를 표시하고 아무 자판이 입력될때까지 화면을 정지시킨다.
                         # 이 함수에 입력받은 text가 Paused라면, 재생중인 배경음을 일단 멈추고 pause.wav 효과음을 재생한다.
                         # 또한 입력받은 text는 Press a key to play보다 위에, 큰 글씨로 표시된다.

def showTetristext():
    titleKeySurf, titleKeyRect = makeTextObjs('Tetris!', BASICFONT2, TEXTSHADOWCOLOR)
    titleKeyRect.center = (int(WINDOWWIDTH / 2)+3, 43)
    DISPLAYSURF.blit(titleKeySurf, titleKeyRect)

    titleKeySurf, titleKeyRect = makeTextObjs('Tetris!', BASICFONT2, RED)
    titleKeyRect.center = (int(WINDOWWIDTH / 2), 40)
    DISPLAYSURF.blit(titleKeySurf, titleKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()  # Tetristext를 나나태는 함수. 화면 상단에 Tetris! 라는 문자를 표시한다. 원래는 일정 시간동안 나타났다가 사라지게 하고 싶었지만
                         # 알아본 방식으로 동작하지 않아 자판을 입력하지 않으면 일시정지하는 위의 showTextscreen 함수를 이용했다.

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) #게임을 종료하는 함수. 윈도우 창의 종료 버튼을 누르거나 ESC 자판을 입력하면 프로그램 종료 함수를 실행한다.

def calculateLevelAndFallFreq(score):
    level = int(score / 150) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq  # 게임 레벨과 떨어지는 속도를 조절하는 함수, 실제 점수가 150의 배수를 넘을때마다 레벨이 오르고, 레벨이 오를수록
                            # 블럭이 떨어지는 속도가 0.02 프레임씩 빨라진다.

def getNewPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece # 새 블럭을 만들어내는 함수. 정해진 블럭들 중 하나를 무작위로 선택하고 그 모양에 맞는 블럭을 만들어낸다. 그 색은 또 무작위로 결정된다.

def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']
                # 보드에 블럭을 더하는 함수. 블럭이 바닥 등에 닿게 전까지는 블럭은 정해진 위치가 없이 겉으로만 보드 위에 존재하고 실제로 보드에는 없다.
                # 이 함수를 통해서 실제로 입력된 블럭을 보드의 현재 위치에 더해서 블럭이 쌓이는것을 만들어낸다. 

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board # 보드를 비우는 함수. 보드에 존재하는 블럭을 모두 없앤다.

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT # 보드가 있는지 판단하는 함수. 보드 넓이와 높이값만큼 보드를 만들어낸다.

def isValidPosition(board, piece, adjX=0, adjY=0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True # 블럭이 제대로된 위치에 존재하는지 판단하는 함수. 블럭이 보드에서 존재하는 위치가 제대로 보드 내에 있는지 판단한다.

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True # 줄이 완성되었는지 판단하는 함수. 

def removeCompleteLines(board):
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1
    return numLinesRemoved # 완성된 줄을 지우는 함수

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE)) 

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))

def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawStatus(score, level):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 405, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 405, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

    pauseSurf = BASICFONT.render('Press P to pause game', True, TEXTCOLOR)
    pauseRect = pauseSurf.get_rect()
    pauseRect.center = (WINDOWWIDTH/2, 10)
    DISPLAYSURF.blit(pauseSurf, pauseRect) # 상태를 표시하는 함수. 현재 점수와 레벨, P를 누르면 일시정지가 가능하다는 안내문구를 출력한다.


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:

        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
                    # 블럭을 그리는 함수, 데이터상으로 존재하는 함수를 눈에 보이게 그린다.

def drawNextPiece(piece):
    nextSurf = BASICFONT.render('Next', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 85, 20)
    DISPLAYSURF.blit(nextSurf, nextRect)
    drawPiece(piece, pixelx=WINDOWWIDTH-100, pixely=40) # 다음 블럭을 그리는 함수. 다음 블럭을 화면에 알려준다.

def drawSavedPiece(piece):
    savedSurf = BASICFONT.render('Saved (S)', True, TEXTCOLOR)
    savedRect = savedSurf.get_rect()
    savedRect.topleft = (WINDOWWIDTH - 85, 130)
    DISPLAYSURF.blit(savedSurf, savedRect)
    if piece != None:
        drawPiece(piece, pixelx=WINDOWWIDTH-100, pixely=150) #저장된 블럭을 그리는 함수. 저장된 블럭이 있으면 그 블럭을 화면에 알려준다.

if __name__ == '__main__':
    main()
