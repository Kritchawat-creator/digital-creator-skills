// YouTube Studio helpers (run in the Studio page). Patch file-input clicks so the next "Upload file" opens no picker:
// window.__nextFile = new File([...], name, {type}); then click the Studio button that opens the picker.
(() => {
  if (window.__patchedClick) return 'already patched';
  const orig = HTMLInputElement.prototype.click;
  HTMLInputElement.prototype.click = function () {
    if (this.type === 'file' && window.__nextFile) {
      const dt = new DataTransfer();
      dt.items.add(window.__nextFile);
      this.files = dt.files;
      window.__nextFile = null;
      this.dispatchEvent(new Event('change', { bubbles: true }));
      return;
    }
    return orig.call(this);
  };
  window.__patchedClick = true;
  return 'patched';
})();
