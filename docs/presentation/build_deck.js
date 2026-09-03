const pptxgen = require("pptxgenjs");

const C = {
  bg: "10131A",
  panel: "171C26",
  panel2: "1E2530",
  border: "2A3140",
  ink: "E8EAEF",
  inkDim: "8892A3",
  inkFaint: "565F72",
  amber: "E8A33D",
  cyan: "47C9B8",
  red: "E5484D",
};

const FONT = "Arial";

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

function bgSlide(title, kicker) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  if (kicker) {
    s.addText(kicker.toUpperCase(), {
      x: 0.6, y: 0.45, w: 8, h: 0.35, fontFace: FONT, fontSize: 11,
      color: C.amber, charSpacing: 2, bold: true,
    });
  }
  if (title) {
    s.addText(title, {
      x: 0.6, y: kicker ? 0.78 : 0.55, w: 12.1, h: 0.9, fontFace: FONT,
      fontSize: 30, color: C.ink, bold: true,
    });
  }
  return s;
}

function chip(s, text, x, y, w, color) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 0.4, rectRadius: 0.08, fill: { color: C.panel },
    line: { color, width: 1 },
  });
  s.addText(text, {
    x, y, w, h: 0.4, align: "center", valign: "middle", fontFace: FONT,
    fontSize: 11, color, bold: true,
  });
}

// ============================================================
// SLIDE 1 — TITLE
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.bg } });

  // small mark
  s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: 1.05, w: 0.14, h: 0.14, fill: { color: C.amber }, line: { type: "none" } });
  s.addShape(pres.ShapeType.ellipse, { x: 1.5, y: 1.05, w: 0.14, h: 0.14, fill: { color: C.cyan }, line: { type: "none" } });
  s.addShape(pres.ShapeType.ellipse, { x: 1.2, y: 1.55, w: 0.14, h: 0.14, fill: { color: C.cyan }, line: { type: "none" } });
  s.addShape(pres.ShapeType.line, { x: 0.97, y: 1.12, w: 0.53, h: 0, line: { color: C.amber, width: 1.5 } });
  s.addShape(pres.ShapeType.line, { x: 0.97, y: 1.12, w: 0.23, h: 0.43, line: { color: C.cyan, width: 1.5 }, flipH: true });
  s.addShape(pres.ShapeType.line, { x: 1.27, y: 1.12, w: 0.23, h: 0.43, line: { color: C.cyan, width: 1.5 } });

  s.addText("S\u016aTRA", {
    x: 0.6, y: 2.15, w: 10, h: 1.3, fontFace: FONT, fontSize: 64, bold: true, color: C.ink, charSpacing: 3,
  });
  s.addText("CRIMINAL NETWORK INTELLIGENCE & DECISION-SUPPORT PLATFORM", {
    x: 0.63, y: 3.35, w: 10, h: 0.4, fontFace: FONT, fontSize: 14, color: C.cyan, charSpacing: 2, bold: true,
  });
  s.addText("\u201cEvery clue has a thread. S\u016aTRA finds it.\u201d", {
    x: 0.63, y: 3.95, w: 9, h: 0.5, fontFace: FONT, fontSize: 16, italic: true, color: C.inkDim,
  });

  s.addShape(pres.ShapeType.rect, { x: 0.63, y: 4.7, w: 5.6, h: 0.02, fill: { color: C.border }, line: { type: "none" } });

  s.addText("Smart India Hackathon 2026  \u00b7  Problem Statement: Criminal Network Analysis using AI/ML/Graph Analytics", {
    x: 0.63, y: 6.7, w: 12, h: 0.4, fontFace: FONT, fontSize: 11.5, color: C.inkFaint,
  });
  chip(s, "DEMO \u00b7 SYNTHETIC DATA ONLY", 9.3, 0.55, 3.4, C.red);
}

