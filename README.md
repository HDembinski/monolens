# monolens

Show part of your screen in 8-bit grayscale.

[<img src="https://img.shields.io/pypi/v/monolens.svg">](https://pypi.org/project/monolens)

Watch the demo on YouTube.

[<img src="https://img.youtube.com/vi/f8FRBlSoqWQ/0.jpg">](https://youtu.be/f8FRBlSoqWQ)

# Usage

Install with `pip install monolens`. Then run `monolens` in a terminal on the screen that you want to look at.

- Drag the lens around by holding a Mouse button down inside the window
- Resize the lens by pressing up, down, left, right
- To quit, press Escape, Q, or double click on the lens
- To move the lens to another screen, press S

# Known limitations

- The app is tested on OSX and Linux. It may flicker when you move the lens, if you know
  how to fix this, please help. :)
- Some people have found issues when using two screens, which are hopefully fixed now.
  Leave an issue if this problem appears.
- Pulling the lens to another screen is currently not supported. To switch screens,
  press S.
- The lens actually uses a static screenshot which is periodically updated. Because of
  this, pixels directly under the lens cannot be updated unless you move the lens away
  first from new content that you want to look at, and then back.
- On OSX, you need to give `monolens` permission to make screenshots, since an ordinary
  app is not allowed to read pixels outside of its window for security reasons.
  Doing this is safe; `monolens` has no networking code implemented at all.

# Future plans

- Support gestures and move to rescale the lens (pinch etc)
- Simulate color blindness
- Add a splash screen with a "do not show again" to explain usage.

# For developers

- You can run monolens without installing it from the project folder via
  `python -m monolens`. You need to install `pyside6` manually then.
