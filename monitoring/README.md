# monitoring

The stack that watches the lab. Runs in an LXC container on a second physical host, deliberately not on the machine it monitors.

| File | What it is |
| --- | --- |
| `prometheus.yml` | Scrape config. 12 targets across three subnets, plus blackbox probes against the public site |
| `node_alerts.yml` | Host health rules |
| `storage_alerts.yml` | Drive temperature and pool health rules |
| `site_alerts.yml` | Uptime, response time and TLS certificate expiry for steven-garcia.dev |
| `blackbox.yml` | Probe module config |
| `pool-health.sh` | Textfile collector. Reports ZFS pool health for both pools, including the one inside a guest VM |
| `pool-health.service` / `.timer` | Runs the collector every five minutes |

## Two rules worth explaining

**`HostProcessesBlocked`** watches `node_procs_blocked`. A backup job once hung the hypervisor for 38 hours at load 45 with the CPU 96 percent idle, because forty processes were stuck in uninterruptible sleep on a dead NFS mount. A conventional load alert compares load average against CPU count, which on 88 cores means a threshold near 88, so it would never have fired. Counting blocked processes catches it in ten minutes.

**`DriveTemperatureHigh`** reads SMART on the hypervisor rather than inside the storage VM. Four SAS drives ran at 51 to 56 C for a month while three separate monitoring layers reported nothing, because virtio passes block devices but not the SCSI command set SMART rides on. The collector has to live where the controller is. Temperatures come from the `prometheus-node-exporter-collectors` package.

## Why the timeout in pool-health.sh

The script reads pool health inside the storage guest through the QEMU guest agent, wrapped in `timeout 25`. That command is exactly what hung during the incident above. A collector that blocks on the thing it monitors is the same circular dependency that caused the outage, just smaller.

## Not here

`alertmanager.yml` contains a live Discord webhook and stays out of version control.