// ============================================================
// SLIDE 2 — PROBLEM
// ============================================================
{
  const s = bgSlide("Investigators aren't short on data. They're short on synthesis.", "The Problem");
  const items = [
    ["FIRs & Police Reports", "Unstructured, often handwritten or scanned, filed across separate stations"],
    ["Call Detail Records", "Thousands of rows per case, no obvious pattern to a human reader"],
    ["Financial Transactions", "Bank records that reveal nothing until cross-referenced with people"],
    ["Surveillance & Social Intel", "Fragments that only mean something next to other fragments"],
  ];
  const colW = 2.95, gap = 0.25, startX = 0.6, y = 2.15;
  items.forEach((it, i) => {
    const x = startX + i * (colW + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: colW, h: 3.3, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.border, width: 1 } });
    s.addText(it[0], { x: x + 0.22, y: y + 0.3, w: colW - 0.44, h: 0.7, fontFace: FONT, fontSize: 15, bold: true, color: C.cyan });
    s.addText(it[1], { x: x + 0.22, y: y + 1.05, w: colW - 0.44, h: 2, fontFace: FONT, fontSize: 12, color: C.inkDim, valign: "top" });
  });
  s.addText("A network hides in the gaps between these sources \u2014 and manual cross-referencing at scale is slow, exhausting, and error-prone.", {
    x: 0.6, y: 5.75, w: 12, h: 0.8, fontFace: FONT, fontSize: 15, color: C.ink, italic: true,
  });
}

// ============================================================
// SLIDE 3 — SOLUTION / CORE PRINCIPLE
// ============================================================
{
  const s = bgSlide("One AI system. One design law.", "The Solution");
  s.addText("S\u016aTRA ingests FIRs, CDRs, financial records, and surveillance reports \u2014 extracts and resolves entities, builds a live knowledge graph, and surfaces hidden connections as evidence-backed investigative leads.", {
    x: 0.6, y: 2.0, w: 7.6, h: 1.6, fontFace: FONT, fontSize: 15, color: C.inkDim, valign: "top",
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 3.85, w: 7.6, h: 2.2, rectRadius: 0.08, fill: { color: C.panel }, line: { color: C.amber, width: 1.25 } });
  s.addText("CORE DESIGN LAW", { x: 0.9, y: 4.05, w: 5, h: 0.3, fontFace: FONT, fontSize: 10, color: C.amber, bold: true, charSpacing: 2 });
  s.addText("SUTRA never declares anyone a criminal. Every output is a potential association, a risk indicator, or an investigative lead \u2014 always requiring human verification.", {
    x: 0.9, y: 4.4, w: 7, h: 1.5, fontFace: FONT, fontSize: 15.5, color: C.ink, valign: "top",
  });

  const flow = ["Structured\nAlgorithms\nDiscover", "Knowledge\nGraph\nConnects", "Anomaly\nEngine\nFlags", "LLM\nExplains\n(never decides)"];
  const fw = 1.55, fx = 8.7, fy = 2.05, fgap = 0.15;
  flow.forEach((t, i) => {
    const x = fx;
    const y = fy + i * (0.95 + fgap);
    const col = i === 3 ? C.amber : C.cyan;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.6, h: 0.95, rectRadius: 0.06, fill: { color: C.panel2 }, line: { color: col, width: 1 } });
    s.addText(t.replace(/\n/g, " "), { x: x + 0.15, y, w: 3.3, h: 0.95, fontFace: FONT, fontSize: 12, color: col, bold: true, valign: "middle" });
    if (i < flow.length - 1) {
      s.addShape(pres.ShapeType.line, { x: fx + 1.8, y: y + 0.95, w: 0, h: fgap, line: { color: C.inkFaint, width: 1.5, endArrowType: "triangle" } });
    }
  });
}

