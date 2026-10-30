Videos, stills, and sounds that sit beside the session file on the tablet.

Everything in this folder is copied into dist/<campaign>/ on every build, so the
whole dist/<campaign>/ folder is what goes on the tablet.

Names follow the world slug:
  kestrel-surface.mp4     main drone feed, Visible mode
  kestrel-thermal.mp4     main drone feed, Thermal mode
  kestrel-surface01.mp4   second drone feed (free-form, no caption)
.webm works too, and so does a still image with the same name (.webp, .png, .jpg).

A trigger sound named in campaign.md (Sound: klaxon.mp3) can live here as well,
though putting it in sounds/ instead bakes it into the file, which is more reliable on Android.
