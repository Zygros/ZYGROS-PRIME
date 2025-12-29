# Anchor hint on Bitcoin (optional; technical)
# The robust approach is OpenTimestamps (already included).
# If you still want a raw on-chain OP_RETURN, use a wallet or bitcoin-cli with a funded address.
# Example (advanced users only):
#   bitcoin-cli createrawtransaction "[]" '[{"data":"<hex-encoded-bytes-of-hash>"}]'
#   ...
# Many wallets expose 'OP_RETURN' note fields; paste the SHA-512 or a short hash (SHA-256) due to size.
