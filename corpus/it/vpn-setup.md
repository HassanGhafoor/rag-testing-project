# VPN Setup Guide

**Owner:** IT & Cyber Security, Nimbus Logistics (Pvt) Ltd, Lahore
**Applies to:** All staff accessing internal systems from outside the office

## Overview

Nimbus Logistics uses **NimbusConnect**, a WireGuard-based VPN, to secure remote
access to internal systems such as NimbusHR, NimbusClaim, and the fleet
dispatch dashboard. You must connect through NimbusConnect whenever you access
these systems from outside the Lahore office network.

## Before You Start

Make sure you have:

- Your company laptop with the standard image installed
- Your Nimbus email account and MFA already configured (see
  **passwords-and-mfa.md**)
- A stable internet connection (do not set up the VPN for the first time on
  public Wi-Fi)

## Installing NimbusConnect

1. Open the **Nimbus Software Portal** on your company laptop.
2. Search for **NimbusConnect** and click **Install**. The client is approved
   for automatic installation and needs no separate request.
3. Wait for the installer to finish; it takes about **2 minutes**.
4. Launch **NimbusConnect** from the applications menu.

## Requesting Your VPN Profile

Each employee needs a personal VPN profile. To request one:

1. In NimbusConnect, click **Request Profile**.
2. Sign in with your Nimbus email and complete the MFA prompt.
3. IT provisions the profile automatically within **15 minutes** during business
   hours (09:00–18:00 PKT). Outside these hours, allow up to the next morning.
4. When you receive the confirmation email, reopen NimbusConnect and your
   profile appears under **My Connections**.

Profiles are tied to a single device. If you replace your laptop, request a new
profile and the old one is revoked automatically.

## Connecting

1. Open **NimbusConnect** and select your profile.
2. Click **Connect**. The status indicator turns green when the tunnel is
   active.
3. You can confirm the connection by visiting the internal status page at
   **status.internal.nimbus** — it only loads while the VPN is active.

The VPN disconnects automatically after **12 hours** or after **30 minutes** of
laptop sleep, and you will need to reconnect.

## Split Tunnelling

NimbusConnect uses split tunnelling: only traffic to internal Nimbus systems
goes through the VPN, while general internet traffic uses your normal
connection. This keeps browsing fast while protecting company data. Do not
attempt to disable split tunnelling; the configuration is managed by IT.

## Troubleshooting

- **Status stays yellow / won't connect:** quit NimbusConnect fully and relaunch,
  then reconnect. If it still fails, restart the laptop.
- **"Profile expired" message:** VPN profiles expire after **90 days** of
  inactivity. Click **Request Profile** to get a fresh one.
- **MFA prompt not arriving:** confirm your authenticator app time is synced;
  see **passwords-and-mfa.md**.
- **Slow internal apps:** check your underlying internet speed first, since split
  tunnelling means the VPN only carries internal traffic.
- **Public Wi-Fi issues:** some public networks block VPN traffic. Use a mobile
  hotspot as a fallback.

If none of these resolve the issue, raise a ticket with the **IT Helpdesk**
through the Nimbus Software Portal or email it.helpdesk@nimbuslogistics.example.
Include a screenshot of the NimbusConnect status window and the time the problem
occurred.

## Security Reminders

- Never share your VPN profile or export it to another device.
- Always connect through the VPN before opening internal systems on public or
  home networks.
- Lock your screen whenever you step away, even at home.
- Report a lost or stolen laptop to IT immediately so the profile can be revoked
  (see **laptop-policy.md**).

## Related Documents

See **passwords-and-mfa.md** for account and MFA setup, **laptop-policy.md** for
device rules, and **it-faq.md** for quick answers to common questions.
