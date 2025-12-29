# Anchor on Arweave (optional)
# Requires an Arweave keyfile (JWK) and the 'arbundles' or 'arweave' tooling.

## Using Bundlr (recommended)
# 1) Install:  npm i -g @bundlr-network/client
# 2) Fund:     bundlr fund 1000000  # (example units; requires wallet)
# 3) Upload seal:
bundlr upload seal.txt --content-type text/plain
# 4) Keep the returned transaction ID as your public reference.
