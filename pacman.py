import pygame
import random
import math

# Initialize Pygame
try:
    pygame.init()
except Exception as e:
    print(f"Error initializing pygame: {e}")
    exit(1)

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
CELL_SIZE = 25
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - 100) // CELL_SIZE  # Leave space for score

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Create window
try:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pac-Man Game")
    clock = pygame.time.Clock()
except Exception as e:
    print(f"Error creating game window: {e}")
    pygame.quit()
    exit(1)

# Maze layout (1 = wall, 0 = path, 2 = pellet, 3 = power pellet)
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,3,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,1,1,1,1,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [0,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],
    [1,1,1,1,1,1,2,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1],
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,2,1,1,1,1,2,1,1,1,1,1,1,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,2,1],
    [1,3,2,2,1,1,2,2,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,1,1,2,2,3,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1],
    [1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up
        self.next_direction = 0
        self.speed = 0.15
        self.angle = 0
        self.mouth_open = True
        self.mouth_timer = 0
        
    def update(self):
        # Try to change direction if requested
        if self.can_move(self.next_direction):
            self.direction = self.next_direction
        
        # Move in current direction
        if self.can_move(self.direction):
            if self.direction == 0:  # Right
                self.x += self.speed
            elif self.direction == 1:  # Down
                self.y += self.speed
            elif self.direction == 2:  # Left
                self.x -= self.speed
            elif self.direction == 3:  # Up
                self.y -= self.speed
        
        # Wrap around screen edges
        if self.x < 0:
            self.x = GRID_WIDTH - 1
        elif self.x >= GRID_WIDTH:
            self.x = 0
        
        # Animate mouth
        self.mouth_timer += 1
        if self.mouth_timer > 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
    
    def can_move(self, direction):
        # Check if can move in given direction
        test_x, test_y = self.x, self.y
        
        if direction == 0:  # Right
            test_x += self.speed + 0.5
        elif direction == 1:  # Down
            test_y += self.speed + 0.5
        elif direction == 2:  # Left
            test_x -= self.speed + 0.5
        elif direction == 3:  # Up
            test_y -= self.speed + 0.5
        
        grid_x = int(test_x)
        grid_y = int(test_y)
        
        if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT:
            return True  # Allow wrapping
        
        if maze[grid_y][grid_x] == 1:
            return False
        return True
    
    def draw(self):
        center_x = int(self.x * CELL_SIZE + CELL_SIZE // 2)
        center_y = int(self.y * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        
        if self.mouth_open:
            # Calculate mouth angle based on direction
            # Direction: 0=Right, 1=Down, 2=Left, 3=Up
            mouth_angle = 45  # Mouth opening angle (degrees)
            
            if self.direction == 0:  # Right
                start_angle = -mouth_angle
                end_angle = mouth_angle
            elif self.direction == 1:  # Down
                start_angle = 90 - mouth_angle
                end_angle = 90 + mouth_angle
            elif self.direction == 2:  # Left
                start_angle = 180 - mouth_angle
                end_angle = 180 + mouth_angle
            elif self.direction == 3:  # Up
                start_angle = 270 - mouth_angle
                end_angle = 270 + mouth_angle
            else:
                start_angle = -mouth_angle
                end_angle = mouth_angle
            
            # Draw full circle first
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
            
            # Draw mouth (black triangle/polygon)
            points = [(center_x, center_y)]
            # Generate points along the arc
            for angle in range(int(start_angle), int(end_angle) + 1, 2):
                rad = math.radians(angle)
                px = center_x + radius * math.cos(rad)
                py = center_y - radius * math.sin(rad)
                points.append((int(px), int(py)))
            
            # Ensure we have enough points
            if len(points) >= 3:
                pygame.draw.polygon(screen, BLACK, points)
        else:
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
    
    def get_grid_pos(self):
        return int(self.x), int(self.y)

class Ghost:
    def __init__(self, x, y, color):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.randint(0, 3)
        self.speed = 0.1
        self.scared = False
        self.scared_timer = 0
        
    def update(self):
        # Update scared timer
        if self.scared:
            self.scared_timer -= 1
            if self.scared_timer <= 0:
                self.scared = False
        
        # Simple AI: try to continue in current direction, or pick random if blocked
        if random.random() < 0.05 or not self.can_move(self.direction):
            # Try to pick a new direction
            possible_dirs = []
            for d in range(4):
                if self.can_move(d):
                    possible_dirs.append(d)
            if possible_dirs:
                self.direction = random.choice(possible_dirs)
        
        # Move
        if self.can_move(self.direction):
            if self.direction == 0:  # Right
                self.x += self.speed
            elif self.direction == 1:  # Down
                self.y += self.speed
            elif self.direction == 2:  # Left
                self.x -= self.speed
            elif self.direction == 3:  # Up
                self.y -= self.speed
        
        # Wrap around
        if self.x < 0:
            self.x = GRID_WIDTH - 1
        elif self.x >= GRID_WIDTH:
            self.x = 0
    
    def can_move(self, direction):
        test_x, test_y = self.x, self.y
        
        if direction == 0:
            test_x += self.speed + 0.5
        elif direction == 1:
            test_y += self.speed + 0.5
        elif direction == 2:
            test_x -= self.speed + 0.5
        elif direction == 3:
            test_y -= self.speed + 0.5
        
        grid_x = int(test_x)
        grid_y = int(test_y)
        
        if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT:
            return True
        
        if maze[grid_y][grid_x] == 1:
            return False
        return True
    
    def draw(self):
        center_x = int(self.x * CELL_SIZE + CELL_SIZE // 2)
        center_y = int(self.y * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        
        color = (0, 0, 255) if self.scared else self.color
        
        # Draw ghost body (rounded rectangle)
        pygame.draw.circle(screen, color, (center_x, center_y - radius // 2), radius)
        pygame.draw.rect(screen, color, (center_x - radius, center_y - radius // 2, radius * 2, radius * 2))
        
        # Draw wavy bottom
        wave_points = []
        for i in range(5):
            x = center_x - radius + (i * radius * 2 // 4)
            y = center_y + radius // 2 + (5 if i % 2 == 0 else 0)
            wave_points.append((x, y))
        pygame.draw.polygon(screen, color, wave_points + [(center_x + radius, center_y + radius // 2)])
        
        # Draw eyes
        if not self.scared:
            eye_size = 3
            pygame.draw.circle(screen, WHITE, (center_x - radius // 2, center_y - radius // 2), eye_size)
            pygame.draw.circle(screen, WHITE, (center_x + radius // 2, center_y - radius // 2), eye_size)
            pygame.draw.circle(screen, BLACK, (center_x - radius // 2, center_y - radius // 2), eye_size // 2)
            pygame.draw.circle(screen, BLACK, (center_x + radius // 2, center_y - radius // 2), eye_size // 2)
        else:
            # Scared face
            pygame.draw.circle(screen, WHITE, (center_x - radius // 2, center_y - radius // 2), 4)
            pygame.draw.circle(screen, WHITE, (center_x + radius // 2, center_y - radius // 2), 4)
    
    def get_grid_pos(self):
        return int(self.x), int(self.y)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.scared = False

def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, rect)
            elif maze[y][x] == 2:  # Pellet
                pygame.draw.circle(screen, YELLOW, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 2)
            elif maze[y][x] == 3:  # Power pellet
                pygame.draw.circle(screen, YELLOW, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 6)

def main():
    # Initialize game objects
    pacman = PacMan(16, 23)
    ghosts = [
        Ghost(15, 14, RED),
        Ghost(16, 14, PINK),
        Ghost(15, 15, CYAN),
        Ghost(16, 15, ORANGE),
    ]
    
    score = 0
    game_over = False
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.next_direction = 0
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = 1
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = 2
                elif event.key == pygame.K_UP:
                    pacman.next_direction = 3
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    pacman = PacMan(16, 23)
                    ghosts = [
                        Ghost(15, 14, RED),
                        Ghost(16, 14, PINK),
                        Ghost(15, 15, CYAN),
                        Ghost(16, 15, ORANGE),
                    ]
                    score = 0
                    game_over = False
                    # Reset maze pellets
                    for y in range(len(maze)):
                        for x in range(len(maze[y])):
                            if maze[y][x] == 0:
                                maze[y][x] = 2
        
        if not game_over:
            # Update game objects
            pacman.update()
            
            # Check pellet collection
            px, py = pacman.get_grid_pos()
            if 0 <= py < len(maze) and 0 <= px < len(maze[py]):
                if maze[py][px] == 2:  # Regular pellet
                    maze[py][px] = 0
                    score += 10
                elif maze[py][px] == 3:  # Power pellet
                    maze[py][px] = 0
                    score += 50
                    # Make ghosts scared
                    for ghost in ghosts:
                        ghost.scared = True
                        ghost.scared_timer = 300
            
            # Update ghosts
            for ghost in ghosts:
                ghost.update()
                
                # Check collision with pacman
                gx, gy = ghost.get_grid_pos()
                if abs(pacman.x - ghost.x) < 0.8 and abs(pacman.y - ghost.y) < 0.8:
                    if ghost.scared:
                        # Eat ghost
                        ghost.reset()
                        score += 200
                    else:
                        # Game over
                        game_over = True
        
        # Draw everything
        screen.fill(BLACK)
        draw_maze()
        
        if not game_over:
            pacman.draw()
            for ghost in ghosts:
                ghost.draw()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, WINDOW_HEIGHT - 80))
        
        # Draw instructions
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            screen.blit(game_over_text, text_rect)
        else:
            instructions = font.render("Use Arrow Keys to Move", True, WHITE)
            screen.blit(instructions, (10, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

