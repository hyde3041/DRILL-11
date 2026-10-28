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


if __name__ == '__main__':
    unittest.main()
