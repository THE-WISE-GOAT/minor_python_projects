import pygame      # graphics, window, drawing, events
import random      # random vehicle generation and colors
import time        # time utilities (unused currently)


# Screen width and height (entire window size)
SCREEN_W, SCREEN_H = 1000, 800

# Width of each road
ROAD_W = 150

# Frames per second (controls simulation speed)
FPS = 60

# Center reference point of the intersection
CENTER_X, CENTER_Y = 400, 400

# Traffic light phase durations (in simulation time steps / frames)
PHASES = {
    'GREEN': 300,     # Green light duration
    'YELLOW': 90,     # Yellow light duration
    'ALL_RED': 60     # Safety buffer where all lights are red
}


# Background and road colors
C_GRASS = (34, 139, 34)
C_ASPHALT = (45, 45, 48)
C_DASH = (20, 20, 25)

# Text color
C_WHITE = (240, 240, 240)

# Traffic light colors
C_RED = (230, 50, 50)
C_YEL = (240, 200, 50)
C_GRN = (50, 220, 100)


class TrafficLight:
    def __init__(self, pos, orientation="VERTICAL"):
        # Position of the traffic light on screen
        self.pos = pos
        
        # Orientation is kept for flexibility (not used actively here)
        self.orientation = orientation
        
        # Initial state of every traffic light
        self.state = "RED"

    def draw(self, screen):
        # Draw traffic light housing
        rect = pygame.Rect(self.pos[0], self.pos[1], 30, 80)
        pygame.draw.rect(screen, (10, 10, 10), rect, border_radius=5)

        # Draw red light (bright only if active)
        pygame.draw.circle(
            screen,
            C_RED if self.state == "RED" else (40, 0, 0),
            (rect.centerx, rect.y + 15),
            8
        )

        # Draw yellow light
        pygame.draw.circle(
            screen,
            C_YEL if self.state == "YELLOW" else (40, 40, 0),
            (rect.centerx, rect.y + 40),
            8
        )

        # Draw green light
        pygame.draw.circle(
            screen,
            C_GRN if self.state == "GREEN" else (0, 40, 0),
            (rect.centerx, rect.y + 65),
            8
        )


class Vehicle:
    def __init__(self, direction):
        # Direction from which the vehicle enters (N, S, E, W)
        self.dir = direction
        
        # Speed of vehicle (pixels per frame)
        self.speed = 3

        # Random color chosen for visual variety
        self.color = random.choice([
            (70, 130, 180),
            (220, 20, 60),
            (255, 140, 0),
            (119, 158, 203),
            (255, 179, 186),
            (188, 226, 158),
            (255, 223, 186),
            (42, 157, 143),
            (233, 196, 106),
            (231, 111, 81),
            (109, 89, 122),
            (82, 121, 111)
        ])

        # Set initial position and movement direction vector
        # Vector represents movement direction
        if direction == "N":
            self.pos = [420, 850]
            self.vec = (0, -1)   # Move upward
        elif direction == "S":
            self.pos = [350, -50]
            self.vec = (0, 1)    # Move downward
        elif direction == "E":
            self.pos = [-50, 420]
            self.vec = (1, 0)    # Move right
        elif direction == "W":
            self.pos = [850, 350]
            self.vec = (-1, 0)   # Move left

    def update(self, can_move):
        # Move vehicle only if allowed (green light and no collision)
        if can_move:
            self.pos[0] += self.vec[0] * self.speed
            self.pos[1] += self.vec[1] * self.speed

    def draw(self, screen):
        # Vehicle shape depends on direction
        w, h = (35, 18) if self.dir in "EW" else (18, 35)
        pygame.draw.rect(
            screen,
            self.color,
            (int(self.pos[0]), int(self.pos[1]), w, h),
            border_radius=3
        )


