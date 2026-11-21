# The World Today — Saturday 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Tayuya69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Tayuya69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121):
one image summing up the world's news of Saturday 21 November 2026, drawn as a
newspaper front page. This is the second edition: a new composition led by the
Shenzhen summit, replacing the first edition's Kyiv-led page.

## The day, in five stories

- **Diplomacy — Shenzhen (lead):** after the first three-way meeting of the
  US, Chinese and Russian leaders, Trump defends his ties to Putin and Xi;
  the summit ends in a four-point joint peace declaration, silent on Ukraine.
- **Justice — The Hague:** the International Court of Justice finds Myanmar
  committed genocide against the Rohingya — the first time it has held a
  state responsible for genocide.
- **Markets — New York:** an AI sell-off drags stocks into correction —
  S&P 500 down 3.7%, Nasdaq 5.3%, Nikkei 5.1%.
- **War in Europe:** Russia fires more than 400 drones and 110 missiles at
  Ukraine overnight; at least eight killed in Kyiv, and two missiles land in
  Poland — NATO condemns the falls on Polish soil.
- **Health — London:** a trial of the pill daraxonrasib makes pancreatic
  cancer undetectable on scans in one in twelve patients.

Plus an in-brief strip: the reported FBI crime-database hack, the Peru quake,
the COP31 deadlock in Antalya, Trump's pardon of Pete Rose, and the storm
that killed three in southern Brazil.

Sources checked against reporting from 21 November 2026 (oneturn.news day
page, Standard Topic's world archive, Fox News, Dainik Jagran, Juba Global).

## How it is built

`draw.py` (Python 3 + Pillow, run at build time) draws the front page from
scratch — masthead, headlines, and every picture panel — and writes
`entry.png` (1024×1024, under 1 MiB). `main.ts` (Node 22, standard library
only) copies that image to `/output/entry.png`, deterministically:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
