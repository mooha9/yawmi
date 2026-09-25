Your job: refresh the morning news brief of the «يومي» app. Edit only the file src/news.json in the current folder.

1. Today's date in Riyadh is given at the end of this message. Read CLAUDE.md and the current src/news.json. It is the exact schema and style to reproduce.

2. Research with WebSearch and WebFetch. Use only news from the last 24-48 hours:
   - Saudi market (TASI): the latest session close, the change in points and %, the main movers, and the oil and news drivers. Sources: argaam.com/ar, saudiexchange.sa, mubasher, tradingeconomics. Tadawul trades Sun-Thu 10:00-15:00 and is closed on Fri/Sat and on holidays. If it is closed, summarize the last session and say when it reopens.
   - US market: the previous session's closes for the S&P 500, Nasdaq and Dow, Treasury yields, the Fed, the main movers, and what to watch today. If the market was closed (weekend/holiday), summarize the last session. Sources: cnbc, yahoo finance, thestreet, apnews/abcnews, reuters.
   - Crypto: BTC and ETH price and 24h change this morning, plus the main driver. Sources: coindesk, fortune, yahoo finance, coinmarketcap.
   - AI: 6-8 of the most important AI stories of the past day. Sources: theneuron.ai, buildfastwithai, techcrunch, the verge, reuters, official company blogs.
   If a page returns 403, try another source. Never invent or estimate a number. Every figure must come from a page you actually read. If you cannot confirm a figure, leave it out.

3. Rewrite src/news.json completely in Arabic, following the same schema:
   - date = today's Riyadh date (YYYY-MM-DD). label like «الجمعة ٢٥ سبتمبر ٢٠٢٦ · صباحاً».
   - markets in the order sa, us, crypto. Each has: headline (one line), figures (2-3 triples [name, value, change]; the change starts with «−» or «+», or is «مستقر»), points (4-5 short factual sentences), watch (one sentence), and sources (2-4 pairs [short Arabic title, URL]).
   - ai: headline, items (6-8 pairs [short tag, 1-2 sentences]), forYou (one sentence that turns one of today's stories into a practical AI app idea that benefits Saudi/Arab society), and sources (3-5).
   - Use Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) with ٬ for thousands and ٫ for decimals. Keep product and company names in Latin script. Write plain, clear Arabic with no hype.
   - The file must be valid JSON.

4. Do not change any other file. Finish with one Arabic line containing the day's headlines.
