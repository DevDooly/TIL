document.addEventListener("DOMContentLoaded", function() {
  mermaid.initialize({
    startOnLoad: true,
    theme: document.querySelector('body').getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'default'
  });
});
