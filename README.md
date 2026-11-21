[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tatang2005/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tatang2005/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

My entry for the make.fun competition **news-image-20261121**: a single
image that sums up the world's news of Saturday 21 November 2026.

Bounty page: https://make.fun/bounty/news-image-20261121

The image is a newspaper front page — "The Daily Wire" — with a dated
masthead (Saturday, 21 November 2026), six story panels, and a black
"LATE WIRE" ticker strip along the bottom carrying three more of the
day's stories.

## The six stories

1. **Russian Missiles Land in Poland** — two Russian missiles and a
   jet-powered drone came down in south-eastern Poland during the giant
   overnight strike on Ukraine. PM Tusk called it a likely intentional
   provocation; NATO's chief called it a "grave violation". Nobody was
   hurt.
2. **Kyiv Pounded in Massive Strike** — Russia fired more than 400
   drones and 110 missiles, some with cluster warheads, killing at
   least nine people, crippling Kyiv's bridges and cutting power across
   nine regions, in retaliation for the destruction of the Kerch Bridge.
3. **COP31 Deadlocked in Overtime** — the UN climate talks in Antalya
   ran past their Friday close into the weekend with no deal, after the
   latest draft dropped every mention of fossil fuels. A third draft
   was promised for Saturday morning.
4. **Trump: Iran Must Take a 'Real Deal'** — President Trump said Iran
   wants an agreement but not one he can accept, demanding a "real
   deal", while US envoys met Qatari mediators in Berlin and the naval
   blockade of Iran ground on.
5. **Two Tankers Ablaze off Hormuz** — Iran's army said two oil
   tankers burst into flames after striking mines in the waters off
   Hormuz, the strait at the heart of the US–Iran confrontation.
6. **Nvidia Probed over China Chips** — California's attorney general
   subpoenaed Nvidia amid worries over its AI chips reaching China,
   while a House committee reported the US approved sales of nearly
   900,000 AI chips to China in six months.

Ticker: the EU approving €1 billion more in military aid for Ukraine,
Italian workers and students walking out over living costs, and Myanmar
rejecting the ICJ genocide verdict as Malaysia agrees to take 10,000
Rohingya.

## How it works

- `draw.py` renders the whole page with Pillow: masthead, six panels
  with hand-drawn icon illustrations (missile over the Polish flag, a
  broken bridge under a blast, a globe with a thermometer, a rejected
  deal document, a burning tanker, an AI chip), and the ticker strip.
  The output is deterministic: running it twice gives byte-identical
  files.
- `main.py` is the entry program: it renders the page and writes
  `entry.png` (1024x1024) next to itself and, when available, into
  `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## Run

```sh
python3 main.py
```

## License

MIT — see `LICENSE`.
