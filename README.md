<div align="center">

<img src="https://raw.githubusercontent.com/LibrePhotos/librephotos/dev/docs/static/img/logo.png" alt="LibrePhotos" width="96" height="96">

# LibrePhotos for Home Assistant

**Turn your self-hosted photo library into a living dashboard.**
A new random memory from your [LibrePhotos](https://github.com/LibrePhotos/librephotos) instance, every single day.

<br>

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-18BCF2?style=for-the-badge&logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://hacs.xyz/)
[![LibrePhotos](https://img.shields.io/badge/LibrePhotos-Supported-2563EB?style=for-the-badge)](https://github.com/LibrePhotos/librephotos)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Experimental-F59E0B?style=for-the-badge)](#-development-status)

<br>

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Haizoooon&repository=librephotos-ha&category=integration)
[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=librephotos)

[Features](#-features) · [Installation](#-installation) · [Configuration](#%EF%B8%8F-configuration) · [Dashboard](#-dashboard) · [Automation](#-automation) · [Troubleshooting](#-troubleshooting) · [Roadmap](#%EF%B8%8F-roadmap)

</div>

---

## ✨ Overview

**LibrePhotos for Home Assistant** connects your self-hosted LibrePhotos server to your smart home. Rediscover old memories, or turn any tablet or wall panel into a digital photo frame, with no extra containers or external services.

> [!NOTE]
> Everything runs natively inside Home Assistant. Your photos never leave your own network unless you expose LibrePhotos yourself.

## 🚀 Features

| | Feature | Description |
|---|---|---|
| 🎲 | **Daily Random Photo** | Automatically picks a fresh photo from your library. |
| 🖼️ | **Native Image Entity** | Works with any dashboard card that supports `image` entities. |
| 🔄 | **On-demand Refresh** | Trigger a new random photo any time via a service call. |
| 📅 | **Photo Metadata** | Access the capture date of the currently selected photo. |
| 🔢 | **Photo Counter** | See how many photos your library contains. |
| 🔐 | **JWT Authentication** | Secure login against the LibrePhotos API. |
| 🌐 | **HTTPS Support** | Works with remotely hosted instances. |

## 📋 Requirements

- Home Assistant (OS, Supervised, Container or Core)
- A running LibrePhotos instance with API access
- A LibrePhotos username and password
- Network access from Home Assistant to LibrePhotos

## 📦 Installation

<details open>
<summary><b>Option 1 · HACS (recommended)</b></summary>

<br>

Click the button for one-click setup:

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Haizoooon&repository=librephotos-ha&category=integration)

Or add it manually:

1. Open **HACS** in Home Assistant.
2. Click the **⋮** menu (top right) → **Custom repositories**.
3. Enter the repository URL:
   ```text
   https://github.com/Haizoooon/librephotos-ha
   ```
4. Select **Integration** as the category and click **Add**.
5. Search for **LibrePhotos** in HACS and click **Download**.
6. **Restart** Home Assistant.

> [!IMPORTANT]
> HACS requires a valid `hacs.json` in the repository root.

</details>

<details>
<summary><b>Option 2 · Manual installation</b></summary>

<br>

1. Download the latest release or clone this repository.
2. Copy the `librephotos` folder into your Home Assistant `custom_components` directory.
3. **Restart** Home Assistant.

```text
/config/
└── custom_components/
    └── librephotos/
        ├── __init__.py
        ├── config_flow.py
        ├── const.py
        ├── image.py
        ├── sensor.py
        ├── manifest.json
        └── services.yaml
```

If the directory does not exist yet:

```bash
mkdir -p /config/custom_components
```

</details>

## ⚙️ Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **LibrePhotos**
3. Enter your connection details:

| Setting | Example |
|---|---|
| **URL** | `https://photos.example.com` |
| **Username** | Your LibrePhotos username |
| **Password** | Your LibrePhotos password |

The integration authenticates against the LibrePhotos API and fetches an initial random photo right away.

## 🧩 Entities

| Entity | Type | Description |
|---|---|---|
| `image.librephotos_tagesfoto` | Image | The currently selected random photo |
| `sensor.librephotos_fotoanzahl` | Sensor | Number of available photos |
| `sensor.librephotos_aufnahmedatum` | Sensor | Capture date of the selected photo |

> [!TIP]
> Actual entity IDs depend on your Home Assistant language and naming settings.

## 🖥️ Dashboard

### Show the daily photo

```yaml
type: picture-entity
entity: image.librephotos_tagesfoto
show_name: false
show_state: false
```

### Add a "new photo" button

```yaml
type: button
name: Random Photo
icon: mdi:image-refresh
tap_action:
  action: perform-action
  perform_action: librephotos.next_random_photo
```

## 🤖 Automation

Pick a new photo every day at midnight:

```yaml
alias: LibrePhotos - Daily Random Photo
description: Select a new random photo every day.
triggers:
  - trigger: time
    at: "00:00:00"
actions:
  - action: librephotos.next_random_photo
mode: single
```

> [!TIP]
> Change the `at:` time to whatever suits you, or use another trigger such as a presence or motion sensor.

## 🛠️ Troubleshooting

<details>
<summary><b>The integration cannot connect</b></summary>

<br>

- Is your LibrePhotos instance reachable from Home Assistant?
- Is the URL correct (including `https://` and port, if any)?
- Are your username and password correct?
- Is your HTTPS certificate valid?

</details>

<details>
<summary><b>No photos are displayed</b></summary>

<br>

- Check the Home Assistant logs for API errors.
- Make sure your library contains **indexed** photos.
- Make sure your account has permission to access them.

</details>

<details>
<summary><b>Authentication errors</b></summary>

<br>

LibrePhotos uses JWT authentication. Verify that the API authentication endpoints are reachable and that your credentials are valid.

</details>

### 🐛 Reporting issues

Please [open an issue](../../issues) and include:

- Your Home Assistant version
- Your LibrePhotos version
- Relevant logs
- Steps to reproduce

> [!WARNING]
> Never include passwords, tokens or other sensitive data in bug reports.

## 🚧 Development Status

This integration is **experimental**. API compatibility, metadata parsing and image retrieval may vary between LibrePhotos versions.

## 🗺️ Roadmap

- [ ] Configurable photo selection intervals
- [ ] Exclude specific albums or photos
- [ ] Random photos from selected albums
- [ ] Additional EXIF metadata
- [ ] "On this day" photos from previous years
- [ ] Multiple photo entities
- [ ] Configurable randomization options
- [ ] Improved HACS support and release management

## 🤝 Contributing

Contributions are welcome! Fork the repository, create a feature branch and open a pull request.

## 📄 License

Released under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ for **Home Assistant** and **LibrePhotos**

⭐ If you like this project, consider giving it a star!

</div>
