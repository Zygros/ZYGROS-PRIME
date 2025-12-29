# Termux scheduled jobs (cronie)

1) Install: `pkg install cronie` then `sv-enable crond`
2) Edit your crontab: `crontab -e`
   Example jobs:
   - Run backup every 6h:
     `0 */6 * * * $HOME/vault_backup_sync.sh >> $HOME/backup.log 2>&1`
   - Weekly dedupe scan:
     `0 2 * * 0 python $HOME/dedupe_scan.py >> $HOME/dedupe.log 2>&1`

Logs are in your home directory. Use `tmux` for long sessions.
