import pygame
import math

pygame.init()
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador Sistema Solar")

BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (0, 51, 255)
VERMELHO = (188, 39, 50)
CINZA = (80, 78, 81)
LARANJA = (250, 116, 0)

FONTE = pygame.font.SysFont("arial", 16)
 
class Planeta:
        UA = 149.6e6 * 1000
        G = 6.67428e-11
        ESCALA = 150 / UA # 1UA == 100 pixels
        TIMESTEP = 3600*24 # 1 dia

        def __init__(self, x, y, raio, cor, massa):
            self.x = x
            self.y = y
            self.raio = raio
            self.cor = cor
            self.massa = massa

            self.orbita = []
            self.sol = False
            self.distancia_do_sol = 0

            self.x_vel = 0
            self.y_vel = 0

        def draw (self, win):
            x = self.x * self.ESCALA + WIDTH / 2
            y = self.y * self.ESCALA + HEIGHT / 2

            if len(self.orbita) > 2 :
                updated_pontos = []
                for ponto in self.orbita:
                    x, y = ponto
                    x = x * self.ESCALA + WIDTH / 2
                    y = y * self.ESCALA + HEIGHT / 2
                    updated_pontos.append((x, y))

                pygame.draw.lines(win, self.cor, False, updated_pontos, 2)


            pygame.draw.circle(win, self.cor, (x , y), self.raio)

            if not self.sol:
                distancia_texto = FONTE.render(f"{round(self.distancia_do_sol/1000)}km", 1, BRANCO) #adicionar round se quiser
                win.blit(distancia_texto, (x - distancia_texto.get_width()/2, y - distancia_texto.get_height()/2))


        def atracao(self, other):  
            other_x, other_y = other.x , other.y
            distancia_x = other_x - self.x
            distancia_y = other_y - self.y
            distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

            if other.sol:
                self.distancia_do_sol = distancia

            forca = self.G * self.massa * other.massa / distancia ** 2
            teta = math.atan2(distancia_y, distancia_x)
            forca_x = math.cos(teta) * forca
            forca_y = math.sin(teta) * forca
            return forca_x, forca_y

        def update_posicao (self, planetas):
            total_fx = total_fy = 0
            for planeta in planetas:
                if self == planeta:
                    continue

                fx, fy = self.atracao(planeta)
                total_fx += fx
                total_fy += fy

            self.x_vel += total_fx / self.massa * self.TIMESTEP
            self.y_vel += total_fy / self.massa * self.TIMESTEP
            
            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP
            self.orbita.append((self.x, self.y))




def main():
    run = True
    clock = pygame.time.Clock()

    sol = Planeta(0, 0, 30, AMARELO, 1.98892 * 10**30)
    sol.sol = True

    terra = Planeta(-1*Planeta.UA, 0, 16 ,AZUL, 5.9742 * 10**24)
    terra.y_vel = 29.783 * 1000

    marte = Planeta(-1.524 * Planeta.UA, 0, 12, VERMELHO, 6.39 *10**23)
    marte. y_vel = 24.007 * 1000
    
    mercurio = Planeta(0.387 * Planeta.UA, 0, 8, CINZA, 0.330 * 10**23)
    mercurio.y_vel = 47.4 * 1000

    venus = Planeta(0.723 * Planeta.UA, 0, 14, LARANJA, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000


    planetas = [sol, terra, marte, mercurio, venus]



    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planeta in planetas:
            planeta.update_posicao(planetas)
            planeta.draw(WIN)

        pygame.display.update()

    
    pygame.quit()

main()