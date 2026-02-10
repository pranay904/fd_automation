# ---------------------------
# Global click/hover highlight for all elements
# ---------------------------
def enable_click_highlight(page):
    """
    Automatically highlights every clicked element with red outline.
    Optional: hover highlight in orange.
    """
    page.add_init_script("""
        document.addEventListener('click', event => {
            const el = event.target;
            const originalOutline = el.style.outline;
            el.style.outline = '3px solid red';
            el.style.outlineOffset = '2px';
            setTimeout(() => {
                el.style.outline = originalOutline;
            }, 800);
        }, true);

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

# ---------------------------
# Manual highlight for specific elements
# ---------------------------
from playwright.sync_api import Locator

def highlight_element(locator: Locator, duration=800):
    """
    Highlights a specific locator element for a duration (ms).
    Useful for inputs or buttons.
    """
    locator.evaluate("""
        (el, duration) => {
            const original = el.style.outline;
            el.style.outline = '3px solid orange';
            el.style.outlineOffset = '2px';
            setTimeout(() => { el.style.outline = original; }, duration);
        }
    """, duration)