// ============================================================
// SLIDE 4 — ARCHITECTURE PIPELINE
// ============================================================
{
  const s = bgSlide("From raw records to investigative leads", "System Architecture");
  const stages = ["Data\nIngestion", "OCR +\nCleaning", "NLP Entity\nExtraction", "Entity\nResolution", "Knowledge\nGraph", "Graph\nAnalytics", "Anomaly\nDetection", "Risk\nScoring", "AI\nAssistant", "Investigator\nDashboard"];
  const n = stages.length, boxW = 1.12, gap = 0.14, totalW = n * boxW + (n - 1) * gap;
  const startX = (13.333 - totalW) / 2, y = 2.6;
  stages.forEach((t, i) => {
    const x = startX + i * (boxW + gap);
    const col = i === 3 ? C.amber : (i >= 5 && i <= 7 ? C.amber : C.cyan);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: boxW, h: 1.35, rectRadius: 0.05, fill: { color: C.panel }, line: { color: col, width: 1.25 } });
    s.addText(t, { x: x + 0.04, y: y + 0.08, w: boxW - 0.08, h: 1.2, fontFace: FONT, fontSize: 9.5, color: C.ink, bold: true, align: "center", valign: "middle" });
    if (i < n - 1) {
      s.addShape(pres.ShapeType.line, { x: x + boxW, y: y + 0.675, w: gap, h: 0, line: { color: C.inkFaint, width: 1.5, endArrowType: "triangle" } });
    }
  });
  s.addText("Highlighted stages (amber) are where SUTRA's actual differentiation lives \u2014 entity resolution and the transparent, source-weighted risk scoring formula.", {
    x: 0.6, y: 4.6, w: 12, h: 0.5, fontFace: FONT, fontSize: 12.5, color: C.inkFaint, italic: true,
  });

  const stack = [
    ["Frontend", "React + D3.js knowledge-graph visualization"],
    ["Backend", "FastAPI, JWT + role-based access control"],
    ["Graph DB", "Neo4j \u2014 native multi-hop relationship queries"],
    ["AI Layer", "spaCy/IndicNLP + scikit-learn + RAG-constrained LLM"],
  ];
  const cw = 2.95, cgap = 0.25, cy = 5.45;
  stack.forEach((it, i) => {
    const x = 0.6 + i * (cw + cgap);
    s.addShape(pres.ShapeType.roundRect, { x, y: cy, w: cw, h: 1.35, rectRadius: 0.06, fill: { color: C.panel2 }, line: { color: C.border, width: 1 } });
    s.addText(it[0], { x: x + 0.18, y: cy + 0.15, w: cw - 0.36, h: 0.35, fontFace: FONT, fontSize: 12.5, bold: true, color: C.cyan });
    s.addText(it[1], { x: x + 0.18, y: cy + 0.52, w: cw - 0.36, h: 0.75, fontFace: FONT, fontSize: 10.5, color: C.inkDim, valign: "top" });
  });
}

// ============================================================
// SLIDE 5 — DIFFERENTIATOR: ENTITY RESOLUTION (real output)
// ============================================================
{
  const s = bgSlide("Most student projects skip this. We built it.", "Differentiator 01 \u2014 Entity Resolution");
  s.addText("Different documents describe the same person differently. Without resolving that, a knowledge graph fills with duplicate, disconnected nodes \u2014 and hides the very connections it's meant to find.", {
    x: 0.6, y: 2.0, w: 12, h: 0.75, fontFace: FONT, fontSize: 14, color: C.inkDim, valign: "top",
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 2.95, w: 12.1, h: 3.15, rectRadius: 0.08, fill: { color: C.panel }, line: { color: C.border, width: 1 } });
  s.addText("REAL OUTPUT FROM OUR WORKING ENGINE  (not a mockup)", { x: 0.95, y: 3.15, w: 8, h: 0.3, fontFace: FONT, fontSize: 10, color: C.amber, bold: true, charSpacing: 1.5 });

  const rows = [
    ["\u201cR. Malhotra\u201d", "Rajeev Malhotra", "80%", "AUTO-MERGE (flagged for confirmation)", C.cyan],
    ["\u201cA. Rao\u201d", "Anita Rao", "70%", "AUTO-MERGE (flagged for confirmation)", C.cyan],
    ["\u201cVikram S.\u201d", "Vikram Solanki", "80%", "AUTO-MERGE (flagged for confirmation)", C.cyan],
    ["\u201cFerozz Shiekh\u201d (misspelled)", "Feroz Sheikh", "48%", "SUGGESTED MATCH \u2014 requires manual review", C.amber],
  ];
  let ry = 3.6;
  rows.forEach((r) => {
    s.addText(r[0], { x: 0.95, y: ry, w: 3.4, h: 0.55, fontFace: FONT, fontSize: 12.5, color: C.ink, valign: "middle" });
    s.addText("\u2192  " + r[1], { x: 4.5, y: ry, w: 2.9, h: 0.55, fontFace: FONT, fontSize: 12.5, color: C.inkDim, valign: "middle" });
    s.addText(r[2], { x: 7.5, y: ry, w: 1, h: 0.55, fontFace: FONT, fontSize: 13, bold: true, color: r[4], valign: "middle" });
    s.addText(r[3], { x: 8.6, y: ry, w: 3.9, h: 0.55, fontFace: FONT, fontSize: 10.5, color: r[4], valign: "middle" });
    ry += 0.6;
  });
  s.addText("Note the last row: a misspelled name correctly drops to \u201crequires review\u201d instead of auto-merging \u2014 real false-positive protection, not a scripted demo.", {
    x: 0.6, y: 6.28, w: 12.1, h: 0.5, fontFace: FONT, fontSize: 11.5, italic: true, color: C.inkFaint,
  });
}

