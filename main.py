import pygame
import random
import numpy as np
from dino import Dino

# Set up Pygame
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))

# Simulation Params
cactus_width, cactus_height = 20, 60
cactus_color = (255, 0, 0)
cactus_list = []
dino_list = []
pop_size = 20
live_dinos = pop_size
best_score = 0
bsg = 0
generation = 0


def mutate_layer(mutation_rate, mutation_step, layer):
    if mutation_rate > 1 or mutation_rate < 0:
        raise Exception("Mutation rate out of bounds. Must be between 0 - 1")
    mutated_layer = layer
    for i in range(len(mutated_layer)):
        for j in range(len(mutated_layer[i])):
            rand = random.randint(0, 100)
            if rand <= (mutation_rate*100):
                mutated_layer[i][j] = random.randint(-1, 1) * mutation_step
    return mutated_layer


def avg_colors(w1, w2, c1, c2):
    result = (w1 * c1[0] + w2 * c2[0]) / (w1 + w2), (w1 * c1[1] + w2 * c2[1]) / (w1 + w2), (w1 * c1[2] + w2 * c2[2]) / (
            w1 + w2)
    return result


def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n


def mutate_color(color,step_size):
    mutated_color = list(color)
    r = random.randint(0, 2)
    step_dir = random.randrange(-1, 1, 2)
    mutated_color[r] = clamp(mutated_color[r] + step_dir*step_size*10, 0, 255)
    return tuple(mutated_color)


def mutate_dino(dino, m_rate, step_size):
    mutated_layers = []
    new_color = ()
    for layer in dino.model.layers:
        mutated_layers.append(mutate_layer(m_rate, step_size, layer.get_weights()[0]))
        new_color = mutate_color(dino.color, step_size)
    return Dino(new_color, mutated_layers)

# *** DOES NOT DO GOOD THINGS
# Cross over weights of two different Neural Networks stored inside Dino Class beacause why not

# def cross_over(dino1, dino2):
#     d1layer0 = dino1.model.layers[0].get_weights()[0]
#     d2layer0 = dino2.model.layers[0].get_weights()[0]
#
#     d1layer1 = dino1.model.layers[1].get_weights()[0]
#     d2layer1 = dino2.model.layers[1].get_weights()[0]
#
#     d1layer2 = dino1.model.layers[2].get_weights()[0]
#     d2layer2 = dino2.model.layers[2].get_weights()[0]
#
#     new_layers = []
#     new_color = ()
#
#     layers = [[d1layer0, d2layer0], [d1layer1, d2layer1], [d1layer2, d2layer2]]
#     for i in range(len(layers)):
#         crossover_point = random.randint(1, len(layers[i][0][0])-1)
#         if i == 0:
#             new_color = avg_colors(crossover_point, len(layers[i][0][0]) - crossover_point, dino1.color, dino2.color)
#         new_layer = np.concatenate((layers[i][0][:crossover_point], layers[i][1][crossover_point:]))
#         new_layers.append(np.array(mutate_layer(0.2, 1, new_layer)))
#         new_color = mutate_color(new_color)
#     return Dino(new_color, new_layers)


def populate(fittest, pop_size):
    dinos = [fittest[0],fittest[1]]
    while len(dinos) < pop_size:
        child_dino = mutate_dino(fittest[0], 0.3, 0.2)
        child_dino2 = mutate_dino(fittest[0], 0.3, 2)
        child_dino3 = mutate_dino(fittest[1], 0.3, 0.2)
        child_dino4 = mutate_dino(fittest[1], 0.3, 2)
        dinos.append(child_dino)
        dinos.append(child_dino2)
        dinos.append(child_dino3)
        dinos.append(child_dino4)
    return dinos


def find_fittest(dinos):
    fittest = [dinos[0], dinos[1]]
    for dino in dinos:
        if dino.score > fittest[0].score:
            fittest[1] = fittest[0]
            fittest[0] = dino
    return fittest


for i in range(pop_size):
    rand_c = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    dino_list.append(Dino(color=rand_c))

# Define game variables
current_tick = 0
score_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
game_running = True
next_cactus_tick = 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = not game_running

        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_SPACE and is_jumping:
        #         # End jumping and set jump velocity
        #         is_jumping = False
        #         dino_y_vel = jump_vel * jump_count // 5
        #         jump_count = 0

    if game_running and live_dinos > 0:
        # Update game state

        # if is_jumping and jump_count <= jump_mult_max:
        #     # Increase jump count while jumping
        #     jump_count += 4
        #

        # dino_rect.width = dino_width+jump_count*2
        # dino_rect.height = dino_height-jump_count*2
        # dino_rect.x = 50 - jump_count
        # dino_rect.y += dino_y_vel
        # dino_y_vel += 3
        # if dino_rect.y > 300+jump_count*2:
        #     dino_rect.y = 300+jump_count*2
        #     dino_y_vel = 0

        # Update dinos
        for dino in dino_list:
            if len(cactus_list) > 0:
                x = cactus_list[0].x
                w = cactus_list[0].width
                h = cactus_list[0].height
            else:
                x, w, h = 0, 0, 0
            dino.update(x, w, h,current_tick)

        # Update cacti
        for cactus in cactus_list:
            cactus.x -= 10

        # Check for collisions
        for cactus in cactus_list:
            for dino in dino_list:
                if dino.rect.colliderect(cactus) and dino.alive:
                    dino.alive = False
                    live_dinos -= 1

        # Spawn new cacti
        if current_tick > next_cactus_tick:
            random_height = random.randint(-30, 0+min(int(next_cactus_tick/50), 150))
            random_width = random.randint(0, 0+min(int(next_cactus_tick/100), 70))
            new_cactus_rect = pygame.Rect(width, 300 - random_height, cactus_width + random_width,
                                          cactus_height + random_height)
            cactus_list.append(new_cactus_rect)
            next_cactus_tick = current_tick + random.randint(80-min(int(current_tick/100), 60),
                                                             125-min(int(current_tick/100), 80))

        # Remove cacti that have gone off-screen
        cactus_list = [cactus for cactus in cactus_list if cactus.x > -cactus_width]

        # Update score
        current_tick += 1

        # Draw game objects
        screen.fill((255, 255, 255))
        for dino in dino_list:
            pygame.draw.rect(screen, dino.color, dino.rect)
        for cactus in cactus_list:
            pygame.draw.rect(screen, cactus_color, cactus)
        score_text = score_font.render(f"Score: {current_tick}  Gen: {generation} Alive {live_dinos}", True, (0, 0, 0))
        best_text = score_font.render(f"Best: {best_score}  Gen: {bsg}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(best_text, (10, 40))
        # Update screen
        pygame.display.update()

        # Delay so game doesn't run at mach 3
        pygame.time.delay(10)

    else:
        # Game over screen
        pygame.display.update()
        # re-init
        if current_tick > 0:
            if(current_tick > best_score):
                best_score = current_tick
                bsg = generation
            generation += 1
            cactus_list = []
            current_tick = 0
            next_cactus_tick = 0
            fittest = find_fittest(dino_list)
            for dino in fittest:
                dino.alive = True
                dino.score = 0
            dino_list = populate(fittest, pop_size)
            live_dinos = len(dino_list)
            # for i in range(pop_size):
            #     rand_c = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
            #     dino_list.append(Dino(color=rand_c))
