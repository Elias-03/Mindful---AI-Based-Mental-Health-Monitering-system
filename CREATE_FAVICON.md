# Favicon Setup

I've added an SVG favicon to `static/fav.ico` with your app's gradient colors.

## Current Favicon
- **Location**: `static/fav.ico`
- **Design**: Brain emoji (🧠) on gradient purple-blue circle
- **Format**: SVG (works in all modern browsers)

## To Add a Traditional .ico File

If you want a traditional favicon.ico:

1. **Option A - Use an online converter:**
   - Go to https://favicon.io/favicon-converter/
   - Upload an image (logo, icon, or screenshot)
   - Download the generated favicon.ico
   - Place it in `static/favicon.ico`

2. **Option B - Use an emoji:**
   - Go to https://favicon.io/emoji-favicons/brain/
   - Download the brain emoji favicon
   - Place favicon.ico in `static/` folder

3. **Option C - Create custom:**
   - Design a 32x32 or 64x64 icon
   - Save as PNG
   - Convert to .ico format
   - Place in `static/favicon.ico`

The templates are already configured to use both SVG (modern) and ICO (fallback) formats.

## Current Implementation
All pages now include:
```html
<link rel="icon" type="image/svg+xml" href="/static/fav.ico">
<link rel="alternate icon" href="/static/favicon.ico">
```

The browser will use SVG if supported, otherwise fall back to ICO.
