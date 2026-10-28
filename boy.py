from pico2d import (
    get_time, load_image,
    SDL_KEYDOWN, SDL_KEYUP,
    SDLK_LEFT, SDLK_RIGHT, SDLK_a,
)
from transitions import Machine


SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
SPRITE_COLUMNS = 8
IDLE_FRAMES = SPRITE_COLUMNS
IDLE_FPS = 8.0
RUN_FRAMES = SPRITE_COLUMNS
RUN_FPS = 12.0
MOVE_SPEED = 300.0
AUTO_RUN_SPEED = 450.0
AUTO_RUN_SIZE = 150
AUTO_RUN_LIMIT = 5.0
SLEEP_AFTER = 5.0
SLEEP_DRAW_Y = 55
CANVAS_LEFT = 50
CANVAS_RIGHT = 750

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0.0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.previous_time = get_time()
        self.idle_time = 0.0

        self.pressed_keys = set()
        self.auto_run_time = 0.0

        self.state_machine = Machine(
            model=self,
            states=['IDLE', 'RUN_LEFT', 'RUN_RIGHT', 'AUTO_RUN', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
        )
        self.state_machine.add_transition('animate', 'IDLE', None, after='update_idle')
        self.state_machine.add_transition('animate', 'RUN_LEFT', None, after='update_run_left')
        self.state_machine.add_transition('animate', 'RUN_RIGHT', None, after='update_run_right')
        self.state_machine.add_transition('animate', 'AUTO_RUN', None, after='update_auto_run')
        self.state_machine.add_transition('animate', 'SLEEP', None, after='update_sleep')
        self.state_machine.add_transition('move_left', '*', 'RUN_LEFT', before='face_left')
        self.state_machine.add_transition('move_right', '*', 'RUN_RIGHT', before='face_right')
        self.state_machine.add_transition('start_auto_run', ['IDLE', 'AUTO_RUN'], 'AUTO_RUN', before='reset_auto_run')
        self.state_machine.add_transition('stop_auto_run', 'AUTO_RUN', 'IDLE', before='reset_idle')
        self.state_machine.add_transition('stop', ['RUN_LEFT', 'RUN_RIGHT'], 'IDLE', before='reset_idle')
        self.state_machine.add_transition('sleep', ['IDLE', 'RUN_LEFT', 'RUN_RIGHT'], 'SLEEP', before='enter_sleep')
        self.state_machine.add_transition('wake_up', 'SLEEP', 'IDLE', before='reset_idle')

    def face_left(self):
        self.face_dir = -1
        self.idle_time = 0.0

    def face_right(self):
        self.face_dir = 1
        self.idle_time = 0.0

    def reset_auto_run(self):
        self.auto_run_time = 0.0
        self.idle_time = 0.0

    def enter_sleep(self):
        self.pressed_keys.clear()
        self.frame = 0.0
        self.idle_time = 0.0

    def reset_idle(self):
        self.frame = 0.0
        self.idle_time = 0.0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a and self.state == 'IDLE':
                self.start_auto_run()
                return

            if event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.pressed_keys.add(event.key)
                if self.state == 'SLEEP':
                    self.wake_up()
                if event.key == SDLK_LEFT:
                    self.move_left()
                else:
                    self.move_right()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_keys.discard(event.key)
            if not self.pressed_keys and self.state in ('RUN_LEFT', 'RUN_RIGHT'):
                self.stop()
            elif SDLK_LEFT in self.pressed_keys:
                self.move_left()
            elif SDLK_RIGHT in self.pressed_keys:
                self.move_right()

    def update_idle(self, frame_time):
        self.frame = (self.frame + IDLE_FPS * frame_time) % IDLE_FRAMES
        self.idle_time += frame_time

    def update_run_left(self, frame_time):
        self.frame = (self.frame + RUN_FPS * frame_time) % RUN_FRAMES
        self.face_dir = -1
        self.x = max(50, self.x - MOVE_SPEED * frame_time)
        self.idle_time = 0.0

    def update_run_right(self, frame_time):
        self.frame = (self.frame + RUN_FPS * frame_time) % RUN_FRAMES
        self.face_dir = 1
        self.x = min(750, self.x + MOVE_SPEED * frame_time)
        self.idle_time = 0.0

    def update_auto_run(self, frame_time):
        self.frame = (self.frame + RUN_FPS * frame_time) % RUN_FRAMES
        self.auto_run_time += frame_time
        self.idle_time = 0.0
        self.x += AUTO_RUN_SPEED * frame_time * self.face_dir

        if self.x <= CANVAS_LEFT:
            self.x = CANVAS_LEFT
            self.face_dir = 1
        elif self.x >= CANVAS_RIGHT:
            self.x = CANVAS_RIGHT
            self.face_dir = -1

    def update_sleep(self, frame_time):
        pass

    def update(self):
        current_time = get_time()
        frame_time = current_time - self.previous_time
        self.previous_time = current_time
        self.animate(frame_time)

        if self.state == 'AUTO_RUN' and self.auto_run_time >= AUTO_RUN_LIMIT:
            self.stop_auto_run()
        elif self.state == 'IDLE' and self.idle_time >= SLEEP_AFTER:
            self.sleep()

    def draw(self):
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(
                0, 300, 100, 100,
                -1.5707963267948966, '',
                self.x, SLEEP_DRAW_Y, 100, 100,
            )
        elif self.state == 'AUTO_RUN':
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(
                int(self.frame) * 100, row, 100, 100,
                self.x, self.y + 25, AUTO_RUN_SIZE, AUTO_RUN_SIZE,
            )
        elif self.state == 'RUN_RIGHT':
            self.image.clip_draw(int(self.frame) * 100, 100, 100, 100, self.x, self.y)
        elif self.state == 'RUN_LEFT':
            self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, self.x, self.y)
        elif self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, self.x, self.y)

