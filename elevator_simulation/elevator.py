# Simple elevator simulation (two cars, passenger pickup/dropoff)
# Directional commitment and basic call assignment

import pygame
import random

WIDTH, HEIGHT = 1100, 800  # Window dimensions
SIDEBAR_W = 280  # Sidebar width for floor labels
FLOORS = 10  # Number of floors
FLOOR_H = HEIGHT // FLOORS  # Height per floor
FPS = 60  # Frames per second
CAPACITY = 6  # Max passengers per elevator

# Color Palette
C_VOID = (10, 10, 15)  # Background
C_ACCENT = (0, 255, 100)  # Green for new/waiting passengers
C_WAITING = (255, 160, 0)  # Orange for long-waiting passengers
C_ELEV_GLOW = (0, 130, 255)  # Elevator glow
C_GREY = (60, 60, 65)  # Exited/done passengers
C_METAL = (120, 125, 135)  # Elevator doors


class Passenger:
    """Represents a passenger in the elevator system."""
    def __init__(self, start, offset=0):
        self.start = start  # Starting floor
        self.dest = random.choice([i for i in range(FLOORS) if i != start])  # Random destination != start
        self.dir = 1 if self.dest > self.start else -1  # Direction: 1 up, -1 down

        # Position on floor, offset for side-by-side spawning
        base_x = (150 + (WIDTH - SIDEBAR_W - 250)) // 2 + 50
        self.x = base_x + offset * 30
        self.y = (FLOORS - 1 - start) * FLOOR_H + FLOOR_H - 20
        self.target_x = self.x  # Target x for walking

        # State management
        self.state = "NEW"  # States: NEW, WAITING, WALKING_IN, IN_ELEVATOR, WALKING_OUT, DONE
        self.timer = 100  # Timer for state transition
        self.walk_speed = 1.5  # Reduced walking speed for smoother animation
        self.wait_time = 0  # Time spent waiting, for color change
        self.board_order = 0  # Order boarded, for prioritization

        # Assignment to elevator
        self.assigned_elevator = None

    def update(self):
        """Update passenger state and position."""
        if self.state == "NEW":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "WAITING"

        if self.state in ["NEW", "WAITING"]:
            self.wait_time += 1  # Track waiting time for color change

        # Move towards target_x
        if self.x < self.target_x:
            self.x = min(self.x + self.walk_speed, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - self.walk_speed, self.target_x)

        # Check if reached target
        if abs(self.x - self.target_x) < 1:
            if self.state == "WALKING_IN":
                self.state = "IN_ELEVATOR"
            elif self.state == "WALKING_OUT":
                self.state = "DONE"

    def draw(self, screen, font):
        """Draw the passenger on screen."""
        if self.state == "IN_ELEVATOR":
            return  # Hidden when inside elevator

        # Determine color based on state and wait time
        if self.state in ["NEW", "WAITING"]:
            color = C_ACCENT if self.wait_time < 600 else C_WAITING
        elif self.state in ["WALKING_OUT", "DONE"]:
            color = C_GREY
        else:
            color = C_ACCENT

        # Draw passenger circle
        pygame.draw.circle(screen, color, (int(self.x), int(self.y - 12)), 8)

        # Draw destination number
        num_txt = font.render(str(self.dest), True, (255, 255, 255))
        screen.blit(num_txt, (self.x - 5, self.y - 35))

        # Draw direction arrow
        if self.state != "DONE":
            arrow_color = (100, 100, 100)
            if self.dir == 1:  # Up arrow
                pygame.draw.polygon(
                    screen,
                    arrow_color,
                    [(self.x - 7, self.y - 2),
                     (self.x + 7, self.y - 2),
                     (self.x, self.y - 12)]
                )
            else:  # Down arrow
                pygame.draw.polygon(
                    screen,
                    arrow_color,
                    [(self.x - 7, self.y - 15),
                     (self.x + 7, self.y - 15),
                     (self.x, self.y - 5)]
                )


