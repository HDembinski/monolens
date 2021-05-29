# monolens

Show part of your screen in 8-bit grayscale.

[<img src="https://img.shields.io/pypi/v/monolens.svg">](https://pypi.org/project/monolens)

Watch the demo on YouTube.

[<img src="https://img.youtube.com/vi/f8FRBlSoqWQ/0.jpg">](https://youtu.be/f8FRBlSoqWQ)

Install with `pip install monolens` and then run `monolens` in a terminal or do it in one command with or `pipx run monolens`.

# Usage

<!-- usage begin -->

- Drag the lens around by holding a Mouse button down inside the window
- Resize the lens by pressing up, down, left, right
- To quit, press Escape, Q, or double click on the lens
- To move the lens to another screen, press S
- On OSX, you need to give Monolens permission to make screenshots, which is safe.

<!-- usage end -->

# Known limitations

- The app is tested on OSX and Linux. It may flicker when you move the lens (less so on
  OSX). If you know how to fix this, please help. :)
- Pulling the lens to another screen is currently not supported. To switch screens,
  press S.
- The lens actually uses a static screenshot which is updated as you move the lens around.
  This trick is necessary, because an app cannot read the pixels under its own window.
  Because of this, the pixels under the app are only updated when you move the lens away
  first and then back.
- On OSX, an ordinary app is not allowed to read pixels outside of its window for security
  reasons. Doing this is safe; Monolens has no networking code implemented at all and
  will not store or send information about your pixels anywhere.

# Future plans

- Support gestures to rescale the lens (pinch etc)
- Add filters that simulate color blindness as well
- Add a splash screen with a "do not show again" to explain usage.

# For developers

- You can run Monolens without installing it from the project folder via
  `python -m monolens`. You need to install `pyside6` manually then.
