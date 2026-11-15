# Download via Hangar — Chrome / Edge companion

Hangar 1.1 includes an unpacked Manifest V3 browser extension for **Google Chrome and Microsoft Edge on Windows**. It adds a second **Download via Hangar** button below the normal green download button in a WT Live post, plus compact buttons on feed cards.

The normal WT Live download remains available. Only downloads started with the Hangar button are sent to the app.

## One-time setup

1. **Close and restart Hangar after upgrading from 1.0.** Keep your existing `library` folder. The new source package can be extracted over the old application files; it does not contain or replace your library.
2. In Chrome open `chrome://extensions`, or in Edge open `edge://extensions`.
3. Turn on **Developer mode**. Choose **Load unpacked** and select the `extension` folder inside your Hangar installation. Select the folder containing `manifest.json`, not the ZIP and not the parent Hangar folder.
4. Open **Hangar → Settings → Browser extension → Set up browser extension**.
5. Choose **Chrome**, **Edge**, or **Chrome and Edge**, then click **Connect browser**. This registers the local helper for your Windows account. No administrator rights are needed.
6. Reload the extension from the browser's extension page, then refresh your WT Live tab.
7. Pin the extension if you want quick access to connection status, recent downloads and retries.

The unpacked extension ID is stable across folder moves:

```text
njenenicikfcfjffpgcebmhccfcpgelf
```

After moving the Hangar application or changing its paired library, run **Connect browser** again. One helper registration is paired to one library per Windows account. Connecting another library changes the destination for subsequent browser imports.

This build has **not been published to the Chrome Web Store or Edge Add-ons**. Loading the provided source folder is required. No extension or registry connection is installed automatically by extracting or launching the app.

## What happens when you click

1. The extension checks that Hangar's local helper is available.
2. The browser downloads the file using the post's existing official `https://live.warthunder.com/dl/.../` link. Redirects, login/session handling, download cancellation and browser download checks stay with the browser.
3. The extension waits for its own download ID to complete and checks that it is an accepted ZIP.
4. It passes the completed local filename and public post information to the registered helper using native messaging. Webpage messages cannot provide local filenames; the extension obtains those only from the browser's Downloads API.
5. The helper queues an import and opens Hangar when needed. An already-running Hangar checks its inbox roughly once per second, waiting while another operation or dialog is active.
6. Hangar uses its existing ZIP validation and metadata pipeline. New imports stay **disabled**. If the mod has variants, the normal options dialog appears. You enable and deploy it yourself.

For regular ZIPs, Hangar can use the post's visible title/first paragraph, author, description and hashtags as generated metadata. If the archive already has author metadata, that metadata takes precedence. Details include an **Open original WT Live post** button. Descriptions remain plain text.

The browser's original downloaded ZIP stays where it was downloaded. Hangar caches its own original ZIP in the library, just as it does for a manual import.

## Connection and retries

Open the extension toolbar popup to check the connection, view recent requests or **Retry handoff** after a temporary helper failure. A retry reuses the completed download. If the download itself is interrupted, resume it in the browser's download panel first. Browser restarts are handled by saved download IDs and reconciliation.

The page shows **Sent to Hangar** once the helper accepts the request. This means the request is queued; Hangar may still be importing the ZIP or waiting for you to finish another dialog. Click **Refresh** in the toolbar popup to see the eventual imported/error result.

- **Helper not found / disconnected:** connect it in Hangar Settings, reload the extension, then refresh WT Live. If you upgraded from 1.0, restart the desktop app.
- **Hangar did not open:** open it manually. The accepted request stays in the paired library's inbox until processed.
- **An options dialog is already open:** finish or close it; queued requests wait.
- **Unsupported archive / login page:** ZIP is the current supported import type. RAR, 7z, HTML login pages and other file types stay in your browser and are not imported.
- **Download blocked or under review:** finish the normal browser review yourself. The extension does not dismiss warnings or bypass browser checks.
- **Duplicate ZIP:** the existing library entry is reused without changing its enabled state. It is not imported twice.
- **No button visible:** refresh WT Live after loading the extension. The implementation matches the current `a.downloadButton` and feed `.downloads` controls. If WT Live changes its page structure, its selectors may need an update.

## Command-line alternative

The same connection can be configured from the Hangar folder:

```powershell
py -3 browser_bridge_setup.py --browser both
```

For a separate library:

```powershell
py -3 browser_bridge_setup.py --browser chrome --data-dir "D:\War Thunder Mods"
```

Prepare helper files without registering anything:

```powershell
py -3 browser_bridge_setup.py --prepare-only
```

Disconnect:

```powershell
py -3 browser_bridge_setup.py --browser both --remove
```

You can also disconnect from Hangar's setup dialog and remove the extension normally in your browser.

## Local files and registration

The setup writes:

```text
library/.browser-bridge/
  bridge.json                 # trusted app/interpreter/library paths and extension origin
  native_host.cmd             # launches the local Python helper with binary stdio
  com.hangar.wtlive.json       # native host manifest; allows only the fixed extension origin

library/incoming/
  <request UUID>.json          # queued import; contains the completed download's path
  results/<request UUID>.json  # imported/error receipt
  processed/<request UUID>.json
```

**Connect browser** writes only the selected Hangar entries under the current user's registry:

```text
HKCU\Software\Google\Chrome\NativeMessagingHosts\com.hangar.wtlive
HKCU\Software\Microsoft\Edge\NativeMessagingHosts\com.hangar.wtlive
```

It does not change the game, register an HTTP service, add a startup task, or change download file associations. The helper reads completed local ZIPs; network shares, links and non-ZIP downloads are rejected.

## Privacy and permissions

See [extension/PRIVACY.md](extension/PRIVACY.md). The extension requests only WT Live site access, Downloads, Storage and Native Messaging. There is no analytics service, external upload, cookie-reading permission or Hangar web account.

## Verification and remaining manual check

Automated checks cover fixed extension identity, official URL validation, sender/frame validation, browser-owned download paths, instant download races, retries without redownloading, duplicate events, normal-download isolation, button injection and re-injection in a DOM fixture, trusted clicks, native protocol framing, a real helper subprocess, source metadata, app inbox processing, malformed request quarantine and author metadata precedence.

The existing deployment and purge tests also run. Tests use fake ZIPs and separate libraries. Native registration was prepared and inspected without changing your registry.

Live WT Live markup was inspected directly to identify the download links and button containers. **An installed-extension download in Chrome/Edge still needs a manual end-to-end check after the setup above.** Browser policy blocked opening the local preview file, and the environment's network restrictions prevented the local HTTP preview; these restrictions were not bypassed.

Browser API references: [Chrome Downloads](https://developer.chrome.com/docs/extensions/reference/api/downloads), [Chrome native messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging), [Edge native messaging](https://learn.microsoft.com/en-us/microsoft-edge/extensions/developer-guide/native-messaging).
