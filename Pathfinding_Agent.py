class PathfindingGUI:
    def __init__(self):
        pygame.init()
        
        self.rows = 10
        self.cols = 10
        self.cell_size = 40
        
        self.get_grid_size_from_user()
        self.cols = self.rows
        
        self.grid_width = self.cols * self.cell_size
        self.grid_height = self.rows * self.cell_size
        self.metrics_height = 180
        self.control_height = 150
        self.width = max(self.grid_width, 700)
        self.height = self.grid_height + self.metrics_height + self.control_height
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.LIGHT_BLUE = (173, 216, 230)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dynamic Pathfinding Agent")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.big_font = pygame.font.Font(None, 32)
        
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.start = None
        self.goal = None
        
        self.algorithm = "A*"
        self.heuristic = "Manhattan"
        
        self.gbfs = GBFS()
        self.astar = Astar()
        self.current_path = None
        self.current_frontier = []
        self.current_visited = []
        
        self.nodes_visited = 0
        self.path_cost = 0
        self.execution_time = 0
        
        self.dynamic_mode = False
        self.agent_pos = None
        self.path_index = 0
        self.obstacle_prob = 0.02
        
        self.mode = "wall"  # wall, start, goal
        self.buttons = {}
        self.create_buttons()
        
        print("GUI initialized")
        print(f"Grid size: {self.rows}x{self.cols}")
        print("Click mode buttons then click on grid:")
        print("  Wall mode: Click to toggle walls")
        print("  Start mode: Click to set start")
        print("  Goal mode: Click to set goal")
    
    def get_grid_size_from_user(self):
        try:
            size = input("Enter grid size (5-20): ")
            size = int(size)
            if 5 <= size <= 20:
                self.rows = size
            else:
                print("Using default 10")
        except:
            print("Using default 10")
    
    def create_buttons(self):
        button_y = self.grid_height + self.metrics_height + 10
        button_width = 90
        button_height = 30
        margin = 5
        
        # Row 1: Mode selection
        self.buttons = {
            'Wall Mode': pygame.Rect(10, button_y, button_width, button_height),
            'Start Mode': pygame.Rect(10 + button_width + margin, button_y, button_width, button_height),
            'Goal Mode': pygame.Rect(10 + (button_width + margin) * 2, button_y, button_width, button_height),
        }
        
        # Row 2: Algorithms
        y2 = button_y + button_height + margin
        self.buttons['A*'] = pygame.Rect(10, y2, button_width, button_height)
        self.buttons['GBFS'] = pygame.Rect(10 + button_width + margin, y2, button_width, button_height)
        
        # Row 3: Heuristics
        y3 = y2 + button_height + margin
        self.buttons['Manhattan'] = pygame.Rect(10, y3, button_width, button_height)
        self.buttons['Euclidean'] = pygame.Rect(10 + button_width + margin, y3, button_width, button_height)
        
        # Row 4: Actions
        y4 = y3 + button_height + margin
        self.buttons['Random'] = pygame.Rect(10, y4, button_width, button_height)
        self.buttons['Clear'] = pygame.Rect(10 + button_width + margin, y4, button_width, button_height)
        self.buttons['Find Path'] = pygame.Rect(10 + (button_width + margin) * 2, y4, button_width, button_height)
        self.buttons['Dynamic'] = pygame.Rect(10 + (button_width + margin) * 3, y4, button_width, button_height)
    
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                if self.grid[row][col] == 1:
                    color = self.GRAY
                elif self.grid[row][col] == 2:
                    color = self.GREEN
                elif self.grid[row][col] == 3:
                    color = self.RED
                else:
                    pos = (row, col)
                    if self.current_path and pos in self.current_path:
                        color = self.YELLOW
                    elif pos in self.current_frontier:
                        color = self.ORANGE
                    elif pos in self.current_visited:
                        color = self.LIGHT_BLUE
                    else:
                        color = self.WHITE
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
    
    def draw_metrics(self):
        y = self.grid_height + 5
        
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, 
                        (0, self.grid_height, self.width, self.metrics_height))
        pygame.draw.line(self.screen, self.BLACK, (0, self.grid_height), 
                        (self.width, self.grid_height), 2)
        
        title = self.big_font.render("METRICS DASHBOARD", True, self.BLACK)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, y))
        
        col1_x = 20
        col2_x = self.width // 2 + 20
        
        mode_color = self.GREEN if self.mode == "start" else self.RED if self.mode == "goal" else self.BLACK
        mode_text = f"Mode: {self.mode.upper()}"
        
        metrics1 = [
            f"Algorithm: {self.algorithm}",
            f"Heuristic: {self.heuristic}",
            f"Grid Size: {self.rows}x{self.cols}",
            mode_text
        ]
        
        metrics2 = [
            f"Nodes Visited: {self.nodes_visited}",
            f"Path Cost: {self.path_cost}",
            f"Time: {self.execution_time:.2f} ms",
            f"Density: {int(self.obstacle_prob*100)}%"
        ]
        
        for i, text in enumerate(metrics1):
            text_surface = self.font.render(text, True, self.BLACK)
            self.screen.blit(text_surface, (col1_x, y + 30 + i * 25))
        
        for i, text in enumerate(metrics2):
            text_surface = self.font.render(text, True, self.BLACK)
            self.screen.blit(text_surface, (col2_x, y + 30 + i * 25))
    
    def draw_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for name, rect in self.buttons.items():
            # Highlight current mode
            if (name == 'Wall Mode' and self.mode == 'wall') or \
               (name == 'Start Mode' and self.mode == 'start') or \
               (name == 'Goal Mode' and self.mode == 'goal'):
                color = (100, 255, 100)  # Bright green for active mode
            elif rect.collidepoint(mouse_pos):
                color = (200, 200, 200)
            else:
                color = (150, 150, 150)
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 2)
            
            text = self.small_font.render(name, True, self.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def handle_click(self, pos, button):
        x, y = pos
        
        # Check button clicks
        for name, rect in self.buttons.items():
            if rect.collidepoint(x, y):
                self.handle_button_click(name)
                return
        
        # Check grid click
        if y < self.grid_height:
            col = x // self.cell_size
            row = y // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if self.mode == "wall":
                    if (row, col) != self.start and (row, col) != self.goal:
                        self.grid[row][col] = 1 - self.grid[row][col]
                        self.clear_search_results()
                elif self.mode == "start":
                    if self.grid[row][col] != 1:
                        if self.start:
                            self.grid[self.start[0]][self.start[1]] = 0
                        self.start = (row, col)
                        self.grid[row][col] = 2
                        self.clear_search_results()
                elif self.mode == "goal":
                    if self.grid[row][col] != 1:
                        if self.goal:
                            self.grid[self.goal[0]][self.goal[1]] = 0
                        self.goal = (row, col)
                        self.grid[row][col] = 3
                        self.clear_search_results()
    
    def handle_button_click(self, name):
        if name == "Wall Mode":
            self.mode = "wall"
        elif name == "Start Mode":
            self.mode = "start"
        elif name == "Goal Mode":
            self.mode = "goal"
        elif name == "A*":
            self.algorithm = "A*"
        elif name == "GBFS":
            self.algorithm = "GBFS"
        elif name == "Manhattan":
            self.heuristic = "Manhattan"
        elif name == "Euclidean":
            self.heuristic = "Euclidean"
        elif name == "Random":
            self.generate_random_map()
        elif name == "Clear":
            self.clear_grid()
        elif name == "Find Path":
            self.find_path()
        elif name == "Dynamic":
            self.toggle_dynamic_mode()
    
    def generate_random_map(self, density=0.3):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) != self.start and (row, col) != self.goal:
                    if random.random() < density:
                        self.grid[row][col] = 1
        
        self.clear_search_results()
    
    def clear_grid(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.start = None
        self.goal = None
        self.clear_search_results()
    
    def clear_search_results(self):
        self.current_path = None
        self.current_frontier = []
        self.current_visited = []
        self.nodes_visited = 0
        self.path_cost = 0
        self.execution_time = 0
    
    def find_path(self):
        if not self.start or not self.goal:
            return
        
        if self.heuristic == "Manhattan":
            h_func = manhattan_distance
        else:
            h_func = euclidean_distance
        
        start_time = time.time()
        
        if self.algorithm == "GBFS":
            self.current_path = self.gbfs.search(self.grid, self.start, self.goal, h_func)
            self.nodes_visited = self.gbfs.nodes_visited
            self.current_frontier = self.gbfs.frontier_nodes
            self.current_visited = self.gbfs.visited_nodes
        else:
            self.current_path = self.astar.search(self.grid, self.start, self.goal, h_func)
            self.nodes_visited = self.astar.nodes_visited
            self.current_frontier = self.astar.frontier_nodes
            self.current_visited = self.astar.visited_nodes
        
        self.execution_time = (time.time() - start_time) * 1000
        
        if self.current_path:
            self.path_cost = len(self.current_path) - 1
    
    def toggle_dynamic_mode(self):
        if not self.start or not self.goal:
            return
        
        self.dynamic_mode = not self.dynamic_mode
        
        if self.dynamic_mode:
            self.agent_pos = self.start
            self.path_index = 0
            self.find_path()
    
    def dynamic_step(self):
        if not self.dynamic_mode or not self.current_path:
            return
        
        if random.random() < self.obstacle_prob:
            self.spawn_random_obstacle()
        
        if self.path_index < len(self.current_path):
            next_pos = self.current_path[self.path_index]
            
            if self.grid[next_pos[0]][next_pos[1]] == 1:
                self.replan()
            else:
                self.agent_pos = next_pos
                self.path_index += 1
                
                if self.agent_pos == self.goal:
                    self.dynamic_mode = False
    
    def spawn_random_obstacle(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        
        if ((row, col) not in [self.start, self.goal, self.agent_pos] and 
            self.grid[row][col] != 1):
            self.grid[row][col] = 1
    
    def replan(self):
        h_func = manhattan_distance if self.heuristic == "Manhattan" else euclidean_distance
        
        if self.algorithm == "GBFS":
            self.current_path = self.gbfs.search(self.grid, self.agent_pos, self.goal, h_func)
        else:
            self.current_path = self.astar.search(self.grid, self.agent_pos, self.goal, h_func)
        
        if self.current_path:
            self.path_index = 1
        else:
            self.dynamic_mode = False
    
    def run(self):
        running = True
        last_step_time = time.time()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
            
            if self.dynamic_mode:
                current_time = time.time()
                if current_time - last_step_time > 0.5:
                    self.dynamic_step()
                    last_step_time = current_time
            
            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_metrics()
            self.draw_buttons()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
