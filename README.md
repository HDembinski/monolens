# monolens

Show part of your screen monochrome or in simulated deuteranopia, protanopia, or tritanopia.

[<img src="https://img.shields.io/pypi/v/monolens.svg">](https://pypi.org/project/monolens)

Watch the demo on YouTube.

[<img src="https://img.youtube.com/vi/f8FRBlSoqWQ/0.jpg">](https://youtu.be/f8FRBlSoqWQ)

Install with `pip install monolens` and then run `monolens` in a terminal or do it in one
command with or `pipx run monolens`.

# Usage

<!-- usage begin -->

- Drag the lens around by holding a Mouse button down inside the window
- To quit, press Escape, Q, or double click on the lens
- Resize the lens by pressing up, down, left, right
- Press T to switch through simulated monochromacy, deuteranopia, protanopia, tritanopia
- To move the lens to another screen, press S
- On OSX, you need to give Monolens permission to make screenshots, which is safe.

<!-- usage end -->

# Known limitations

- The app is tested on OSX and Linux. It may flicker when you move the lens (less so on
  OSX). If you know how to fix this, please help. :)
- Pulling the lens to another screen is currently not supported. Press S to switch screens
  instead.
- The lens actually uses a static screenshot which is updated as you move the lens around.
  This trick is necessary, because an app cannot read the pixels under its own window.
  Because of this, the pixels under the app are only updated when you move the lens away
  first and then back.
- On OSX, an ordinary app is not allowed to read pixels outside of its window for security
  reasons, which is why this app needs special permissions. Doing this is safe; Monolens
  contains no networking code and will neither store nor send your pixels anywhere.

# Future plans

- Support gestures to rescale the lens (pinch etc)
