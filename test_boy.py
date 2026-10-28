import sys
import types
import unittest


pico2d = types.ModuleType('pico2d')
pico2d.get_time = lambda: 0.0
pico2d.load_image = lambda path: object()
pico2d.SDL_KEYDOWN = 2
pico2d.SDL_KEYUP = 3
pico2d.SDLK_LEFT = 80
pico2d.SDLK_RIGHT = 79
pico2d.SDLK_a = 97
sys.modules['pico2d'] = pico2d

from boy import Boy


class BoyStateTests(unittest.TestCase):
    def setUp(self):
        self.boy = Boy()

    def test_starts_idle(self):
        self.assertEqual(self.boy.state, 'IDLE')

    def test_auto_run_starts_from_idle(self):
        self.boy.start_auto_run()
        self.assertEqual(self.boy.state, 'AUTO_RUN')

    def test_auto_run_reverses_at_right_edge(self):
        self.boy.start_auto_run()
        self.boy.x = 750
        self.boy.face_dir = 1
        self.boy.update_auto_run(0.1)
        self.assertEqual(self.boy.face_dir, -1)

    def test_sleep_enters_from_idle(self):
        self.boy.sleep()
        self.assertEqual(self.boy.state, 'SLEEP')


if __name__ == '__main__':
    unittest.main()
