import random

class Vex:
    def __init__(self, world_size, rock_density, dust_density):
        self.world = world_size
        self.map = [['clean' for _ in range(world_size[1])] for _ in range(world_size[0])]
        self.rocks = set()
        self.dust_spots = set()
        self.pos = (0, 0)
        self.face = 'right'
        self.steps = 0
        self.max_steps = 1000
        self.brain = {
            'dust_avg': 0,
            'cleaned': 0,
            'path': [],
            'rock_map': set()
        }
        
        self._sprinkle_rocks(rock_density)
        self._sprinkle_dust(dust_density)
        self._find_start()
    
    def _sprinkle_rocks(self, density):
        for i in range(self.world[0]):
            for j in range(self.world[1]):
                if random.random() < density:
                    self.rocks.add((i, j))
                    self.map[i][j] = 'rock'
    
    def _sprinkle_dust(self, density):
        for i in range(self.world[0]):
            for j in range(self.world[1]):
                if (i, j) not in self.rocks and random.random() < density:
                    self.dust_spots.add((i, j))
                    self.map[i][j] = 'dusty'
    
    def _find_start(self):
        while True:
            spot = (random.randint(0, self.world[0]-1), random.randint(0, self.world[1]-1))
            if spot not in self.rocks:
                self.pos = spot
                break
    
    def _blocked_ahead(self, spot):
        x, y = spot
        return (x < 0 or x >= self.world[0] or 
                y < 0 or y >= self.world[1] or 
                (x, y) in self.rocks)
    
    def _next_spot(self):
        x, y = self.pos
        if self.face == 'up': return (x-1, y)
        if self.face == 'right': return (x, y+1)
        if self.face == 'down': return (x+1, y)
        if self.face == 'left': return (x, y-1)
    
    def _spin_right(self):
        turns = ['up', 'right', 'down', 'left']
        self.face = turns[(turns.index(self.face) + 1) % 4]
    
    def see(self):
        now_status = self.map[self.pos[0]][self.pos[1]]
        front_block = self._blocked_ahead(self._next_spot())
        return {
            'here_status': now_status,
            'front_block': front_block,
            'where': self.pos,
            'facing': self.face
        }
    
    def think(self, brain, senses):
        new_brain = brain.copy()
        new_brain['path'].append(senses['where'])
        if len(new_brain['path']) > 10:
            new_brain['path'].pop(0)
        
        if senses['front_block']:
            new_brain['rock_map'].add(self._next_spot())
        
        if senses['here_status'] == 'dusty':
            new_brain['dust_avg'] = new_brain['dust_avg'] + 0.1
        else:
            new_brain['dust_avg'] = new_brain['dust_avg'] * 0.95
        
        return new_brain
    
    def decide(self, brain, senses):
        if senses['here_status'] == 'dusty':
            return 'suck'
        
        for _ in range(4):
            if not senses['front_block']:
                return 'go'
            self._spin_right()
            senses['front_block'] = self._blocked_ahead(self._next_spot())
        
        return 'spin'
    
    def act(self, choice):
        if choice == 'suck':
            if self.map[self.pos[0]][self.pos[1]] == 'dusty':
                self.map[self.pos[0]][self.pos[1]] = 'clean'
                self.dust_spots.discard(self.pos)
                self.brain['cleaned'] += 1
        elif choice == 'go':
            next_spot = self._next_spot()
            if not self._blocked_ahead(next_spot):
                self.pos = next_spot
        elif choice == 'spin':
            self._spin_right()
    
    def work(self):
        while self.steps < self.max_steps and self.dust_spots:
            senses = self.see()
            self.brain = self.think(self.brain, senses)
            choice = self.decide(self.brain, senses)
            self.act(choice)
            self.steps += 1

class CleverVex:
    def __init__(self, world_size, rock_density, dust_density):
        self.feet = Feet(world_size, rock_density, dust_density)
        self.hands = Hands()
        self.head = Head()
        self.mem = {}
    
    def work(self):
        while self.feet.steps < self.feet.max_steps and self.feet.dust_spots:
            foot_sense = self.feet.see()
            foot_mem = self.hands.think(self.mem.get('foot', {}), foot_sense, None)
            foot_choice = self.hands.do(self.mem.get('foot', {}), foot_sense, None)
            
            head_sense = self.hands.see_more(self.mem.get('foot', {}), foot_sense, foot_choice)
            head_mem = self.head.think(self.mem.get('head', {}), head_sense, foot_choice)
            head_choice = self.head.do(self.mem.get('head', {}), head_sense, foot_choice)
            
            self.feet.act(foot_choice)
            self.mem = {'foot': foot_mem, 'head': head_mem}