class SimulationManager:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create window
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Balanced Intersection Simulator")

        # Clock to control simulation speed
        self.clock = pygame.time.Clock()

        # Fonts for UI text
        self.font = pygame.font.SysFont("Verdana", 18)
        self.header_font = pygame.font.SysFont("Verdana", 24, bold=True)

        # Traffic lights placed at each approach
        self.lights = {
            "N": TrafficLight((480, 480)),
            "S": TrafficLight((290, 240)),
            "E": TrafficLight((290, 480)),
            "W": TrafficLight((480, 240))
        }

        # List of active vehicles
        self.vehicles = []

        # Simulation clock (discrete time)
        self.timer = 0

        # Counter for vehicles that passed the intersection
        self.total_passed = 0

    # Determines traffic light states based on time
    def get_phase_logic(self):
        t = self.timer
        cycle = PHASES['GREEN'] + PHASES['YELLOW'] + PHASES['ALL_RED']

        if t < PHASES['GREEN']:
            return ("GREEN", "RED")

        if t < PHASES['GREEN'] + PHASES['YELLOW']:
            return ("YELLOW", "RED")

        if t < cycle:
            return ("RED", "RED")

        if t < cycle + PHASES['GREEN']:
            return ("RED", "GREEN")

        if t < cycle + PHASES['GREEN'] + PHASES['YELLOW']:
            return ("RED", "YELLOW")

        return ("RED", "RED")


    def run(self):
        running = True

        while running:
            # Clear screen with grass background
            self.screen.fill(C_GRASS)

            # Advance simulation clock (loops over full signal cycle)
            self.timer = (self.timer + 1) % ((PHASES['GREEN'] + PHASES['YELLOW'] + PHASES['ALL_RED']) * 2)

            # Determine traffic light states
            ns_state, ew_state = self.get_phase_logic()

            # Apply light states to each traffic light
            for k, l in self.lights.items():
                l.state = ns_state if k in "NS" else ew_state

            # Draw horizontal and vertical roads
            pygame.draw.rect(self.screen, C_ASPHALT, (0, 325, 800, ROAD_W))
            pygame.draw.rect(self.screen, C_ASPHALT, (325, 0, ROAD_W, 800))

            # Draw intersection boundary
            pygame.draw.rect(self.screen, (60, 60, 65), (325, 325, 150, 150), 2)

            # Draw sidebar panel
            pygame.draw.rect(self.screen, C_DASH, (800, 0, 200, 800))

            # Random vehicle generation
            if random.random() < 0.02:
                self.vehicles.append(Vehicle(random.choice(["N", "S", "E", "W"])))

            # Update each vehicle
            for v in self.vehicles[:]:
                can_move = True
                l = self.lights[v.dir]

                # Stop vehicle at red or yellow signal
                if l.state != "GREEN":
                    if (
                        (v.dir == "E" and 280 < v.pos[0] < 300) or
                        (v.dir == "W" and 470 > v.pos[0] > 450) or
                        (v.dir == "S" and 280 < v.pos[1] < 300) or
                        (v.dir == "N" and 470 > v.pos[1] > 450)
                    ):
                        can_move = False

                # Collision avoidance with vehicle ahead
                for other in self.vehicles:
                    if v != other and v.dir == other.dir:
                        dist = ((v.pos[0] - other.pos[0])**2 + (v.pos[1] - other.pos[1])**2)**0.5
                        if dist < 50:
                            if (
                                (v.dir == "E" and other.pos[0] > v.pos[0]) or
                                (v.dir == "S" and other.pos[1] > v.pos[1]) or
                                (v.dir == "W" and other.pos[0] < v.pos[0]) or
                                (v.dir == "N" and other.pos[1] < v.pos[1])
                            ):
                                can_move = False

                # Move and draw vehicle
                v.update(can_move)
                v.draw(self.screen)

                # Remove vehicle once it exits the simulation area
                if (
                    v.pos[0] < -100 or v.pos[0] > 900 or
                    v.pos[1] < -100 or v.pos[1] > 900
                ):
                    self.vehicles.remove(v)
                    self.total_passed += 1

            # Display statistics
            self.screen.blit(self.header_font.render("METRICS", True, C_WHITE), (820, 30))
            self.screen.blit(self.font.render(f"Passed: {self.total_passed}", True, C_WHITE), (820, 80))
            self.screen.blit(self.font.render(f"Active: {len(self.vehicles)}", True, C_WHITE), (820, 110))

            # Draw traffic lights last (on top)
            for l in self.lights.values():
                l.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Control simulation speed
            self.clock.tick(FPS)

            # Handle quit event
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

        # Close pygame properly
        pygame.quit()


if __name__ == "__main__":
    SimulationManager().run()