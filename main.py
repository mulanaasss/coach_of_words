import pygame
import sys
import random
pygame.init()

#настройки экрана
screen_width = 1170
screen_height = 779
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Тренер перевода слов с английского на русский")

background_image = pygame.image.load("background2.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
CORRECT_COLOR = (0, 200, 0)
WRONG_COLOR = (200, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)

correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
game_over_image = pygame.image.load("mouse.jpg")
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (55, 50))
heart_image.set_colorkey((255, 255, 255))
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

words_and_translations = {
"apple": "яблоко",
    "banana": "банан",
    "cat": "кошка",
    "dog": "собака",
    "house": "дом",
    "tree": "дерево",
    "bird": "птица",
    "fish": "рыба",
    "flower": "цветок",
    "fruit": "фрукт",
    "vegetable": "овощ",
    "car": "машина",
    "boat": "лодка",
    "train": "поезд",
    "bicycle": "велосипед",
    "book": "книга",
    "pencil": "карандаш",
    "paper": "бумага",
    "school": "школа",
    "teacher": "учитель",
    "student": "ученик",
    "friend": "друг",
    "family": "семья",
    "mother": "мама",
    "father": "папа",
    "son": "сын",
    "daughter": "дочь",
    "country": "страна",
    "city": "город",
    "village": "деревня",
    "world": "мир",
    "sun": "солнце",
    "moon": "луна",
    "star": "звезда",
    "sky": "небо",
    "cloud": "облако",
    "rain": "дождь",
    "snow": "снег",
    "wind": "ветер",
    "hot": "горячий",
    "cold": "холодный",
    "big": "большой",
    "small": "маленький",
    "love": "любовь",
    "peace": "мир",
    "friendship": "дружба",
    "hope": "надежда",
    "dream": "мечта",
    "life": "жизнь",
    "death": "смерть",
    "time": "время",
    "space": "пространство",
    "universe": "вселенная",
    "nature": "природа",
    "science": "наука",
    "art": "искусство",
    "music": "музыка",
    "literature": "литература",
    "history": "история",
    "philosophy": "философия",
    "mathematics": "математика",
    "physics": "физика",
    "chemistry": "химия",
    "biology": "биология",
    "medicine": "медицина",
    "technology": "технология",
    "law": "закон",
    "society": "общество",
    "culture": "культура",
    "education": "образование",
    "sport": "спорт",
    "game": "игра",
    "fun": "веселье",
    "happiness": "счастье",
}

#переменные для управления игрой
current_word = ""
feedback = ""
feedback_color = TEXT_COLOR
feedback_alpha = 255
feedback_showing = False
feedback_delay = 1000
feedback_start_time = 0
alpha_change_rate = 2

#переменные для управления жизнями
lives = 5
heart_scale = 1.0
correct_answers = 0

#координаты и размеры кнопки Check
button_width = 120
button_height = 50
button_x = screen_width / 2 - button_width - 10
button_y = 350

#координаты и размеры кнопки Skip
skip_button_x = screen_width / 2 + 10
skip_button_y = 350
skip_button_width = 120
skip_button_height = 50

#переменная для хранения текста ввода
input_rect = pygame.Rect(screen_width / 2 - 150, 250, 300, 50)

#скорость движения фона
background_speed = 1

#переменная для хранения текущего смещения фона по оси X
background_image_x = 0

support_messages_en = ["Go ahead!", "Don't give up!", "You can do it!", "Don't worry!", "Keep trying!"]

#переменные для анимации сообщений поддержки
support_message_en = ""
support_message_color_en = TEXT_COLOR
support_message_alpha_en = 255
support_message_showing_en = False
support_message_delay_en = 1000
support_message_start_time_en = 0


#выбор нового слова и его перевода
def new_word():
    return random.choice(list(words_and_translations.items()))
word, translation = new_word()

