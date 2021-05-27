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

- The app works smoothly on OSX, but flickers on Linux when you move the lens.
- Some people have found issues when using two screens. It is tested with two screens
  on OSX, but not yet on Linux. Please leave an issue if it does not work for you.
- Pulling the window to another screen is currently not supported. To switch screens,
  you need to run `monolens` from a terminal on that screen (this works on OSX at least).
  This limitation will hopefully be lifted in the near future.
- The lens uses a static screenshot which has to be manually updated if the screen
  content changed. Press spacebar to update the lens.
- On OSX, you need to give `monolens` permission to make screenshots, since an ordinary
  app is not allowed to read pixels outside of its window for security reasons.
  `monolens` is safe to use because it has no networking code implemented at all.

# For developers

- You can run monolens without installing it from the project folder via
  `python -m monolens`. You need to install `pyside6` manually then.
