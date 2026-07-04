/* =====================================================================
 * Sophia Galaxy — config
 * ---------------------------------------------------------------------
 * Theming for the sophia-agi knowledge base.
 * Keys must match folder names produced by the scanner.
 * Unlisted folders still appear with a nice auto color.
 * ===================================================================== */

window.GALAXY_CONFIG = {
  title: "SOPHIA GALAXY",
  subtitle: "PROVENANCE  •  WISDOM  •  AGI",
  quote: "Per aspera ad astra",
  quoteBy: "through hardship to the stars",

  style: {
    // Largest / primary knowledge bodies
    "wiki": {
      sub: "Living Corpus",
      color: "#7dd3fc",
      ring: true,
      desc: "The expansive, evolving collection of notes, traces, and emergent knowledge. The beating heart of the second brain."
    },
    "docs": {
      sub: "Structured Knowledge",
      color: "#a855f7",
      ring: false,
      desc: "Formal documentation, roadmaps, agent architecture, epistemic substrate, and disciplined methodology."
    },

    // Evidence & rigor
    "agi-proof": {
      sub: "Evidence & Ledgers",
      color: "#34d399",
      ring: false,
      desc: "Failure ledgers, benchmarks, proofs, and verifiable traces. What has actually been shown."
    },
    "_map": {
      sub: "Constellations",
      color: "#c084fc",
      ring: false,
      desc: "High-level knowledge maps and architectural constellations of the project."
    },

    // Core intellectual domains
    "moral_corpus": {
      sub: "Ethics & Virtue",
      color: "#fbbf24",
      ring: true,
      desc: "Moral philosophy, cardinal virtues, value alignment, and the ethical substrate for AGI."
    },
    "training": {
      sub: "Substrate",
      color: "#f472b6",
      ring: false,
      desc: "Training data, recipes, continual learning, and the raw material of intelligence."
    },

    // Supporting clusters
    "okf": {
      sub: "Open Knowledge",
      color: "#5eead4",
      ring: false,
      desc: "Open Knowledge Framework artifacts and related explorations."
    },
    "skills": {
      sub: "Capabilities",
      color: "#60a5fa",
      ring: false,
      desc: "Agent skills, MCP servers, and composable capabilities."
    },
    "eval": {
      sub: "Measurement",
      color: "#fb923c",
      ring: false,
      desc: "Evaluations, benchmarks, and faithfulness harnesses."
    },
    "pretraining": {
      sub: "Foundation",
      color: "#a3e635",
      ring: false,
      desc: "Pretraining pipelines, datasets, and base model work."
    },

    // Other notable folders (will appear even if not listed)
    "paper": { sub: "Publications", color: "#e879f9", ring: false, desc: "Papers, notes toward publication, and formal writing." },
    "sophia-storage": { sub: "Memory Systems", color: "#67e8f9", ring: false, desc: "Storage, retrieval, and long-term memory substrate." },
    "huggingface": { sub: "Artifacts", color: "#c4b5fd", ring: false, desc: "Model cards, spaces, and published artifacts." },
  },

  // Fallback palette for any unstyled planets. Rich, cosmic, high-contrast.
  palette: [
    "#7dd3fc", "#a855f7", "#34d399", "#fbbf24", "#f472b6",
    "#60a5fa", "#5eead4", "#fb923c", "#a3e635", "#c084fc",
    "#e879f9", "#67e8f9", "#f9a8d4"
  ],
};
