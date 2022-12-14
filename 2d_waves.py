import pygame
import numpy as np
import random

H=1         # spatial set width
K=1         # time set width
DIMX=300    # with of simulation domain
DIMY=300    # height of simulation domain
CELLSIZE=2  # display size of a cell in pixel

def init_simulation():
    u = np.zeros((3, DIMX, DIMY))   # 3d sim grid
    c = 0.5 # original wave propagation speed
    alpha = np.zeros((DIMX, DIMY)) # wave prop velocities of entire sim dom
    alpha[0:DIMX, 0:DIMY] = ((c*K)/H)**2 # will be set to const value of tau
    return u, alpha

def update(u, alpha):
    u[2] = u[1]
    u[1] = u[0]

    u[0, 1:DIMX-1, 1:DIMY-1] = alpha[1:DIMX-1, 1:DIMY-1] * (u[1, 0:DIMX-2, 1:DIMY-1] +
                                        u[1, 2:DIMX, 1:DIMY-1] +
                                        u[1, 1:DIMX-1, 0:DIMY-2] +
                                        u[1, 1:DIMX-1, 2:DIMY] - 4*u[1, 1:DIMX-1, 1:DIMY-1]) \
                                        + 2*u[1, 1:DIMX-1, 1:DIMY-1] - u[2, 1:DIMX-1, 1:DIMY-1]
    
    u[0, 1:DIMX-1, 1:DIMY-1] *= 0.995

def place_raindrops(u):
    if (random.random()<0.02):
        x = random.randrange(5, DIMX-5)
        y = random.randrange(5, DIMY-5)
        u[0, x-2:x+2, y-2:y+2] = 120

def main():
    pygame.init()
    display = pygame.display.set_mode((DIMX*CELLSIZE, DIMY*CELLSIZE))
    pygame.display.set_caption("2d wave equation")

    u, alpha = init_simulation()
    pixeldata = np.zeros((DIMX, DIMY, 3), dtype=np.uint8)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        place_raindrops(u)
        update(u, alpha)

        pixeldata[1:DIMX, 1:DIMY, 0] = np.clip(u[0, 1:DIMX, 1:DIMY] + 128, 0, 255)
        pixeldata[1:DIMX, 1:DIMY, 1] = np.clip(u[1, 1:DIMX, 1:DIMY] + 128, 0, 255)
        pixeldata[1:DIMX, 1:DIMY, 2] = np.clip(u[2, 1:DIMX, 1:DIMY] + 128, 0, 255)

        surf = pygame.surfarray.make_surface(pixeldata)
        display.blit(pygame.transform.scale(surf, (DIMX*CELLSIZE, DIMY*CELLSIZE)), (0,0))
        pygame.display.update()

if __name__ == "__main__":
    main()