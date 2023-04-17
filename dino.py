import pygame
import tensorflow as tf
import numpy as np


class Dino:
    def __init__(self, color, weights=None):
        self.alive = True
        self.y_vel = 0
        self.width, self.height = 40, 60
        self.color = color
        self.rect = pygame.Rect(50, 300, self.width, self.height)
        self.jump_vel = -10
        self.jump_mult_max = 25
        self.jump_strength = 0
        self.score = 0
        self.is_jumping = False
        self.target_strength = 1
        self.last_action = None

        # Create layers for Neural Net
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(5, input_dim=3, activation='relu', input_shape=[1]),
            tf.keras.layers.Dense(3, activation='sigmoid'),
            tf.keras.layers.Dense(2, activation='sigmoid', )
        ])

        if weights is not None:
            for i in range(len(weights)):
                empty_bias = np.zeros(len(weights[i][0]))
                self.model.layers[i].set_weights([weights[i], empty_bias])

    def jump(self, strength):
        if self.rect.y >= 300:
            self.score -= 20
            self.is_jumping = True
            self.target_strength = min(strength, self.jump_mult_max)

    def jump_update(self):
        # Handle jumping
        if self.is_jumping:
            if self.jump_strength < self.target_strength:
                self.jump_strength += 1
            else:
                self.y_vel = self.jump_vel * self.jump_strength // 5
                self.jump_strength = 0
                self.target_strength = 0
                self.is_jumping = False
        # Gravity and other stuff
        self.rect.width = self.width + self.jump_strength * 2
        self.rect.height = self.height - self.jump_strength * 2
        self.rect.x = 50 - self.jump_strength
        self.rect.y += self.y_vel
        self.y_vel += 3
        if self.rect.y > 300 + self.jump_strength * 2:
            self.rect.y = 300 + self.jump_strength * 2
            self.y_vel = 0

    def update(self, cactus_x, cactus_w, cactus_h, tick):
        if self.alive:
            self.jump_update()
            self.score += 1
            if cactus_x < self.rect.x:
                self.score += 10
            if tick % 5 == 0:
                action = self.model(np.array([cactus_x, cactus_w, cactus_h], dtype=np.float32))[0]
                jump = action[0]
                strength = action[1]
                if jump > 0.5:
                    self.jump(strength * self.jump_mult_max)
        else:
            self.rect.x -= 10
