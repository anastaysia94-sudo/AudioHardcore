# AudioHardcore WordPress Integration

AudioHardcore uses WordPress as a publishing/content layer rather than as the authoritative music-library database. The platform's application data stays in the AudioHardcore API/database; WordPress can publish pages, news, documentation, community content, and integration widgets.

## 1. Install WordPress

Use a WordPress host that meets current WordPress requirements, then complete the normal WordPress installation. Many hosts provide a one-click installer; WordPress also documents a manual installation path.

## 2. Install the AudioHardcore connector plugin

The repository contains a minimal connector plugin at:

```text
wordpress/audiohardcore-integration/
```

Create a ZIP from that folder, keeping `audiohardcore-integration/` as the top-level folder.

In WordPress:

1. Go to **Plugins > Add New**.
2. Choose **Upload Plugin**.
3. Select the AudioHardcore plugin ZIP.
4. Click **Install Now**.
5. Click **Activate Plugin**.

WordPress documents ZIP upload installation and manual SFTP installation.

## 3. Configure the connector

After activation, open **Settings > AudioHardcore** and enter your AudioHardcore API base URL, for example:

```text
https://music.example.com
```

## 4. Add the widget to a page

Use:

```text
[audiohardcore_library]
```

The widget reads the configured AudioHardcore API and displays a compact library summary and link.

## 5. Security

- Use HTTPS for the AudioHardcore API in production.
- Do not place API secrets in page content.
- Keep WordPress, plugins, and themes updated.
- Restrict authenticated API operations to server-side integration when credentials are required.
- Prefer documented WordPress authentication mechanisms such as Application Passwords for authenticated WordPress API operations.

## 6. Architecture

```text
WordPress
   |
   +-- Pages / Posts / Docs / Community content
   |
   +-- AudioHardcore Integration Plugin
   |
   +-- AudioHardcore REST API
             |
             +-- Library
             +-- Playlists
             +-- Users
             +-- Sync
             +-- Metadata
```

The WordPress REST API is JSON-based and provides a standard application boundary for external apps and plugins. AudioHardcore should keep its core music database outside WordPress rather than duplicating the library there.

## Official references

- https://wordpress.org/documentation/article/manage-plugins/
- https://developer.wordpress.org/rest-api/
- https://developer.wordpress.org/plugins/rest-api/