class Elevator:
    """Represents an elevator car with state management and movement."""
    next_board_order = 0  # Global counter for boarding order

    def __init__(self, x_pos, id_num):
        self.x = x_pos  # Horizontal position
        self.id = id_num  # Elevator ID (0 or 1)
        self.y = float((FLOORS - 1) * FLOOR_H)  # Vertical position (top floor)
        self.target_y = self.y  # Target vertical position
        self.door_anim = 0.0  # Door animation state (0 closed, 1 open)
        self.passengers = []  # List of passengers inside
        self.state = "IDLE"  # States: IDLE, OPENING, BOARDING, CLOSING, MOVING
        self.timer = 0  # Timer for boarding/closing
        self.speed = 1.5  # Reduced movement speed for smoother animation
        self.direction = 0  # Direction: 1 up, -1 down, 0 idle
        self.cooldown = 0  # Cooldown to prevent immediate reopen

    def get_current_floor(self):
        """Calculate the current floor based on y position."""
        return FLOORS - 1 - round(self.y / FLOOR_H)

    def get_exact_floor(self):
        """Get exact floor position for smoother calculations."""
        return FLOORS - 1 - (self.y / FLOOR_H)

    def update(self, all_passengers):
        """Update elevator state, movement, and interactions."""
        # Always check for new tasks
        self.find_next_task(all_passengers)

        if self.cooldown > 0:
            self.cooldown -= 1  # Decrement cooldown timer

        if self.state == "IDLE":
            pass # handling in find_next_task
            
        elif self.state == "MOVING":
            if self.y < self.target_y:
                self.y = min(self.y + self.speed, self.target_y)
            elif self.y > self.target_y:
                self.y = max(self.y - self.speed, self.target_y)

            if abs(self.y - self.target_y) < 0.1:
                self.y = self.target_y
                self.state = "OPENING"

        elif self.state == "OPENING":
            self.door_anim = min(1.0, self.door_anim + 0.02)  # Slower door opening
            if self.door_anim >= 1.0:
                self.state = "BOARDING"
                self.timer = 120  # Longer boarding time

        elif self.state == "BOARDING":
            curr_f = self.get_current_floor()
            
            # Alighting
            leaving = [
                p for p in self.passengers
                if p.dest == curr_f and p.state == "IN_ELEVATOR"
            ]

            for i, p in enumerate(leaving):
                p.state = "WALKING_OUT"
                p.target_x = -100 - i * 30 if self.id == 0 else WIDTH + 100 + i * 30
                p.y = (FLOORS - 1 - curr_f) * FLOOR_H + FLOOR_H - 20
                self.passengers.remove(p)

            available_slots = CAPACITY - len(self.passengers)

            # Auto-turnaround check:
            # If no tasks remain STRICTLY ahead in the current direction, 
            # release the committed direction so we can pick up any assigned call here (e.g. turnaround).
            if self.direction != 0:
                 has_tasks_ahead = False
                 for p in self.passengers:
                      if (p.dest - curr_f) * self.direction > 0: 
                          has_tasks_ahead = True
                          break
                 
                 if not has_tasks_ahead:
                     for p in all_passengers:
                          # Check assigned calls strictly ahead
                          if p.assigned_elevator == self.id and p.state in ["NEW", "WAITING"]:
                              if (p.start - curr_f) * self.direction > 0:
                                   has_tasks_ahead = True
                                   break
                 
                 if not has_tasks_ahead:
                      self.direction = 0

            # Boarding: strict direction check
            # Only board if passenger aligns with our committed direction,
            # or if we are IDLE/Reversing.
            
            waiting_here = [
                p for p in all_passengers
                if p.start == curr_f
                and p.state in ["NEW", "WAITING"]
                and p.assigned_elevator == self.id
            ]
            
            # Filter by direction
            # If we have a direction, only take passengers going that way.
            # UNLESS we are empty and this is our only task (which means we turn).
            
            entering = []
            for p in waiting_here:
                if len(entering) >= available_slots:
                    break
                    
                should_board = False
                if self.direction == 0:
                     should_board = True
                     # Will set direction below
                elif p.dir == self.direction:
                     should_board = True
                
                if should_board:
                     entering.append(p)

            for i, p in enumerate(entering):
                p.state = "WALKING_IN"
                p.target_x = self.x + 50 + i * 20
                self.passengers.append(p)
                # If we were IDLE, we commit to this passenger's direction
                if self.direction == 0:
                     self.direction = p.dir

            if self.timer > 0:
                self.timer -= 1
            else:
                self.state = "CLOSING"

        elif self.state == "CLOSING":
            self.door_anim = max(0.0, self.door_anim - 0.02)  # Slower door closing
            if self.door_anim <= 0:
                self.state = "IDLE"
                self.cooldown = 20

    def find_next_task(self, all_passengers):
        """Determine the next task for the elevator based on priority and direction."""
        # Don't interrupt door operations
        if self.state in ["OPENING", "BOARDING", "CLOSING"]:
            return

        curr_f = self.get_current_floor()
        exact_f = self.get_exact_floor()

        # Gather relevant tasks: destinations inside and assigned calls
        inside_dest = [p.dest for p in self.passengers]
        assigned_calls = [
            p for p in all_passengers
            if p.assigned_elevator == self.id
            and p.state in ["NEW", "WAITING"]
        ]

        # Priority 1: If idle, find nearest task
        if self.direction == 0:
            if not inside_dest and not assigned_calls:
                return

            # Pick nearest target
            all_targets = inside_dest + [p.start for p in assigned_calls]
            nearest_f = min(all_targets, key=lambda f: abs(f - curr_f))

            if nearest_f == curr_f:
                # Call at current floor, open doors
                here_call = next((p for p in assigned_calls if p.start == curr_f), None)
                if here_call:
                    self.direction = here_call.dir
                    self.state = "OPENING"
            else:
                # Move to nearest floor
                self.target_y = (FLOORS - 1 - nearest_f) * FLOOR_H
                self.direction = 1 if nearest_f > curr_f else -1
                self.state = "MOVING"
            return

        # Priority 2: If committed to direction, find next stop ahead
        # Identify stops ahead in current direction
        stops = []

        # Check inside passengers' destinations ahead
        for f in inside_dest:
            if (f - exact_f) * self.direction >= -0.1:  # Forward or current floor
                stops.append(f)

        # Check assigned hall calls ahead in same direction
        for p in assigned_calls:
            if (p.start - exact_f) * self.direction >= -0.1:
                if p.dir == self.direction:
                    stops.append(p.start)

        if stops:
            # Go to nearest valid stop in direction
            if self.direction == 1:
                next_stop = min(stops)
            else:
                next_stop = max(stops)

            self.target_y = (FLOORS - 1 - next_stop) * FLOOR_H

            # If already at the stop, open doors
            if abs(exact_f - next_stop) < 0.1:
                if self.cooldown == 0:
                    self.state = "OPENING"
            else:
                self.state = "MOVING"
            if abs(self.y - self.target_y) < 1.0:
                 self.state = "OPENING"
            else:
                 self.state = "MOVING"
            return
            
        # 3. Direction Exhausted?
        # No VALID stops ahead in current direction.
        # Check for calls in opposite direction AHEAD (to turn around at top/bottom)
        
        furthest_target = None
        for p in assigned_calls:
             # Check if it's "ahead" physically
             if (p.start - exact_f) * self.direction > 0:
                  cand = p.start
                  if furthest_target is None:
                      furthest_target = cand
                  else:
                      if self.direction == 1:
                          furthest_target = max(furthest_target, cand)
                      else:
                          furthest_target = min(furthest_target, cand)
                          
        if furthest_target is not None:
             self.target_y = (FLOORS - 1 - furthest_target) * FLOOR_H
             self.state = "MOVING"
             return
             
        # 4. Totally Exhausted
        # No requests ahead. Stop and become IDLE.
        self.direction = 0
        self.state = "IDLE"
        # Immediate re-scan (recursion safe as dir=0 now)
        self.find_next_task(all_passengers)

    def draw(self, screen):
        """Draw the elevator car, passengers, doors, and direction indicator."""
        rect = pygame.Rect(self.x + 5, self.y + 5, 100, FLOOR_H - 10)
        color = C_ELEV_GLOW if self.direction != 0 else C_METAL  # Glow when moving
        pygame.draw.rect(screen, (25, 30, 45), rect, border_radius=5)  # Background

        # Draw passengers inside
        for i, p in enumerate(self.passengers):
            if p.state == "IN_ELEVATOR":
                px = self.x + 25 + (i % 3 * 25)
                py = self.y + 25 + (i // 3 * 25)
                pygame.draw.circle(screen, (220, 220, 220), (int(px), int(py)), 6)

        # Draw doors
        gap = 50 * self.door_anim
        pygame.draw.rect(screen, C_METAL, (rect.x, rect.y, 50 - gap, rect.h))
        pygame.draw.rect(screen, C_METAL, (rect.x + 50 + gap, rect.y, 50 - gap, rect.h))
        pygame.draw.rect(screen, color, rect, 2, border_radius=5)

        # Draw direction arrow
        if self.direction != 0:
            cx, cy = rect.centerx, rect.centery
            arrow_col = (0, 255, 0)
            if self.direction == 1:  # Up arrow
                pygame.draw.polygon(screen, arrow_col, [(cx-5, cy+5), (cx+5, cy+5), (cx, cy-5)])
            else:  # Down arrow
                pygame.draw.polygon(screen, arrow_col, [(cx-5, cy-5), (cx+5, cy-5), (cx, cy+5)])


class SimManager:
    """Manages the overall simulation, including elevators, passengers, and call assignment."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        # Create two elevators
        self.elevators = [
            Elevator(150, 0),
            Elevator(WIDTH - SIDEBAR_W - 250, 1)
        ]

        self.passengers = []

    def assign_calls(self):
        """Assign unassigned passengers to the best elevator based on cost."""
        for p in self.passengers:
            if p.state not in ["NEW", "WAITING"] or p.assigned_elevator is not None:
                continue

            best_elevator = None
            best_cost = float("inf")

            for e in self.elevators:
                curr_f = e.get_current_floor()
                dist = abs(curr_f - p.start)

                # Cost calculation: prefer elevators moving towards the call
                score = float("inf")

                heading_towards = False
                if e.direction == 1 and p.start >= curr_f:
                    heading_towards = True
                elif e.direction == -1 and p.start <= curr_f:
                    heading_towards = True

                if heading_towards:
                    score = dist  # Low cost for correct direction
                elif e.direction == 0:
                    score = dist + 2  # Medium for idle
                else:
                    score = dist + 5  # High penalty for wrong direction

                if score < best_cost:
                    best_cost = score
                    best_elevator = e

            if best_elevator:
                p.assigned_elevator = best_elevator.id
                    
                if heading_towards and e.direction == p.dir:
                    # Ideal: Moving towards and same direction
                    score = dist
                elif e.direction == 0:
                    # Idle: Second best
                    score = dist + 5.0 
                elif heading_towards:
                    # Moving towards but wrong dir (e.g. going UP to 8, call at 5 DOWN)
                    # We treat this as "Moving Incorrectly" effectively for the purpose of "Least Delay to Pickup"
                    # But delay is distance...
                    # Penalize elevators moving in the wrong direction to avoid long delays
                    score = dist + 20.0
                else:
                    # Moving away
                    score = dist + 50.0

                if score < best_cost:
                    best_cost = score
                    best_elevator = e

            if best_elevator:
                p.assigned_elevator = best_elevator.id

    def run(self):
        """Main simulation loop."""
        while True:
            self.screen.fill(C_VOID)

            # Draw floor lines and labels
            for i in range(FLOORS):
                y = i * FLOOR_H
                pygame.draw.line(self.screen, (35, 35, 45), (0, y), (WIDTH - SIDEBAR_W, y), 2)
                txt = self.font.render(f"Lvl {FLOORS - 1 - i}", True, (80, 80, 90))
                self.screen.blit(txt, (10, y + 10))

            # Spawn new passengers occasionally (reduced frequency and max)
            if len(self.passengers) < 15 and random.random() < 0.007:
                start_f = random.randint(0, FLOORS - 1)
                self.passengers.append(Passenger(start_f))

            # Assign calls to elevators
            self.assign_calls()

            # Update and draw elevators
            for e in self.elevators:
                e.update(self.passengers)
                e.draw(self.screen)

            # Update and draw passengers
            for p in self.passengers[:]:
                p.update()
                if p.state == "DONE" and (p.x < -50 or p.x > WIDTH + 50):
                    self.passengers.remove(p)
                else:
                    p.draw(self.screen, self.font)

            pygame.display.flip()
            self.clock.tick(FPS)

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == "__main__":
    # Start the elevator simulation
    SimManager().run()