#главный цикл приложения
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_over = False
                lives = 5
                correct_answers = 0
                word, translation = new_word()
        elif not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x < event.pos[0] < button_x + button_width and button_y < event.pos[1] < button_y + button_height:
                    #логика проверки ответа и выбор нового слова
                    feedback_showing = True
                    feedback_start_time = pygame.time.get_ticks()
                    if current_word.lower() == translation.lower():
                        correct_sound.play()
                        feedback = "Correct!"
                        feedback_color = CORRECT_COLOR
                        correct_answers += 1
                    else:
                        wrong_sound.play()
                        feedback = f"Wrong! Correct: {translation}"
                        feedback_color = WRONG_COLOR
                        lives -= 1
                        #при неправильном ответе выбираем случайное сообщение поддержки
                        support_message_en = random.choice(support_messages_en)
                        support_message_showing_en = True
                        support_message_start_time_en = pygame.time.get_ticks()
                    current_word = ""
                    if lives > 0:
                        word, translation = new_word()
                    else:
                        game_over = True
                elif skip_button_x < event.pos[0] < skip_button_x + skip_button_width and skip_button_y < event.pos[1] < skip_button_y + skip_button_height:
                    #пропустить слово
                    word, translation = new_word()
                    current_word = ""
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_word = current_word[:-1]
                elif event.key == pygame.K_RETURN and not game_over:
                    feedback_showing = True
                    feedback_start_time = pygame.time.get_ticks()
                    if current_word.lower() == translation.lower():
                        correct_sound.play()
                        feedback = "Correct!"
                        feedback_color = CORRECT_COLOR
                        correct_answers += 1
                    else:
                        wrong_sound.play()
                        feedback = f"Wrong! Correct: {translation}"
                        feedback_color = WRONG_COLOR
                        lives -= 1
                        #при неправильном ответе выбираем случайное сообщение поддержки
                        support_message_en = random.choice(support_messages_en)
                        support_message_showing_en = True
                        support_message_start_time_en = pygame.time.get_ticks()
                    current_word = ""
                    if lives > 0:
                        word, translation = new_word()
                    else:
                        game_over = True
                elif event.unicode.isalpha():
                    current_word += event.unicode

    #движение фона
    background_image_x -= background_speed
    if background_image_x <= -screen_width:
        background_image_x = 0

    screen.blit(background_image, (background_image_x, 0))
    screen.blit(background_image, (background_image_x + screen_width, 0))  #дополнительное изображение для плавного перехода

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_hover = button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height
    skip_button_hover = skip_button_x < mouse_x < skip_button_x + skip_button_width and skip_button_y < mouse_y < skip_button_y + skip_button_height

    if not game_over:
        font = pygame.font.Font(None, 50)
        word_surface = font.render(word, True, TEXT_COLOR)
        input_box_surf = font.render(current_word, True, TEXT_COLOR, BACKGROUND_COLOR)
        input_box_surf.set_alpha(255)
        screen.blit(word_surface, (screen_width / 2 - word_surface.get_width() / 2, 100))
        pygame.draw.rect(screen, TEXT_COLOR, input_rect, 2)
        screen.blit(input_box_surf, (input_rect.x + 5, input_rect.y + 5))

        button_color = BUTTON_HOVER_COLOR if button_hover else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_text_surf = font.render("Check", True, TEXT_COLOR)
        screen.blit(button_text_surf, (button_x + (button_width - button_text_surf.get_width()) / 2, button_y + (button_height - button_text_surf.get_height()) / 2))

        skip_button_color = BUTTON_HOVER_COLOR if skip_button_hover else BUTTON_COLOR
        pygame.draw.rect(screen, skip_button_color, (skip_button_x, skip_button_y, skip_button_width, skip_button_height))
        skip_button_text_surf = font.render("Skip", True, TEXT_COLOR)
        screen.blit(skip_button_text_surf, (skip_button_x + (skip_button_width - skip_button_text_surf.get_width()) / 2, skip_button_y + (skip_button_height - skip_button_text_surf.get_height()) / 2))

        for i in range(lives):
            scaled_heart_image = pygame.transform.scale(heart_image, (int(55 * heart_scale), int(50 * heart_scale)))
            screen.blit(scaled_heart_image, (20 + i * 60, 20))

        if feedback_showing:
            current_time = pygame.time.get_ticks()
            if current_time - feedback_start_time < feedback_delay:
                feedback_alpha = 255
            elif current_time - feedback_start_time - feedback_delay < 2000:
                feedback_alpha -= alpha_change_rate if feedback_alpha > 0 else 0
            else:
                feedback_showing = False
                feedback_alpha = 255
            feedback_surf = font.render(feedback, True, feedback_color)
            feedback_surf.set_alpha(feedback_alpha)
            screen.blit(feedback_surf, (screen_width / 2 - feedback_surf.get_width() / 2, 420))

        if support_message_showing_en:
            current_time_en = pygame.time.get_ticks()
            if current_time_en - support_message_start_time_en < support_message_delay_en:
                support_message_alpha_en = 255
            elif current_time_en - support_message_start_time_en - support_message_delay_en < 2000:
                support_message_alpha_en -= alpha_change_rate if support_message_alpha_en > 0 else 0
            else:
                support_message_showing_en = False
                support_message_alpha_en = 255
            support_message_surf_en = font.render(support_message_en, True, support_message_color_en)
            support_message_surf_en.set_alpha(support_message_alpha_en)
            screen.blit(support_message_surf_en, (screen_width - support_message_surf_en.get_width() - 20, 20))
    else:
        screen.blit(game_over_image, (screen_width / 2 - game_over_image.get_width() / 2, screen_height / 2 - game_over_image.get_height() / 2))
        game_over_text = pygame.font.Font(None, 72).render("GAME OVER! Press R to restart", True, GAME_OVER_COLOR)
        screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 + game_over_image.get_height() / 2 + 30))

    correct_text = font.render(f"Correct: {correct_answers}", True, TEXT_COLOR)
    screen.blit(correct_text, (20, screen_height - 50))
    pygame.display.flip()

pygame.quit()
sys.exit()