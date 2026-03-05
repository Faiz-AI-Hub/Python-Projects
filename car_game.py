import os
import sys
import msvcrt
import random
import time
from ctypes import windll

# Constants
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 26
WIN_WIDTH = 70

# Enable ANSI escape sequences on Windows
kernel32 = windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Game variables
enemyY = [0, 0, 0]
enemyX = [0, 0, 0]
enemyFlag = [False, False, False]
car = [
    [' ', '±', '±', ' '],
    ['±', '±', '±', '±'],
    [' ', '±', '±', ' '],
    ['±', '±', '±', '±']
]

carPos = WIN_WIDTH // 2
score = 0

def gotoxy(x, y):
    """Move cursor to position (x, y)"""
    print(f"\033[{y+1};{x+1}H", end='')

def setcursor(visible):
    """Set cursor visibility"""
    if visible:
        print("\033[?25h", end='')
    else:
        print("\033[?25l", end='')

def drawBorder():
    """Draw game border"""
    for i in range(SCREEN_HEIGHT):
        for j in range(17):
            gotoxy(0 + j, i)
            print("±", end='', flush=True)
            gotoxy(WIN_WIDTH - j, i)
            print("±", end='', flush=True)
    for i in range(SCREEN_HEIGHT):
        gotoxy(SCREEN_WIDTH, i)
        print("±", end='', flush=True)

def genEnemy(ind):
    """Generate enemy position"""
    enemyX[ind] = 17 + random.randint(0, 32)

def drawEnemy(ind):
    """Draw enemy car"""
    if enemyFlag[ind]:
        gotoxy(enemyX[ind], enemyY[ind])
        print("****", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 1)
        print(" ** ", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 2)
        print("****", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 3)
        print(" ** ", end='', flush=True)

def eraseEnemy(ind):
    """Erase enemy car"""
    if enemyFlag[ind]:
        gotoxy(enemyX[ind], enemyY[ind])
        print("    ", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 1)
        print("    ", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 2)
        print("    ", end='', flush=True)
        gotoxy(enemyX[ind], enemyY[ind] + 3)
        print("    ", end='', flush=True)

def resetEnemy(ind):
    """Reset enemy position"""
    eraseEnemy(ind)
    enemyY[ind] = 1
    genEnemy(ind)

def drawCar():
    """Draw player car"""
    for i in range(4):
        for j in range(4):
            gotoxy(j + carPos, i + 22)
            print(car[i][j], end='')

def eraseCar():
    """Erase player car"""
    for i in range(4):
        for j in range(4):
            gotoxy(j + carPos, i + 22)
            print(" ", end='', flush=True)

def collision():
    """Check for collision"""
    for i in range(2):
        if enemyFlag[i] and enemyY[i] + 4 >= 23:
            if enemyX[i] + 4 - carPos >= 0 and enemyX[i] + 4 - carPos < 9:
                return 1
    return 0

def gameover():
    """Display game over screen"""
    os.system('cls')
    print()
    print("\t\t--------------------------")
    print("\t\t-------- Game Over -------")
    print("\t\t--------------------------")
    print()
    print("\t\tPress any key to go back to menu.")
    msvcrt.getch()

def updateScore():
    """Update score display"""
    gotoxy(WIN_WIDTH + 7, 5)
    print(f"Score: {score}", end='', flush=True)

def instructions():
    """Display instructions"""
    os.system('cls')
    print("Instructions")
    print("----------------")
    print(" Avoid Cars by moving left or right. ")
    print("\n Press 'a' to move left")
    print(" Press 'd' to move right")
    print(" Press 'escape' to exit")
    print("\n\nPress any key to go back to menu")
    msvcrt.getch()

def kbhit():
    """Check if key is pressed (non-blocking)"""
    return msvcrt.kbhit()

def getch():
    """Get pressed key"""
    try:
        key = msvcrt.getch()
        if key == b'\xe0':  # Extended key code
            key = msvcrt.getch()
            return key
        return key.decode('utf-8').lower()
    except:
        return ''

def play():
    """Main game loop"""
    global carPos, score, enemyFlag, enemyY
    
    carPos = -1 + WIN_WIDTH // 2
    score = 0
    enemyFlag[0] = True
    enemyFlag[1] = False
    enemyY[0] = 1
    enemyY[1] = 1
    
    os.system('cls')
    drawBorder()
    updateScore()
    genEnemy(0)
    genEnemy(1)
    
    gotoxy(WIN_WIDTH + 7, 2)
    print("Car Game", end='', flush=True)
    gotoxy(WIN_WIDTH + 6, 4)
    print("----------", end='', flush=True)
    gotoxy(WIN_WIDTH + 6, 6)
    print("----------", end='', flush=True)
    gotoxy(WIN_WIDTH + 7, 12)
    print("Control ", end='', flush=True)
    gotoxy(WIN_WIDTH + 7, 13)
    print("-------- ", end='', flush=True)
    gotoxy(WIN_WIDTH + 2, 14)
    print(" A Key - Left", end='', flush=True)
    gotoxy(WIN_WIDTH + 2, 15)
    print(" D Key - Right", end='', flush=True)
    
    gotoxy(18, 5)
    print("Press any key to start", end='', flush=True)
    msvcrt.getch()
    gotoxy(18, 5)
    print("                      ", end='', flush=True)
    
    while True:
        if kbhit():
            ch = getch()
            if isinstance(ch, bytes):
                if ch == b'\x1b':  # Escape key
                    break
            elif ch == 'a':
                if carPos > 18:
                    carPos -= 4
            elif ch == 'd':
                if carPos < 50:
                    carPos += 4
            elif ch == '\x1b':  # Escape key (string)
                break
        
        drawCar()
        drawEnemy(0)
        drawEnemy(1)
        
        if collision() == 1:
            gameover()
            return
        
        time.sleep(0.05)
        eraseCar()
        eraseEnemy(0)
        eraseEnemy(1)
        
        if enemyY[0] == 10:
            if not enemyFlag[1]:
                enemyFlag[1] = True
        
        if enemyFlag[0]:
            enemyY[0] += 1
        
        if enemyFlag[1]:
            enemyY[1] += 1
        
        if enemyY[0] > SCREEN_HEIGHT - 4:
            resetEnemy(0)
            score += 1
            updateScore()
        
        if enemyY[1] > SCREEN_HEIGHT - 4:
            resetEnemy(1)
            score += 1
            updateScore()

def main():
    """Main menu"""
    setcursor(False)
    random.seed(time.time())
    
    while True:
        os.system('cls')
        gotoxy(10, 5)
        print(" -------------------------- ", end='', flush=True)
        gotoxy(10, 6)
        print(" |  Car Game by AZFAR       | ", end='', flush=True)
        gotoxy(10, 7)
        print(" --------------------------", end='', flush=True)
        gotoxy(10, 9)
        print("1. Start Game", end='', flush=True)
        gotoxy(10, 10)
        print("2. Instructions", end='', flush=True)
        gotoxy(10, 11)
        print("3. Quit", end='', flush=True)
        gotoxy(10, 13)
        print("Select option: ", end='', flush=True)
        
        op = msvcrt.getch().decode('utf-8')
        
        if op == '1':
            play()
        elif op == '2':
            instructions()
        elif op == '3':
            sys.exit(0)

if __name__ == "__main__":
    main()