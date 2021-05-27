# monolens

Show part of your screen in 8-bit grayscale.

[<img src="https://img.shields.io/pypi/v/monolens.svg">](https://pypi.org/project/monolens)

Watch the demo on YouTube.

[<img src="https://img.youtube.com/vi/f8FRBlSoqWQ/0.jpg">](https://youtu.be/f8FRBlSoqWQ)

# Usage

Install with `pip install monolens`. Then run `monolens` in a terminal on the screen that you want to look at.

- Drag the lens around by holding a Mouse button down inside the window
- Resize the lens by pressing up, down, left, right
- To quit, press Q or double click while hovering over the lens

# Known limitations

- The app works smoothly on OSX, but may flicker on Linux when you move the lens.
- Some people have found issues when using two screens. It is tested with two screens
  on OSX, but not yet on Linux. Please leave an issue if it does not work for you.
- Pulling the window to another screen is currently not supported. To switch screens,
  you need to run `monolens` from a terminal on that screen (this works on OSX at least).
  This limitation will hopefully be lifted in the near future.
- The lens actually uses a static screenshot which is periodically updated. Because of
  this pixels directly under the lens cannot be updated unless you move the lens away
  first from new content that you want to look at and then back.
- On OSX, you need to give `monolens` permission to make screenshots, since an ordinary
  app is not allowed to read pixels outside of its window for security reasons.
  `monolens` is safe to use because it has no networking code implemented at all.

# For developers

- You can run monolens without installing it from the project folder via
  `python -m monolens`. You need to install `pyside6` manually then.