// ============================================================
// SLIDE 6 — DIFFERENTIATOR: EXPLAINABLE RISK SCORING (real chart)
// ============================================================
{
  const s = bgSlide("A transparent formula, not a black box", "Differentiator 02 \u2014 Explainable Risk Scoring");
  s.addText("Every score is a weighted, auditable formula \u2014 never an opaque ML classifier. Source reliability is a MULTIPLIER, so a pattern built on an anonymous tip can never score high, no matter how unusual it looks.", {
    x: 0.6, y: 2.0, w: 5.9, h: 1.4, fontFace: FONT, fontSize: 13, color: C.inkDim, valign: "top",
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 3.3, w: 5.9, h: 1.9, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.amber, width: 1 } });
  s.addText([
    { text: "Risk Score =", options: { color: C.inkDim, fontSize: 10.5, breakLine: true } },
    { text: "0.25\u00b7comm_anomaly + 0.20\u00b7financial_anomaly", options: { color: C.ink, fontSize: 10.5, bold: true, breakLine: true } },
    { text: "+ 0.20\u00b7centrality + 0.15\u00b7temporal", options: { color: C.ink, fontSize: 10.5, bold: true, breakLine: true } },
    { text: "+ 0.10\u00b7location + 0.10\u00b7resolution_conf.", options: { color: C.ink, fontSize: 10.5, bold: true, breakLine: true } },
    { text: "\u00d7 source_reliability_multiplier (0.4\u20131.0)", options: { color: C.amber, fontSize: 10.5, bold: true } },
  ], { x: 0.85, y: 3.45, w: 5.4, h: 1.6, fontFace: "Courier New", valign: "top", lineSpacingMultiple: 1.25 });

  s.addText("Every returned score is always shown with:", { x: 0.6, y: 5.42, w: 6, h: 0.3, fontFace: FONT, fontSize: 11.5, color: C.inkFaint });
  ["Full reasoning breakdown", "Source evidence record IDs", "\u201cRequires human verification\u201d flag"].forEach((t, i) => {
    s.addText("\u2713  " + t, { x: 0.6, y: 5.75 + i * 0.35, w: 6, h: 0.32, fontFace: FONT, fontSize: 12, color: C.cyan });
  });

  s.addChart(pres.ChartType.bar, [{
    name: "Risk Indicator Score",
    labels: ["Rajeev Malhotra", "Anita Rao", "Feroz Sheikh", "Vikram Solanki", "Kavita Joshi", "Arjun Kapoor"],
    values: [63.8, 42.6, 30.7, 26.5, 22.0, 11.8],
  }], {
    x: 6.85, y: 2.0, w: 5.9, h: 4.6,
    chartColors: [C.amber],
    showTitle: true, title: "Real computed scores (demo case)", titleColor: C.ink, titleFontSize: 13,
    showValue: true, dataLabelColor: C.ink, dataLabelFontSize: 10, dataLabelPosition: "outEnd",
    catAxisLabelColor: C.inkDim, catAxisLabelFontSize: 10,
    valAxisLabelColor: C.inkDim, valAxisLabelFontSize: 10,
    valGridLine: { color: C.border, size: 1 }, catGridLine: { style: "none" },
    showLegend: false, barDir: "bar",
    plotArea: { fill: { color: C.panel } }, chartArea: { fill: { color: C.bg } },
  });
}

