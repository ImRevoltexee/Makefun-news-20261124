# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ImRevoltexee/Makefun-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ImRevoltexee/Makefun-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper-style infographic summing up the world's news on
**Tuesday, 24 November 2026** — six front-page stories plus three
short "Also Today" items, drawn entirely in code with Pillow
(`draw.py` → `entry.png`, 1024×1024, deterministic).

## The six stories

| # | Headline | What happened |
|---|----------|---------------|
| 1 | Nvidia Brings Back Jensen Huang as CEO | Nvidia's board unanimously reinstated Jensen Huang as president and CEO, 11 days after he resigned; shares jumped about a third as President Trump backed the return. |
| 2 | Iran Hits U.S. Bases in Bahrain Again | Iran fired drones at a U.S. radar facility in Bahrain — its third strike on American targets there in three days — as a third U.S. carrier group sailed into the Gulf. |
| 3 | Russian Jets Trigger Alert Over South Korea | Several Russian military aircraft entered South Korea's air defence zone; fighters scrambled and Ulleung Island residents were briefly told to take shelter. |
| 4 | Ukraine Sinks Russian Warship off Libya | Ukrainian sea drones sank the Russian corvette Merkury at Benghazi and hit the cargo ship MV Angara, which Kyiv says carried weapons. |
| 5 | EU Unveils 22nd Sanctions Package | The European Commission proposed its 22nd sanctions package on Russia: a transaction ban on about 60 banks, crypto crackdowns, and a ban on Russian teams competing under the Russian flag in the EU. |
| 6 | Two U.S. States Sue SpaceX Over Grok | Virginia and Oregon sued SpaceX and its AI arm, alleging the Grok chatbot turned photos into non-consensual sexual images, including of children. |

## Also today

- **Mexico to try "El Chapo Isidro" at home** — despite a U.S. extradition order, Mexico says it will prosecute the captured cartel boss first.
- **24 dead in Indonesia factory fire** — rescuers still search for about 30 missing after the Banten candy plant blaze.
- **Spain's right on course for majority** — final polls before Sunday's vote put the PP and Vox past 176 seats.

## How it was made

```sh
python3 draw.py    # regenerates entry.png (byte-identical every run)
python3 main.py    # validates entry.png and writes it to /output/entry.png
```

`main.py` uses only the Python standard library. It accepts a whole PNG
or JPEG file of at most 1 MiB and 1024×1024 pixels, and exits non-zero
on anything else.

## Sources

Reuters, Associated Press, The Wall Street Journal, CNN, Al Jazeera,
European Commission, Aju Press, The Pen PK, Breitbart.
