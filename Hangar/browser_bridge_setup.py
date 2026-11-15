"""User-invoked setup; registration changes only Hangar's HKCU browser keys."""
import argparse
from pathlib import Path
from wtmm.browser_bridge import prepare_registration, install_registration, remove_registration


def main():
    parser = argparse.ArgumentParser(description="Connect the Download via Hangar Chrome / Edge extension")
    parser.add_argument("--browser", choices=("chrome", "edge", "both"), default="both")
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--prepare-only", action="store_true", help="Write helper files without registering anything")
    parser.add_argument("--remove", action="store_true", help="Remove this installation's browser registration")
    args = parser.parse_args()
    app_root = Path(__file__).resolve().parent
    data_dir = args.data_dir or app_root / "library"
    if args.remove:
        remove_registration(app_root, data_dir, args.browser); print("Hangar browser connection removed."); return
    prepared = prepare_registration(app_root, data_dir, args.browser)
    if not args.prepare_only: install_registration(prepared)
    print("Helper prepared." if args.prepare_only else "Hangar browser connection registered for the current Windows user.")
    print("Extension ID:", prepared["extension_id"])
    print("Load unpacked extension folder:", app_root / "extension")
    print("Restart Hangar after upgrading from version 1.0. Reload the extension and refresh WT Live.")


if __name__ == "__main__": main()
