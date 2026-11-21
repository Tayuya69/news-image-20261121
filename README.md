# The World Today — Saturday 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Tayuya69/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Tayuya69/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121):
one image summing up the world's news of Saturday 21 November 2026, drawn as a
newspaper front page.

## The day, in five stories

- **War in Europe (lead):** Russia fires more than 400 drones and 110 missiles
  at Ukraine overnight; at least eight killed in Kyiv, and missiles land in
  Poland — Warsaw calls it a deliberate provocation.
- **Markets:** an AI sell-off drags stocks into correction — S&P 500 down 3.7%,
  Nasdaq 5.3%, Nikkei 5.1%.
- **Climate:** COP31 in Antalya deadlocks over fossil fuels and runs past its
  deadline.
- **Cyber:** the FBI's criminal database is reportedly hacked as US computer
  outages continue.
- **Disaster:** a magnitude 6.9 earthquake shakes Peru's Andes; felt in Lima,
  no casualties reported.

Plus an in-brief strip: UK–EU post-Brexit deals, the Palisades fire conviction,
and Bayer's $7.25bn Roundup settlement.

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
