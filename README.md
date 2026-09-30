# CIS_Lab

The configs, scripts and runbooks behind a home lab running 17 VMs, a three node Kubernetes cluster, a SIEM and a public website, on server hardware that was decommissioned before I owned it.

I am a Navy veteran and a CIS student. This repo is the working parts. The stories live at [steven-garcia.dev](https://steven-garcia.dev), including the incidents where I had the wrong answer first.

## What the lab is

| Layer | What runs there |
| --- | --- |
| Hypervisor | Proxmox VE, Dell Precision T7910, dual Xeon E5-2699 v4, 128 GB |
| Network | OPNsense, five VLANs, zero inbound ports open |
| Storage | TrueNAS SCALE, four wide RAIDZ1, 10.44 TiB usable |
| Compute | k3s on three nodes, plus an Oracle Cloud cluster built with Terraform |
| Security | Wazuh SIEM, seven agents |
| Monitoring | Prometheus, Grafana, Alertmanager, blackbox, on separate physical hardware |
| Public | steven-garcia.dev, served active active from both clusters through one Cloudflare tunnel |

## What is in here

### monitoring/

The stack that watches everything, including the hypervisor. Two rules in here exist because of specific failures:

`HostProcessesBlocked` watches `node_procs_blocked`. A backup job once hung my hypervisor for 38 hours at load 45 with the CPU 96 percent idle. A normal load alert compares load against CPU count, which on 88 cores means a threshold near 88, so it would never have fired. Counting blocked processes would have caught it in ten minutes.

`DriveTemperatureHigh` reads SMART on the Proxmox host rather than inside the storage VM. Four SAS drives cooked at 51 to 56 C for a month while three separate monitoring layers reported nothing, because virtio passes block devices but not the SCSI command set SMART rides on. The collector has to live where the controller is.

### rca/

Prometheus detects a pod failure, Alertmanager posts to a webhook receiver, a local LLM reads the pod spec, events and logs, and a structured root cause analysis lands in Discord without anyone asking for it.

### runbooks/

Procedures written during or immediately after real incidents, while the details were still exact.

### scripts/

Small operational tools. Nothing clever.

### proxmox/

Boot order, startup delays and backup configuration for the VMs, in the order that keeps dependencies satisfied.

## A note on what is not here

No secrets, no tokens, no webhook URLs. Private addresses are left in on purpose. They are not routable from the internet and blurring them would cost credibility without buying security.

## Still open

- Automated snapshots and replication on the storage pool. This is the root cause of most of the incidents in this repo and it is not done yet.
- Proxmox 8 to 9 on the main host.
- A second domain controller on separate hardware.

I would rather list these than pretend the lab is finished.