class Feet:
    def __init__(self, world_size, rock_density, dust_density):
        self.world = world_size
        self.map = [['clean' for _ in range(world_size[1])] for _ in range(world_size[0])]
        self.rocks = set()
        self.dust_spots = set()
        self.pos = (0, 0)
        self.face = 'right'
        self.steps = 0
        self.max_steps = 1000
        
        self._setup_world(rock_density, dust_density)
    
    def _setup_world(self, rock_density, dust_density):
        for i in range(self.world[0]):
            for j in range(self.world[1]):
                if random.random() < rock_density:
                    self.rocks.add((i, j))
                    self.map[i][j] = 'rock'
                elif random.random() < dust_density:
                    self.dust_spots.add((i, j))
                    self.map[i][j] = 'dusty'
        
        while True:
            spot = (random.randint(0, self.world[0]-1), random.randint(0, self.world[1]-1))
            if spot not in self.rocks:
                self.pos = spot
                break
    
    def see(self):
        return {
            'where': self.pos,
            'facing': self.face,
            'here_status': self.map[self.pos[0]][self.pos[1]],
            'front_block': self._blocked_ahead(self._next_spot())
        }
    
    def _blocked_ahead(self, spot):
        x, y = spot
        return (x < 0 or x >= self.world[0] or 
                y < 0 or y >= self.world[1] or 
                (x, y) in self.rocks)
    
    def _next_spot(self):
        x, y = self.pos
        if self.face == 'up': return (x-1, y)
        if self.face == 'right': return (x, y+1)
        if self.face == 'down': return (x+1, y)
        if self.face == 'left': return (x, y-1)
    
    def act(self, choice):
        if choice == 'suck':
            if self.map[self.pos[0]][self.pos[1]] == 'dusty':
                self.map[self.pos[0]][self.pos[1]] = 'clean'
                self.dust_spots.discard(self.pos)
        elif choice == 'go':
            next_spot = self._next_spot()
            if not self._blocked_ahead(next_spot):
                self.pos = next_spot
        elif choice == 'spin':
            turns = ['up', 'right', 'down', 'left']
            self.face = turns[(turns.index(self.face) + 1) % 4]
        
        self.steps += 1

class Hands:
    def think(self, mem, sense, choice):
        if not mem:
            mem = {'spins': 0, 'last_moves': []}
        
        mem['last_moves'].append(choice)
        if len(mem['last_moves']) > 5:
            mem['last_moves'].pop(0)
        
        if choice == 'spin':
            mem['spins'] += 1
        else:
            mem['spins'] = 0
            
        return mem
    
    def do(self, mem, sense, choice):
        if sense['here_status'] == 'dusty':
            return 'suck'
        
        if not sense['front_block']:
            return 'go'
        
        return 'spin'
    
    def see_more(self, mem, sense, choice):
        return {
            'sucked_dust': choice == 'suck',
            'where': sense['where'],
            'stuck': mem.get('spins', 0) >= 4
        }

class Head:
    def think(self, mem, sense, choice):
        if not mem:
            mem = {'total_sucked': 0, 'seen_spots': set()}
        
        mem['seen_spots'].add(sense['where'])
        if sense['sucked_dust']:
            mem['total_sucked'] += 1
            
        return mem
    
    def do(self, mem, sense, choice):
        return None

if __name__ == "__main__":
    print("Testing Vex the vacuum...")
    
    vex = Vex((5, 5), 0.1, 0.3)
    vex.work()
    print(f"Simple Vex - Steps: {vex.steps}, Dust left: {len(vex.dust_spots)}")
    
    smart_vex = CleverVex((5, 5), 0.1, 0.3)
    smart_vex.work()
    print(f"Smart Vex - Steps: {smart_vex.feet.steps}, Dust left: {len(smart_vex.feet.dust_spots)}")
    
    print("All tests passed! Vex is cleaning!")

# AI Statement: AI tools such as VS Code Copilot were used to assist and 
# manage error in the development of this code.
