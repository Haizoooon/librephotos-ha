# LibrePhotos for Home Assistant

<p align="center">
  <strong>Bring your personal photo library into Home Assistant.</strong>
  <br>
  Automatically display a random photo from your LibrePhotos instance on your Home Assistant dashboard.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-18BCF2?logo=homeassistant" alt="Home Assistant">
  <img src="https://img.shields.io/badge/LibrePhotos-Supported-blue" alt="LibrePhotos">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/Status-Experimental-orange" alt="Experimental">
</p>

---

## Overview

**LibrePhotos for Home Assistant** is a custom integration that connects your self-hosted [LibrePhotos](https://github.com/LibrePhotos/librephotos) instance to Home Assistant.

It allows you to display random photos from your personal photo library directly on your Home Assistant dashboard.

Whether you want to rediscover old memories or turn your Home Assistant dashboard into a digital photo frame, this integration makes it possible.

## Features

- **Daily Random Photo** – Automatically select a new random photo.
- **Dashboard Integration** – Display your selected photo using Home Assistant's native image entity.
- **Manual Photo Selection** – Trigger a new random photo whenever you want.
- **Photo Information** – Access metadata of the currently selected photo.
- **Photo Count Sensor** – Display the number of photos available in your library.
- **JWT Authentication** – Authenticate securely with your LibrePhotos instance.
- **HTTPS Support** – Connect to remotely hosted LibrePhotos instances.
- **Native Home Assistant Integration** – No additional Docker containers or external services required.

## Requirements

- Home Assistant OS, Supervised, Container or Core.
- A working LibrePhotos instance.
- LibrePhotos API access.
- A LibrePhotos username and password.
- Network access from Home Assistant to your LibrePhotos instance.

## Installation

There are two ways to install this integration.

### Method 1: HACS (Recommended)

> HACS installation requires this repository to be published on GitHub and to contain a valid `hacs.json` file.

1. Open **HACS** in Home Assistant.
2. Click the three-dot menu in the top-right corner.
3. Select **Custom repositories**.
4. Enter the GitHub repository URL:

   `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY`

5. Select **Integration** as the category.
6. Click **Add**.
7. Search for **LibrePhotos** in HACS.
8. Open the integration and click **Download**.
9. Restart Home Assistant.

After restarting, continue with the configuration.

### Method 2: Manual Installation

1. Download the latest release or clone this repository.
2. Extract the downloaded files.
3. Locate the `custom_components` directory.
4. Copy the `librephotos` folder into your Home Assistant configuration directory.

Your directory structure should look like this:

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

5. Restart Home Assistant.

You can also install the integration using the Home Assistant Terminal:

```bash
mkdir -p /config/custom_components
```

Then transfer the `librephotos` folder into that directory.

## Configuration

After installation:

1. Open **Settings → Devices & Services**.
2. Click **Add Integration**.
3. Search for **LibrePhotos**.
4. Enter your connection details.

| Setting | Example |
|---|---|
| URL | `https://photos.example.com` |
| Username | Your LibrePhotos username |
| Password | Your LibrePhotos password |

Click Submit to connect your LibrePhotos instance.

The integration will authenticate against your LibrePhotos API and retrieve an initial random photo.

## Entities

The integration currently provides the following entities:

| Entity | Description |
|---|---|
| `image.librephotos_tagesfoto` | Currently selected random photo |
| `sensor.librephotos_fotoanzahl` | Number of available photos |
| `sensor.librephotos_aufnahmedatum` | Capture date of the selected photo |

*Note: Actual entity IDs may depend on your Home Assistant entity naming and language settings.*

## Dashboard Configuration

### Display the Daily Photo

Add a Picture Entity card to your Lovelace dashboard:

```yaml
type: picture-entity
entity: image.librephotos_tagesfoto
show_name: false
show_state: false
```

### Add a Random Photo Button

You can manually select another random photo using a button:

```yaml
type: button
name: Random Photo
icon: mdi:image-refresh
tap_action:
  action: perform-action
  perform_action: librephotos.next_random_photo
```

## Automation

### Automatically Change the Photo Every Day

Create the following automation in Home Assistant:

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

This automation selects a new random photo every day at midnight.

You can also change the trigger to any other time you prefer.

## Troubleshooting

### Integration cannot connect

Check the following:

- Your LibrePhotos instance is accessible.
- The URL is correct.
- Your username and password are correct.
- Home Assistant can reach your LibrePhotos server.
- HTTPS certificates are valid.

### No photos are displayed

Check the Home Assistant logs for API errors.

Make sure your LibrePhotos library contains indexed photos and that your account has permission to access them.

### Authentication errors

LibrePhotos uses JWT authentication. Check whether your LibrePhotos API authentication endpoints are accessible and whether your credentials are valid.

### Reporting Issues

If you encounter a problem, please open a GitHub issue and include:

- Your Home Assistant version.
- Your LibrePhotos version.
- Relevant Home Assistant logs.
- Steps to reproduce the issue.

**Never include passwords, access tokens or other sensitive information in bug reports.**

## Development Status

This integration is currently experimental.

API compatibility, photo metadata parsing and image retrieval may vary between LibrePhotos versions.

Contributions, bug reports and feature requests are welcome!

## Roadmap

Potential future improvements:

- [ ] Configurable photo selection intervals.
- [ ] Exclude specific albums or photos.
- [ ] Random photos from selected albums.
- [ ] Additional EXIF metadata.
- [ ] Photo taken on this day in previous years.
- [ ] Multiple photo entities.
- [ ] Configurable randomization options.
- [ ] Improved HACS support and release management.

## Contributing

Contributions are welcome!

Feel free to fork the repository, create a feature branch and submit a pull request.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for Home Assistant and LibrePhotos.
</p>