// ============================================================
// SLIDE 7 — DIFFERENTIATOR: EVIDENCE-CITED AI ASSISTANT
// ============================================================
{
  const s = bgSlide("The LLM explains evidence. It never decides anything.", "Differentiator 03 \u2014 AI Investigation Assistant");
  s.addText("Every answer follows a fixed, auditable structure \u2014 constrained entirely to retrieved graph facts and source documents (RAG), never the model's own \u201cmemory.\u201d", {
    x: 0.6, y: 2.0, w: 12, h: 0.6, fontFace: FONT, fontSize: 14, color: C.inkDim,
  });

  const chain = ["Claim", "Supporting\nEntities", "Supporting\nRelationships", "Source\nRecords", "Confidence", "\u26a0 Human\nVerification"];
  const cw = 1.85, cgap = 0.2, cx0 = (13.333 - (chain.length * cw + (chain.length - 1) * cgap)) / 2, cy = 3.0;
  chain.forEach((t, i) => {
    const x = cx0 + i * (cw + cgap);
    const isLast = i === chain.length - 1;
    s.addShape(pres.ShapeType.roundRect, { x, y: cy, w: cw, h: 1.3, rectRadius: 0.06, fill: { color: C.panel }, line: { color: isLast ? C.red : C.cyan, width: 1.25 } });
    s.addText(t, { x: x + 0.08, y: cy, w: cw - 0.16, h: 1.3, fontFace: FONT, fontSize: 11.5, bold: true, color: isLast ? C.red : C.cyan, align: "center", valign: "middle" });
    if (i < chain.length - 1) {
      s.addShape(pres.ShapeType.line, { x: x + cw, y: cy + 0.65, w: cgap, h: 0, line: { color: C.inkFaint, width: 1.5, endArrowType: "triangle" } });
    }
  });

  s.addShape(pres.ShapeType.roundRect, { x: 1.3, y: 4.85, w: 10.7, h: 1.85, rectRadius: 0.08, fill: { color: C.panel2 }, line: { color: C.border, width: 1 } });
  s.addText("EXAMPLE QUERY", { x: 1.6, y: 5.05, w: 5, h: 0.3, fontFace: FONT, fontSize: 10, color: C.amber, bold: true, charSpacing: 1.5 });
  s.addText("\u201cWhy is this entity marked an investigative priority?\u201d", { x: 1.6, y: 5.35, w: 10, h: 0.35, fontFace: FONT, fontSize: 13.5, italic: true, color: C.ink });
  s.addText("\u2192 High network centrality + repeated contact with 2 flagged entities + financial link to Entity X. Evidence: CDR-104, TXN-209, FIR-031. Confidence: 78%. Requires human verification.", {
    x: 1.6, y: 5.8, w: 10.1, h: 0.75, fontFace: FONT, fontSize: 12, color: C.inkDim, valign: "top",
  });
}

