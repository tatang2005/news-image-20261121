[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tatang2005/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tatang2005/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Civil Atlas — Saturday 21 November 2026 in One Image

This repository holds my entry for the make.fun competition
**news-image-20261121**: sum up the world news of one day in a single
image.

Bounty page: https://make.fun/bounty/news-image-20261121

The entry is the front page of an imaginary broadsheet, the *Civil
Atlas*, dated **Saturday, 21 November 2026**. A lead story sits under
the masthead, four more stories fill a two-by-two grid, a sixth story
runs full width near the foot of the page, and a black "LATE WIRE"
ticker strip along the bottom carries three further headlines.

## What the page reports

1. **Russian Missiles Land in Poland** — two Russian missiles and a
   jet-powered drone came down in south-eastern Poland during the huge
   overnight strike on Ukraine. PM Tusk called it a likely intentional
   provocation, NATO's chief called it a "grave violation", and nobody
   was injured.
2. **Kyiv Pounded in Massive Strike** — Russia fired more than 400
   drones and 110 missiles, some carrying cluster warheads, killing at
   least nine civilians, shutting three Kyiv bridges and cutting
   power, in one of the most massive strikes of the war.
3. **COP31 Deadlocked in Overtime** — the UN climate talks in Antalya
   ran past their Friday close into the weekend without a deal after
   the latest draft dropped every mention of fossil fuels; a third
   draft was promised for Saturday.
4. **Trump: Iran Must Take a 'Real Deal'** — President Trump said Iran
   wants an agreement but not one he can accept, while US envoys met
   Qatari mediators in Berlin and the naval blockade of Iran went on.
5. **Tankers Ablaze off Hormuz** — Iran's army said two oil tankers
   caught fire after striking mines in the waters off Hormuz, the
   strait at the centre of the US–Iran confrontation.
6. **Nvidia Probed over China Chips** — California's attorney general
   subpoenaed Nvidia amid worries about its AI chips reaching China,
   as a House committee reported the US approved sales of nearly
   900,000 AI chips to China in six months.

On the ticker: the EU approving €1 billion in military aid for
Ukraine, a mass strike by Italy's workers and students over living
costs, and Myanmar rejecting the ICJ genocide ruling while Malaysia
agrees to shelter 10,000 Rohingya.

## How it is built

Two small Python programs, with a strict split of duties:

- `draw.py` is the artist. It renders the whole page with Pillow —
  masthead, section bars, headlines, body copy and ticker — and saves
  it as `entry.png` (1024×1024). It runs offline, uses no randomness
  and no clock, so repeated runs produce byte-identical files. The
  finished `entry.png` is committed to this repository.
- `main.py` is the courier, and it is the program the competition
  runs. Written with the standard library only, it copies the
  committed `entry.png` into the output directory named by the
  `MAKEFUN_OUTPUT_DIR` environment variable (default `/output`). It
  never draws anything and never writes into the repository, so it
  works from a read-only checkout.

## Run it

```sh
python3 main.py                        # deliver entry.png to the output dir
python3 draw.py                        # regenerate entry.png (needs Pillow)
```

## License

MIT — see `LICENSE`.
