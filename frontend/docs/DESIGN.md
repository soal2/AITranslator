# Frontend Design Documentation

## Design Philosophy
This interface follows a "Minimalist Tech" aesthetic inspired by Apple's Human Interface Guidelines, focusing on clarity, deference, and depth.

### Key Visual Elements
1.  **Glassmorphism**: Extensive use of `backdrop-filter: blur()` to create depth and context.
2.  **Typography**: San Francisco (system font) stack for native feel. Clear hierarchy with uppercase tracking for labels.
3.  **Color Palette**:
    - Background: `#f5f5f7` (Apple Light Gray)
    - Accents: Blue/Indigo gradients for "Intelligence" feel.
    - Text: Slate scale (`slate-900` for headings, `slate-500` for body).
4.  **Motion**: Smooth layout transitions using `framer-motion` (Spring physics).
5.  **Rounded Corners**: Large `32px` border radius for friendly, modern containers.

## Component Structure
- `App.tsx`: Main container and logic (Single Responsibility for MVP).
- Input Section: Textarea with character count.
- Output Section: Result display with keywords extraction.
- Loading States: Custom spinners and pulsing text.

## Tech Stack
- **React 19**: Core UI library.
- **Tailwind CSS v4**: Utility-first styling with new engine.
- **Framer Motion**: Production-grade animations.
- **Lucide React**: Clean, consistent iconography.
- **Vite**: Build tool.

## Accessibility
- Semantic HTML tags (`header`, `main` implied by div structure, `button`).
- Focus states managed by browser/Tailwind.
- High contrast text colors.
- ARIA labels where necessary (e.g. icon buttons).
