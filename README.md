# monolens

Show part of your screen in 8-bit grayscale.

![Click to watch demo](https://github.com/HDembinski/monolens/blob/main/demo.mov?raw=true)

# Usage

Install with `pip install monolens`. Then run `monolens` in a terminal on the screen that you want to look at.

- Drag the lens around by holding a Mouse button down inside the window
- Resize the lens by pressing up, down, left, right
- To refresh the lens press the spacebar (see limitations)
- To quit, press Q

# Known limitations

- The app currently only works smoothly on OSX, it glitches on Linux.
- Pulling the window to another screen is currently not supported. To switch screens,
  you need to run `monolens` from a terminal on that screen. This limitation will
  hopefully be lifted in the future.
- The lens uses a static screenshot which has to be manually updated if the screen
  content changed. Press spacebar to update the lens (which causes it to flicker).
- On OSX, you need to give `monolens` permission to make screenshots, since an ordinary
  App is not allowed to read pixels outside of its window for security reasons.
  `monolens` is safe to use because it has no networking code implemented at all.

# For developers

- One can run monolens without installing it from the project folder via
  `python -m monolens`. You need to install `pyside6` manually then.