// ============================================================
// SLIDE 8 — REAL RESULTS ON THE DEMO CASE
// ============================================================
{
  const s = bgSlide("What the engine found \u2014 on its own", "Live Demo Results");
  const stats = [
    ["30", "entities ingested"],
    ["34", "relationships mapped"],
    ["7", "communities detected"],
    ["4", "risk indicators auto-flagged"],
  ];
  const sw = 2.85, sgap = 0.25;
  stats.forEach((st, i) => {
    const x = 0.6 + i * (sw + sgap);
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.0, w: sw, h: 1.4, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.border, width: 1 } });
    s.addText(st[0], { x, y: 2.12, w: sw, h: 0.7, align: "center", fontFace: FONT, fontSize: 34, bold: true, color: C.cyan });
    s.addText(st[1], { x, y: 2.85, w: sw, h: 0.4, align: "center", fontFace: FONT, fontSize: 11, color: C.inkFaint });
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 3.75, w: 12.1, h: 2.85, rectRadius: 0.08, fill: { color: C.panel }, line: { color: C.amber, width: 1.25 } });
  s.addText("THE HIDDEN CHAIN \u2014 DISCOVERED BY THE ALGORITHM, NOT SCRIPTED", { x: 0.95, y: 3.95, w: 10, h: 0.3, fontFace: FONT, fontSize: 10.5, color: C.amber, bold: true, charSpacing: 1.5 });
  s.addText("Vikram Solanki  \u2192  Phone (+91 88\u2022\u2022\u20225561)  \u2192  Phone (+91 99\u2022\u2022\u20222207)  \u2192  Anita Rao", {
    x: 0.95, y: 4.4, w: 11.3, h: 0.55, fontFace: "Courier New", fontSize: 15.5, bold: true, color: C.ink,
  });
  s.addText("A low-level courier with no prior record was independently identified as the network's #1 bridging node by betweenness centrality \u2014 exactly the kind of connection a human analyst could spend days missing across scattered CDRs and FIRs.", {
    x: 0.95, y: 5.1, w: 11.3, h: 1.3, fontFace: FONT, fontSize: 13, color: C.inkDim, valign: "top",
  });
}

// ============================================================
// SLIDE 9 — TRUST & SAFETY
// ============================================================
{
  const s = bgSlide("Built for a courtroom, not just a demo", "Trust, Safety & False-Positive Protection");
  const cols = [
    ["No Auto-Accusation", "System structurally cannot output a \u201ccriminal\u201d label \u2014 only risk indicators requiring verification"],
    ["FACT / INFERENCE / LEAD", "Every generated report line is explicitly tagged so nothing is mistaken for confirmed fact"],
    ["Source Reliability Weighting", "An anonymous tip can never outscore a verified official record, by design"],
    ["Full Audit Trail", "Every AI suggestion and investigator decision is logged immutably"],
    ["Role-Based Access", "Admin / Senior Investigator / Investigator / Analyst / Viewer \u2014 least-privilege by default"],
    ["Prompt-Injection Safe", "Raw uploaded documents never reach the LLM directly \u2014 only pre-validated structured facts"],
  ];
  const cw = 3.9, cgap = 0.2, rh = 1.55;
  cols.forEach((c, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * (cw + cgap), y = 2.05 + row * (rh + 0.2);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: rh, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.border, width: 1 } });
    s.addText(c[0], { x: x + 0.2, y: y + 0.16, w: cw - 0.4, h: 0.4, fontFace: FONT, fontSize: 13, bold: true, color: C.cyan });
    s.addText(c[1], { x: x + 0.2, y: y + 0.58, w: cw - 0.4, h: 0.9, fontFace: FONT, fontSize: 10.5, color: C.inkDim, valign: "top" });
  });
}

// ============================================================
// SLIDE 10 — CLOSING
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addText("S\u016aTRA doesn't replace an investigator's judgment.", {
    x: 0.8, y: 2.5, w: 11.7, h: 0.8, fontFace: FONT, fontSize: 28, bold: true, color: C.ink,
  });
  s.addText("It gives them the thread to pull.", {
    x: 0.8, y: 3.25, w: 11.7, h: 0.8, fontFace: FONT, fontSize: 28, bold: true, color: C.amber,
  });
  s.addText("Entity Resolution \u00b7 Knowledge Graph Analytics \u00b7 Explainable Risk Scoring \u00b7 Evidence-Cited AI \u2014 all real, all working, all on synthetic data.", {
    x: 0.8, y: 4.35, w: 11, h: 0.6, fontFace: FONT, fontSize: 14, color: C.inkDim,
  });
  chip(s, "THANK YOU \u2014 QUESTIONS?", 0.8, 6.4, 3.6, C.cyan);
}

pres.writeFile({ fileName: "/home/claude/sutra/pitch/sutra-pitch-deck.pptx" }).then(() => {
  console.log("Deck written.");
});
