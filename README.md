# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/gom92/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/gom92/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image, one day of world news. This front page covers Tuesday 24 November 2026: NATO moves AWACS aircraft to Poland after Russian missiles land there, Ukraine sinks a Russian warship off Libya, plus the day's key numbers and six short briefs.

## How it is made

- `tools/render_frontpage.py` draws the 1024x1024 page with Pillow. Every word on the page is drawn by Pillow; the two pictures in `assets/` are AI-generated illustrations without any text.
- `main.py` checks `entry.png` and copies it to the grading location, byte for byte.
- Headlines and figures come from mainstream reporting on the day (Reuters, CNN, WSJ, Formula 1).

## Run it

```sh
python3 tools/render_frontpage.py   # redraw entry.png
python3 main.py                     # copy entry.png to /output/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=radjee14&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
