import numpy as np
import matplotlib.pyplot as plt
import time
import pygame as pg
import threading as th
import Subjektklassen


class Display:
    def __init__(self, size=1000, factor = 10):
        self.factor = factor
        self.size = size
        pg.init()
        self.screen1 = pg.display.set_mode((self.size, self.size))
        self.screen2 = pg.Surface((self.size, self.size))

    def step(self, Entitys):
        def run_thread(Entitys):
            self.screen1.blit(self.screen2, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                    pass
            for Ent in Entitys:
                if isinstance(Ent, Subjektklassen.Subjekt):
                    pg.draw.circle(self.screen1, color=(0,255,0), center=(self.factor*Ent.posf() + 40), radius=5, width=3)
                elif isinstance(Ent, Subjektklassen.Food):
                    pg.draw.circle(self.screen1, color=(0,0,255), center=(Ent.x*self.factor+40, 40 +Ent.y*self.factor), radius=5, width=3)

            pg.display.flip()
            pg.display.update()

        #runner = th.Thread(target=run_thread(Entitys=Entitys))
        #runner.start()
        run_thread(Entitys)
