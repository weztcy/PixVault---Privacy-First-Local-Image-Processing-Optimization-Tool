PixVault ColorSpace UI Fix

Problem:
Adobe RGB, Display P3 and CMYK are shown but disabled.

Cause:
ColorSpacePage still contains the old ICC limitation.

Files to update:
ui/pages/colorspace_page.py

Changes:
- Enable all ICC targets
- Remove UI blocking
- Update capability message
- Allow build_config to accept ICC targets

Backend colorspace.py must already use ICC profiles.
