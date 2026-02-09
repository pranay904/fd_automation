# utils/highlight_helpers.py

def enable_click_highlight(page):
    """
    Highlights every element automatically on click.
    Duration: 0.8 seconds (800 ms)
    """
    page.add_init_script("""
        // Highlight every clicked element
        document.addEventListener('click', event => {
            const el = event.target;
            const originalOutline = el.style.outline;
            el.style.outline = '3px solid red';
            el.style.outlineOffset = '2px';
            setTimeout(() => {
                el.style.outline = originalOutline;
            }, 800);
        }, true);

        // Optional: highlight hovered elements
        document.addEventListener('mouseover', event => {
            const el = event.target;
            el.style.transition = 'outline 0.2s ease-in-out';
            el.style.outline = '2px solid orange';
        }, true);

        document.addEventListener('mouseout', event => {
            const el = event.target;
            el.style.outline = '';
        }, true);
    """)
