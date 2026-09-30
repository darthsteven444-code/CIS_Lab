#!/usr/bin/env bash
set -u
OUT=/var/lib/prometheus/node-exporter/pools.prom
TMP=$(mktemp)

{
  echo "# HELP zpool_healthy 1 when the pool reports ONLINE"
  echo "# TYPE zpool_healthy gauge"

  for p in $(zpool list -H -o name 2>/dev/null); do
    h=$(zpool list -H -o health "$p")
    v=0; [ "$h" = ONLINE ] && v=1
    echo "zpool_healthy{pool=\"$p\",host=\"proxmox\"} $v"
  done

  th=$(timeout 25 qm guest exec 130 --timeout 20 -- /usr/sbin/zpool list -H -o health tank 2>/dev/null | grep -oE 'ONLINE|DEGRADED|FAULTED|UNAVAIL|OFFLINE|REMOVED' | head -1)
  if [ -n "${th:-}" ]; then
    v=0; [ "$th" = ONLINE ] && v=1
    echo "zpool_healthy{pool=\"tank\",host=\"truenas\"} $v"
  fi
} > "$TMP"

chmod 644 "$TMP"
mv "$TMP" "$OUT"
