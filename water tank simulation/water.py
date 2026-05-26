import pygame
import random
import sys

WIDTH, HEIGHT = 900, 700
TANK_W, TANK_H = 300, 400
SIDEBAR_W = 250
FPS = 60

# Colors
C_WATER = (50, 150, 255)
C_TANK = (200, 200, 210)
C_DANGER = (255, 50, 50)
C_GRASS = (34, 139, 34)
C_BG = (20, 22, 28)
C_TEXT = (240, 240, 240)
C_GOLD = (255, 215, 0)

class WaterSystem:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Smart Flood Control & Water Management Model")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.bold_font = pygame.font.SysFont("Arial", 26, bold=True)

        # Simulation Variables
        self.water_level = 100.0  # Pixels of water
        self.max_level = TANK_H
        self.inflow_rate = 0.5    # Constant rain/inflow
        self.outflow_rate = 0.0   # Pump speed
        self.pump_active = False
        self.flood_events = 0
        self.is_flooded = False

    def update_logic(self):
        # 1. Natural Inflow (Simulation of Rain)
        # Random variation makes the model more realistic
        actual_inflow = self.inflow_rate + random.uniform(-0.1, 0.2)
        self.water_level += actual_inflow

        # 2. Smart Sensor Logic
        # If water > 80%, turn on pump. If < 30%, turn off.
        if self.water_level > self.max_level * 0.8:
            self.pump_active = True
            self.outflow_rate = 1.2 # Pump is stronger than rain
        elif self.water_level < self.max_level * 0.3:
            self.pump_active = False
            self.outflow_rate = 0.0

        # 3. Apply Pump Outflow
        self.water_level -= self.outflow_rate

        # 4. Bounds and Flood Tracking
        if self.water_level >= self.max_level:
            self.water_level = self.max_level
            if not self.is_flooded:
                self.flood_events += 1
                self.is_flooded = True
        else:
            self.is_flooded = False
        
        if self.water_level < 0: self.water_level = 0

    def draw_gui(self):
        # Sidebar Panel
        pygame.draw.rect(self.screen, (15, 15, 20), (WIDTH - SIDEBAR_W, 0, SIDEBAR_W, HEIGHT))
        
        # Calculate percentage
        pct = (self.water_level / self.max_level) * 100
        
        # Header
        self.screen.blit(self.bold_font.render("SYSTEM STATS", True, C_GOLD), (WIDTH - 220, 40))
        
        # Metrics
        stats = [
            f"Water Level: {pct:.1f}%",
            f"Inflow: {self.inflow_rate:.2f} L/s",
            f"Pump Outflow: {self.outflow_rate:.2f} L/s",
            f"Total Floods: {self.flood_events}"
        ]
        
        for i, text in enumerate(stats):
            label = self.font.render(text, True, C_TEXT)
            self.screen.blit(label, (WIDTH - 220, 100 + (i * 40)))

        # Visual Pump Switch
        status_txt = "PUMP: ON" if self.pump_active else "PUMP: OFF"
        status_col = (0, 255, 100) if self.pump_active else (100, 100, 100)
        pygame.draw.rect(self.screen, status_col, (WIDTH - 220, 300, 180, 40), border_radius=5)
        self.screen.blit(self.font.render(status_txt, True, (0,0,0)), (WIDTH - 165, 310))

        # Alert Indicator
        alert_col = C_DANGER if pct > 90 else C_GOLD if pct > 70 else (50, 200, 50)
        alert_msg = "CRITICAL" if pct > 90 else "STABLE"
        pygame.draw.circle(self.screen, alert_col, (WIDTH - 210, 400), 10)
        self.screen.blit(self.font.render(f"SYSTEM: {alert_msg}", True, alert_col), (WIDTH - 190, 390))

    def draw_world(self):
        self.screen.fill(C_BG)
        
        # Draw Tank / Reservoir
        tank_rect = pygame.Rect(200, 150, TANK_W, TANK_H)
        pygame.draw.rect(self.screen, C_TANK, tank_rect, 5, border_radius=10)
        
        # Draw Water
        water_height = int(self.water_level)
        water_rect = pygame.Rect(205, 150 + (TANK_H - water_height), TANK_W - 10, water_height)
        # If flooded, make water pulsate red
        color = C_WATER if not self.is_flooded else (255, 100, 100)
        pygame.draw.rect(self.screen, color, water_rect, border_radius=5)

        # Draw Inflow Pipe
        pygame.draw.rect(self.screen, (80, 80, 90), (100, 160, 100, 30))
        if self.inflow_rate > 0:
            pygame.draw.rect(self.screen, C_WATER, (190, 190, 10, 20)) # Water dripping

        # Draw Outflow Pump
        pygame.draw.rect(self.screen, (80, 80, 90), (500, 500, 100, 30))
        if self.pump_active:
            # Animate outflow spray
            for _ in range(5):
                x = 600 + random.randint(0, 50)
                y = 515 + random.randint(-10, 10)
                pygame.draw.circle(self.screen, C_WATER, (x, y), 3)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                # Manual Control: Press UP/DOWN to change inflow (Rain intensity)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.inflow_rate += 0.2
                    if event.key == pygame.K_DOWN: self.inflow_rate -= 0.2

            self.update_logic()
            self.draw_world()
            self.draw_gui()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    WaterSystem().run()