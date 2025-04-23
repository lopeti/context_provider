// www/topic_editor.js v2

import { html, css, LitElement } from "https://unpkg.com/lit-element/lit-element.js?module";

class TopicEditorPanel extends LitElement {
  static get properties() {
    return {
      files: { type: Array },
    };
  }

  constructor() {
    super();
    this.files = [];
  }

  connectedCallback() {
    super.connectedCallback();
    this.loadFiles();
  }

  async loadFiles() {
    // TODO: fetch list from backend
    this.files = ["heating.md", "energy.md", "topics.yaml"];
  }

  render() {
    return html`
      <h1>Topic szerkesztő</h1>
      <ul>
        ${this.files.map(
          (f) => html`<li><button @click=${() => this.openFile(f)}>${f}</button></li>`
        )}
      </ul>
    `;
  }

  openFile(fileName) {
    alert(`TODO: Open file: ${fileName}`);
  }

  static get styles() {
    return css`
      h1 {
        color: var(--primary-color);
      }
      ul {
        list-style: none;
        padding: 0;
      }
    `;
  }
}

// Ensure the custom element is not registered multiple times
if (!customElements.get("topic-editor-panel")) {
  customElements.define("topic-editor-panel", TopicEditorPanel);
}
