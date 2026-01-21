# Custom Icons Library

This folder contains custom PNG icons that can be used in your macropad actions, in addition to the FontAwesome icons.

## How to Add Custom Icons

1. **File format**: `{CategoryName}_{IconName}.png`
   - Example: `Brands_Discord.png` → goes to "Brands" category, displays as "Discord"
   - Example: `Media_CustomSound.png` → goes to "Media" category, displays as "CustomSound"

2. **Supported image formats**: PNG, JPG, JPEG, ICO, SVG, WebP

3. **Category name**: Must match exactly with an existing category:
   - `Brands_` - for brand/company logos
   - `Media_` - for media player controls
   - `System_` - for system/OS icons
   - `Navigation_` - for navigation arrows, menus
   - `Development_` - for code/terminal icons
   - `Communication_` - for chat/messaging
   - `Streaming_` - for streaming apps
   - `Gaming_` - for game-related icons
   - `UI_` - for UI elements
   - `Status_` - for status indicators

4. **Size recommendation**: 64x64 pixels or larger (will be scaled automatically)

## Example

- `example.png` - Example icon (not prefixed, so won't show up - just for reference)
- `Brands_MyApp.png` - Custom brand icon showing as "MyApp" in the Brands category

## To Add Your Own Icons

1. Name your icon file: `{CategoryName}_{DisplayName}.png`
   - Make sure the category name matches exactly (case-sensitive)
2. Place your PNG/JPG/SVG file in this folder
3. Restart the macropad application
4. Open the action editor and click "From Library"
5. Select the category (e.g., "Brands") and your custom icon will appear
6. Click on your icon to use it

## Tips

- Use transparent backgrounds for best results
- Keep file sizes small (under 100KB per icon)
- Use clear, simple designs for better visibility at small sizes
- The display name (after the underscore) is what appears in the icon list
- If the category prefix doesn't match exactly, the icon won't be loaded

