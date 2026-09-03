const DATA = __DATA_JSON__;

/* ============================================================
   I18N — English / Hindi / Marathi
   ============================================================ */
const I18N = {
en: {
  gov_strip: "GOVERNMENT LAW-ENFORCEMENT DECISION-SUPPORT PROTOTYPE",
  gov_strip_synthetic: "SYNTHETIC DEMONSTRATION DATA ONLY",
  gov_strip_verify: "ALL OUTPUTS REQUIRE HUMAN VERIFICATION",
  land_nav_1: "ANALYTICAL CAPABILITIES", land_nav_2: "SECURE ACCESS PROTOCOL", land_nav_3: "GOVERNMENT DISCLAIMER",
  hero_title: "The Connection Thread",
  hero_subtitle: "Uncovering the invisible networks of crime. A unified investigative decision-support platform for entity resolution, knowledge-graph analysis, and evidence-backed leads \u2014 built for institutional accountability, not automated accusation.",
  btn_request_access: "Request Access \u2192 Command Center",
  btn_view_briefing: "View Briefing",
  caps_title: "Analytical Capabilities", caps_subtitle: "Core modules for advanced investigative decision-support.",
  cap1_title: "Data Integration", cap1_desc: "Harmonize FIRs, CDRs, financial records, and surveillance reports into one structured investigative namespace.",
  cap2_title: "Entity Extraction & Resolution", cap2_desc: "Automated identification of persons, phones, vehicles, and organizations \u2014 with confidence-scored merging of duplicate mentions.",
  cap3_title: "Relationship Mapping", cap3_desc: "Visualize covert networks. Trace financial flows, communication linkages, and hierarchical structures dynamically.",
  cap3_module: "CORE MODULE", cap3_visual: "Network Graph Visualization",
  cap4_title: "Explainable Risk Scoring", cap4_desc: "Transparent, source-weighted risk indicators \u2014 every score fully traceable to evidence, always requiring human verification. No automated accusation, ever.",
  btn_view_docs: "View Documentation",
  footer_copyright: "\u00a9 2026 S\u016aTRA Investigative Intelligence Platform. Prototype \u2014 Restricted Demonstration Use Only.",
  footer_link1: "Secure Access Protocol", footer_link2: "Privacy Policy", footer_link3: "Government Disclaimer", footer_link4: "Contact Administrator",
  stamp_demo: "DEMO \u00b7 SYNTHETIC DATA",
  brand_tagline: "INTELLIGENCE PLATFORM",
  nav_landing: "← Landing / Briefing",
  nav_command: "Command Center", nav_graph: "Network Explorer", nav_profiles: "Entity Profiles",
  nav_datalab: "Data Lab", nav_report: "Analytics Report", nav_assistant: "AI Assistant", nav_settings: "Settings", nav_security: "Security",
  sidebar_gov_note: "GOVERNMENT PROTOTYPE\nSYNTHETIC DATA ONLY",
  meta_entities: "nodes", meta_links: "links",
  case_id_label: "Case ID", entities_resolved_label: "Entities Resolved", engine_status_label: "Engine Status", live_data: "LIVE DATA",
  tb_command: "Command Center", badge_secure: "CONNECTION SECURE",
  tb_graph: "Network Explorer", badge_secure_short: "SECURE", active_graph: "Active Graph: Operation Case MH/CID/2026/0417",
  tb_profiles: "Entity Profiles", persons_of_interest: "PERSONS OF INTEREST",
  tb_datalab: "Data Lab Workspace", badge_doc_analysis: "DOCUMENT ANALYSIS",
  tb_report: "Analytics Report", badge_tagged: "FACT / INFERENCE / LEAD TAGGED",
  stat_live: "LIVE", stat_flagged: "FLAGGED", stat_detected: "DETECTED", stat_monitored: "MONITORED",
  stat_entities_resolved: "Entities Resolved", stat_high_priority: "High-Priority Risk Indicators",
  stat_communities: "Network Communities", stat_suspicious_links: "Suspicious Links",
  feed_title: "Live Investigation Feed", source_prefix: "Source:",
  feed_sev_critical: "critical", feed_sev_warning: "warning", feed_sev_info: "info",
  feed_msg_1: (a,b)=>`Communication burst flagged: ${a} \u2194 ${b} \u2014 27 calls in 48 hrs`,
  feed_msg_2: (n)=>`${n} entity mention(s) require manual review \u2014 confidence below auto-merge threshold`,
  feed_msg_3: (n,e)=>`Knowledge graph rebuilt: ${n} entities, ${e} relationships indexed`,
  feed_msg_4: "Large financial transfer exceeded anomaly threshold \u2014 see Analytics Report",
  feed_src_1: "CDR Analysis Engine", feed_src_2: "Entity Resolution Engine", feed_src_3: "Graph Analytics Engine", feed_src_4: "Risk Scoring Engine",
  feed_time_1: "Just now", feed_time_2: "5 min ago", feed_time_3: "12 min ago", feed_time_4: "18 min ago",
  communities_title: "Detected Communities",
  investigator_query: "Investigator Query", search_placeholder: "Search person, phone, location\u2026",
  ingested_sources: "Ingested Sources", entity_layers: "Entity Layers",
  about_graph_title: "About this graph",
  about_graph_text: "Every node, edge, and centrality value here was computed by the real Python analytics engine (NetworkX degree/betweenness/PageRank + modularity community detection) \u2014 not hardcoded.",
  reset_view: "Reset View",
  graph_hint: "Drag to reposition \u00b7 Scroll to zoom \u00b7 Click a node to inspect",
  graph_error_title: "\u26a0 Graph rendering failed to initialize.",
  graph_error_sub: "Other pages are unaffected.",
  empty_select_node: "SELECT A NODE ON THE GRAPH\nTO VIEW ITS INVESTIGATIVE PROFILE",
  priority_entities_title: "Investigative-Priority Entities", priority_entities_sub: "(blended centrality)",
  type_persons: "Persons", type_phones: "Phone Numbers", type_locations: "Locations",
  type_vehicles: "Vehicles", type_orgs: "Organizations", type_accounts: "Bank Accounts",
  traced_entity: "TRACED ENTITY", network_centrality: "Network Centrality", degree_centrality: "Degree Centrality",
  key_attributes: "Key Attributes", connections: "Connections", aliases: "Aliases",
  none_on_record: "None on record", last_known_location: "Last Known Location", unrecorded: "Unrecorded",
  why_score: "Why This Score", source_reliability_mult: "Source reliability multiplier",
  human_verify_short: "HUMAN VERIFICATION REQUIRED",
  traced_connections: "Traced Connections",
  reason_comm: (v)=>`Elevated communication anomaly score (${v})`,
  reason_fin: (v)=>`Financial transaction anomaly detected (${v})`,
  reason_net: (v)=>`High network centrality (${v})`,
  reason_temporal: "Activity clustered near a flagged time window",
  reason_location: "Location overlap with a flagged site",
  reason_none: "No strong individual risk factors \u2014 score driven by baseline network position",
  persons_of_interest_suffix: "PERSONS OF INTEREST",
  aliases_prefix: "Aliases:", no_aliases: "No aliases on record",
  risk_high: "HIGH RISK", risk_medium: "MEDIUM RISK", risk_low: "LOW RISK", risk_unrated: "UNRATED RISK",
  breadcrumb_profiles: "Entity Profiles",
  pd_alias_label: "Alias:", pd_last_known_label: "Last Known:",
  pd_flag_btn: "Mark for Review", pd_flag_btn_done: "Flagged for Review",
  pd_briefing_title: "Investigative Briefing", pd_computed_tag: "COMPUTED",
  pd_briefing_auto: (name, reasons)=>`Automated analysis indicates <b>${name}</b> shows ${reasons}. This is a computed <b>risk indicator</b>, not a finding of fact \u2014 it identifies a pattern worth an investigator's attention, nothing more.`,
  pd_briefing_baseline: "a baseline network position with no strong individual risk factors",
  pd_briefing_none: (name)=>`No computed risk indicators are on record for <b>${name}</b>. This entity appears in the graph via its recorded relationships only.`,
  pd_risk_score_label: "Risk Indicator Score", pd_source_mult_label: "Source reliability multiplier applied",
  pd_confidence_label: "Confidence in underlying entity resolution",
  pd_alias_corrob: (n)=>`corroborated by ${n} resolved alias mention(s)`,
  pd_no_alias_corrob: "no alias corroboration on record",
  pd_degree_centrality: "Degree Centrality", pd_betweenness: "Betweenness", pd_connections: "Connections",
  pd_verify_note: "HUMAN VERIFICATION REQUIRED \u2014 not an accusation",
  pd_connection_matrix_title: "Connection Matrix", pd_open_explorer: "Open in Network Explorer \u2192",
  pd_identifiers_title: "Identifiers", pd_entity_id: "Entity ID", pd_primary_affiliation: "Primary Affiliation",
  pd_known_aliases: "Known Aliases", pd_risk_assessment: "Risk Assessment",
  pd_timeline_title: "Operational Timeline", pd_no_timeline: "No recorded location visits for this entity.",
  pd_date_unrecorded: "Date unrecorded", pd_graph_unavailable: "Graph unavailable",
  dl_extraction_model: "Extraction Model", dl_model_option: "Rule-Based NER v1 (regex + gazetteer)",
  dl_merge_threshold: "Merge Confidence Threshold", dl_active_classes: "Active Entity Classes",
  dl_conflicts_title: "Data Conflicts", dl_auto_merge: "Auto-Merge Suggested", dl_needs_review: "Needs Manual Review",
  dl_source_prefix: "source:", btn_accept: "Accept", btn_accept_done: "\u2713 Accepted", btn_edit: "Edit",
  alert_edit_msg: "Manual correction workflow: an investigator would adjust or reject this match here. Not wired up in this prototype.",
  mode_sample: "Sample Documents", mode_custom: "Paste Your Own Text", mode_upload: "Upload Source File",
  upload_title: "Upload Source File", upload_sub: "Drag & drop or browse \u2014 plain text (.txt) files only in this prototype",
  upload_loaded: (name, kb)=>`Loaded: ${name} (${kb} KB)`,
  upload_txt_only: "This prototype reads plain .txt files only \u2014 PDF/DOCX parsing needs the production OCR pipeline (see backend/).",
  upload_read_error: "Could not read this file.",
  textarea_placeholder: "Type or paste an FIR excerpt, surveillance note, or informant report\u2026",
  btn_run_extraction: "Run Extraction", btn_example1: "Load Example 1", btn_example2: "Load Example 2",
  extraction_result_title: "Extraction Result", no_entities_detected: "No structured entities detected", no_text_entered: "(no text entered)",
  source_reliability_label: "SOURCE RELIABILITY",
  risk_indicator_label: "Risk Indicator",
  tb_assistant: "AI Investigation Assistant", badge_evidence_cited: "EVIDENCE-CITED ANSWERS ONLY",
  asst_placeholder: "Ask about an entity, a connection, or the case\u2026", asst_send: "Ask",
  asst_welcome: "I can answer questions about this case using only the evidence in the knowledge graph \u2014 every answer is cited. Try a question below, or type your own.",
  asst_you: "You",
  asst_evidence_label: "EVIDENCE", asst_confidence_label: "Confidence", asst_source_label: "Source",
  asst_verify_note: "\u26a0 Requires human verification \u2014 not a finding of fact.",
  asst_graph_verified: "Graph-verified structural connection.",
  asst_no_entity_found: "I couldn't match that to a known entity in this case. Try a full or partial name, e.g. \"Rajeev\" or \"Shree Trading\".",
  asst_need_two_entities: "I found one entity in your question, but connection queries need two. Try: \"Who connects Rajeev Malhotra and Anita Rao?\"",
  asst_path_intro: (a,b)=>`Shortest connection path between <b>${a}</b> and <b>${b}</b>:`,
  asst_path_none: (a,b)=>`No path was found between <b>${a}</b> and <b>${b}</b> in the current graph \u2014 they appear to belong to unrelated clusters, or are connected only through entities outside this case.`,
  asst_path_hops: (n)=>`${n} hop(s)`,
  asst_why_intro: (name, score)=>`<b>${name}</b> has a computed Risk Indicator Score of <b>${score}/100</b>. This reflects:`,
  asst_why_none: (name)=>`<b>${name}</b> has no computed risk indicators on record \u2014 no unusual patterns were detected for this entity.`,
  asst_connections_intro: (name, n)=>`<b>${name}</b> has <b>${n}</b> recorded connection(s):`,
  asst_connections_none: (name)=>`<b>${name}</b> has no recorded connections in the current graph.`,
  asst_top_priority_intro: "Top investigative-priority entities, ranked by blended centrality (degree + betweenness + PageRank):",
  asst_summary_intro: "Case summary, computed directly from the current knowledge graph:",
  asst_summary_entities: (n)=>`${n} entities`,
  asst_summary_edges: (n)=>`${n} relationships`,
  asst_summary_communities: (n)=>`${n} detected communities`,
  asst_summary_highrisk: (n)=>`${n} high-priority risk indicator(s)`,
  asst_summary_suspicious: (n)=>`${n} flagged suspicious link(s)`,
  asst_financial_intro: "Flagged financial transfers in this case:",
  asst_financial_none: "No financial transfers are recorded in this case.",
  asst_suspicious_intro: "Suspicious or flagged links currently in the network:",
  asst_suspicious_none: "No suspicious links are currently flagged in this case.",
  asst_entity_profile_intro: (name, type)=>`<b>${name}</b> (${type}):`,
  asst_fallback: "I'm not sure how to answer that yet. I can help with questions like:",
  asst_amount_label: "Amount", asst_between_label: "Between", asst_relationship_label: "Relationship",
  asst_typing: "Thinking\u2026",
  chip_who_connects: "Who connects Rajeev Malhotra and Anita Rao?",
  chip_why_flagged: "Why is Vikram Solanki flagged?",
  chip_top_priority: "Show top priority entities",
  chip_summarize: "Summarize this case",
  chip_suspicious: "Show suspicious links",
  chip_financial: "Show flagged financial transfers",
},
hi: {
  gov_strip: "\u0938\u0930\u0915\u093e\u0930\u0940 \u0915\u093e\u0928\u0942\u0928-\u092a\u094d\u0930\u0935\u0930\u094d\u0924\u0928 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u0924\u093e \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a",
  gov_strip_synthetic: "\u0915\u0947\u0935\u0932 \u0938\u093f\u0902\u0925\u0947\u091f\u093f\u0915 \u092a\u094d\u0930\u0926\u0930\u094d\u0936\u0928 \u0921\u0947\u091f\u093e",
  gov_strip_verify: "\u0938\u092d\u0940 \u0906\u0909\u091f\u092a\u0941\u091f \u0915\u0947 \u0932\u093f\u090f \u092e\u093e\u0928\u0935 \u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0906\u0935\u0936\u094d\u092f\u0915",
  land_nav_1: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\u093e\u0924\u094d\u092e\u0915 \u0915\u094d\u0937\u092e\u0924\u093e\u090f\u0902", land_nav_2: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u092a\u0939\u0941\u0902\u091a \u092a\u094d\u0930\u094b\u091f\u094b\u0915\u0949\u0932", land_nav_3: "\u0938\u0930\u0915\u093e\u0930\u0940 \u0905\u0938\u094d\u0935\u0940\u0915\u0930\u0923",
  hero_title: "\u0938\u0902\u092c\u0902\u0927 \u0915\u093e \u0938\u0942\u0924\u094d\u0930",
  hero_subtitle: "\u0905\u092a\u0930\u093e\u0927 \u0915\u0947 \u0905\u0926\u0943\u0936\u094d\u092f \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u094b \u0909\u091c\u093e\u0917\u0930 \u0915\u0930\u0928\u093e\u0964 \u0907\u0915\u093e\u0908 \u0938\u092e\u093e\u0927\u093e\u0928, \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b़ \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0914\u0930 \u0938\u093e\u0915\u094d\u0937\u094d\u092f-\u0938\u092e\u0930\u094d\u0925\u093f\u0924 \u0938\u0941\u0930\u093e\u0917 \u0915\u0947 \u0932\u093f\u090f \u090f\u0915 \u0938\u092e\u0947\u0915\u093f\u0924 \u091c\u093e\u0902\u091a-\u0938\u0939\u093e\u092f\u0924\u093e \u092a\u094d\u0932\u0947\u091f\u092b़\u0949\u0930\u094d\u092e \u2014 \u0938\u0902\u0938\u094d\u0925\u093e\u0917\u0924 \u091c\u0935\u093e\u092c\u0926\u0947\u0939\u0940 \u0915\u0947 \u0932\u093f\u090f \u092c\u0928\u093e\u092f\u093e \u0917\u092f\u093e, \u0938\u094d\u0935\u091a\u093e\u0932\u093f\u0924 \u0906\u0930\u094b\u092a \u0915\u0947 \u0932\u093f\u090f \u0928\u0939\u0940\u0902\u0964",
  btn_request_access: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930 \u0915\u0947 \u0932\u093f\u090f \u092a\u0939\u0941\u0902\u091a \u0915\u093e \u0905\u0928\u0941\u0930\u094b\u0927 \u0915\u0930\u0947\u0902 \u2192",
  btn_view_briefing: "\u092c\u094d\u0930\u0940\u092b़\u093f\u0902\u0917 \u0926\u0947\u0916\u0947\u0902",
  caps_title: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\u093e\u0924\u094d\u092e\u0915 \u0915\u094d\u0937\u092e\u0924\u093e\u090f\u0902", caps_subtitle: "\u0909\u0928\u094d\u0928\u0924 \u091c\u093e\u0902\u091a-\u0938\u0939\u093e\u092f\u0924\u093e \u0939\u0947\u0924\u0941 \u092e\u0942\u0932 \u092e\u0949\u0921\u094d\u092f\u0942\u0932\u0964",
  cap1_title: "\u0921\u0947\u091f\u093e \u0913\u0915\u0940\u0915\u0930\u0923", cap1_desc: "FIR, CDR, \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0930\u093f\u0915\u0949\u0930\u094d\u0921 \u0914\u0930 \u0928\u093f\u0917\u0930\u093e\u0928\u0940 \u0930\u093f\u092a\u094b\u0930\u094d\u091f \u0915\u094b \u090f\u0915 \u0938\u0902\u0930\u091a\u093f\u0924 \u091c\u093e\u0902\u091a \u0938\u094d\u0925\u093e\u0928 \u092e\u0947\u0902 \u0938\u092e\u0928\u094d\u0935\u093f\u0924 \u0915\u0930\u0947\u0902\u0964",
  cap2_title: "\u0907\u0915\u093e\u0908 \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937\u0923 \u0914\u0930 \u0938\u092e\u093e\u0927\u093e\u0928", cap2_desc: "\u0935\u094d\u092f\u0915\u094d\u0924\u093f\u092f\u094b\u0902, \u092b़\u094b\u0928, \u0935\u093e\u0939\u0928\u094b\u0902 \u0914\u0930 \u0938\u0902\u0917\u0920\u0928\u094b\u0902 \u0915\u0940 \u0938\u094d\u0935\u091a\u093e\u0932\u093f\u0924 \u092a\u0939\u091a\u093e\u0928 \u2014 \u0921\u0941\u092a\u094d\u0932\u0940\u0915\u0947\u091f \u0909\u0932\u094d\u0932\u0947\u0916\u094b\u0902 \u0915\u0947 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e-\u0938\u094d\u0915\u094b\u0930 \u0935\u093f\u0932\u092f \u0915\u0947 \u0938\u093e\u0925\u0964",
  cap3_title: "\u0938\u0902\u092c\u0902\u0927 \u092e\u0948\u092a\u093f\u0902\u0917", cap3_desc: "\u0917\u0941\u092a\u094d\u0924 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u093e \u0926\u0943\u0936\u094d\u092f\u0940\u0915\u0930\u0923\u0964 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u092a\u094d\u0930\u0935\u093e\u0939, \u0938\u0902\u091a\u093e\u0930 \u0938\u0902\u092c\u0902\u0927 \u0914\u0930 \u0938\u094d\u0924\u0930\u0940\u0915\u0943\u0924 \u0938\u0902\u0930\u091a\u0928\u093e\u0913\u0902 \u0915\u094b \u0917\u0924\u093f\u0936\u0940\u0932 \u0930\u0942\u092a \u0938\u0947 \u091f\u094d\u0930\u0947\u0938 \u0915\u0930\u0947\u0902\u0964",
  cap3_module: "\u092e\u0942\u0932 \u092e\u0949\u0921\u094d\u092f\u0942\u0932", cap3_visual: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0917\u094d\u0930\u093e\u092b़ \u0926\u0943\u0936\u094d\u092f\u0940\u0915\u0930\u0923",
  cap4_title: "\u0935\u094d\u092f\u093e\u0916\u094d\u092f\u0947\u092f \u091c\u094b\u0916\u093f\u092e \u0938\u094d\u0915\u094b\u0930\u093f\u0902\u0917", cap4_desc: "\u092a\u093e\u0930\u0926\u0930\u094d\u0936\u0940, \u0938\u094d\u0930\u094b\u0924-\u092d\u093e\u0930\u093f\u0924 \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 \u2014 \u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0938\u094d\u0915\u094b\u0930 \u092a\u0942\u0930\u0940 \u0924\u0930\u0939 \u0938\u093e\u0915\u094d\u0937\u094d\u092f-\u0906\u0927\u093e\u0930\u093f\u0924, \u0939\u092e\u0947\u0936\u093e \u092e\u093e\u0928\u0935 \u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0906\u0935\u0936\u094d\u092f\u0915\u0964 \u0915\u092d\u0940 \u0915\u094b\u0908 \u0938\u094d\u0935\u091a\u093e\u0932\u093f\u0924 \u0906\u0930\u094b\u092a \u0928\u0939\u0940\u0902\u0964",
  btn_view_docs: "\u0926\u0938\u094d\u0924\u093e\u0935\u0947\u095b़ \u0926\u0947\u0916\u0947\u0902",
  footer_copyright: "\u00a9 2026 \u0938\u0942\u0924\u094d\u0930 \u091c\u093e\u0902\u091a \u0916\u0941\u092b़\u093f\u092f\u093e \u092a\u094d\u0932\u0947\u091f\u092b़\u0949\u0930\u094d\u092e\u0964 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u2014 \u0915\u0947\u0935\u0932 \u092a\u094d\u0930\u0926\u0930\u094d\u0936\u0928 \u0939\u0947\u0924\u0941\u0964",
  footer_link1: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u092a\u0939\u0941\u0902\u091a \u092a\u094d\u0930\u094b\u091f\u094b\u0915\u0949\u0932", footer_link2: "\u0917\u094b\u092a\u0928\u0940\u092f\u0924\u093e \u0928\u0940\u0924\u093f", footer_link3: "\u0938\u0930\u0915\u093e\u0930\u0940 \u0905\u0938\u094d\u0935\u0940\u0915\u0930\u0923", footer_link4: "\u092a\u094d\u0930\u0936\u093e\u0938\u0915 \u0938\u0947 \u0938\u0902\u092a\u0930\u094d\u0915 \u0915\u0930\u0947\u0902",
  stamp_demo: "\u0921\u0947\u092e\u094b \u00b7 \u0938\u093f\u0902\u0925\u0947\u091f\u093f\u0915 \u0921\u0947\u091f\u093e",
  brand_tagline: "\u0907\u0902\u091f\u0947\u0932\u093f\u091c\u0947\u0902\u0938 \u092a\u094d\u0932\u0947\u091f\u092b़\u0949\u0930\u094d\u092e",
  nav_landing: "← मुख्यपृष्ठ / विवरण",
  nav_command: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930", nav_graph: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930", nav_profiles: "\u0907\u0915\u093e\u0908 \u092a\u094d\u0930\u094b\u092b़\u093e\u0907\u0932",
  nav_datalab: "\u0921\u0947\u091f\u093e \u0932\u0948\u092c", nav_report: "\u090f\u0928\u093e\u0932\u093f\u091f\u093f\u0915\u094d\u0938 \u0930\u093f\u092a\u094b\u0930\u094d\u091f", nav_assistant: "\u090f\u0906\u0908 \u0938\u0939\u093e\u092f\u0915", nav_settings: "\u0938\u0947\u091f\u093f\u0902\u0917\u094d\u0938", nav_security: "\u0938\u0941\u0930\u0915\u094d\u0937\u093e",
  sidebar_gov_note: "\u0938\u0930\u0915\u093e\u0930\u0940 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a\n\u0915\u0947\u0935\u0932 \u0938\u093f\u0902\u0925\u0947\u091f\u093f\u0915 \u0921\u0947\u091f\u093e",
  meta_entities: "\u0928\u094b\u0921\u094d\u0938", meta_links: "\u0932\u093f\u0902\u0915",
  case_id_label: "\u092e\u093e\u092e\u0932\u093e \u0906\u0908\u0921\u0940", entities_resolved_label: "\u0939\u0932 \u0915\u0940 \u0917\u0908 \u0907\u0915\u093e\u0907\u092f\u093e\u0902", engine_status_label: "\u0907\u0902\u091c\u0928 \u0938\u094d\u0925\u093f\u0924\u093f", live_data: "\u0932\u093e\u0907\u0935 \u0921\u0947\u091f\u093e",
  tb_command: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930", badge_secure: "\u0915\u0928\u0947\u0915\u094d\u0936\u0928 \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924",
  tb_graph: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930", badge_secure_short: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924", active_graph: "\u0938\u0915\u094d\u0930\u093f\u092f \u0917\u094d\u0930\u093e\u092b़: \u0911\u092a\u0930\u0947\u0936\u0928 \u0915\u0947\u0938 MH/CID/2026/0417",
  tb_profiles: "\u0907\u0915\u093e\u0908 \u092a\u094d\u0930\u094b\u092b़\u093e\u0907\u0932", persons_of_interest: "\u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0935\u094d\u092f\u0915\u094d\u0924\u093f",
  tb_datalab: "\u0921\u0947\u091f\u093e \u0932\u0948\u092c \u0935\u0930\u094d\u0915\u0938\u094d\u092a\u0947\u0938", badge_doc_analysis: "\u0926\u0938\u094d\u0924\u093e\u0935\u0947\u095b़ \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923",
  tb_report: "\u090f\u0928\u093e\u0932\u093f\u091f\u093f\u0915\u094d\u0938 \u0930\u093f\u092a\u094b\u0930\u094d\u091f", badge_tagged: "\u0924\u0925\u094d\u092f / \u0905\u0928\u0941\u092e\u093e\u0928 / \u0938\u0941\u091d\u093e\u0935 \u091f\u0948\u0917\u094d\u0921",
  stat_live: "\u0932\u093e\u0907\u0935", stat_flagged: "\u091a\u093f\u0928\u094d\u0939\u093f\u0924", stat_detected: "\u092a\u0924\u093e \u091a\u0932\u093e", stat_monitored: "\u0928\u093f\u0917\u0930\u093e\u0928\u0940 \u092e\u0947\u0902",
  stat_entities_resolved: "\u0939\u0932 \u0915\u0940 \u0917\u0908 \u0907\u0915\u093e\u0907\u092f\u093e\u0902", stat_high_priority: "\u0909\u091a\u094d\u091a-\u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915",
  stat_communities: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u092e\u0941\u0926\u093e\u092f", stat_suspicious_links: "\u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0932\u093f\u0902\u0915",
  feed_title: "\u0932\u093e\u0907\u0935 \u091c\u093e\u0902\u091a \u092b़\u0940\u0921", source_prefix: "\u0938\u094d\u0930\u094b\u0924:",
  feed_sev_critical: "\u0917\u0902\u092d\u0940\u0930", feed_sev_warning: "\u091a\u0947\u0924\u093e\u0935\u0928\u0940", feed_sev_info: "\u091c\u093e\u0928\u0915\u093e\u0930\u0940",
  feed_msg_1: (a,b)=>`\u0938\u0902\u091a\u093e\u0930 \u0935\u0943\u0926\u094d\u0927\u093f \u091a\u093f\u0928\u094d\u0939\u093f\u0924: ${a} \u2194 ${b} \u2014 48 \u0918\u0902\u091f\u094b\u0902 \u092e\u0947\u0902 27 \u0915\u0949\u0932`,
  feed_msg_2: (n)=>`${n} \u0907\u0915\u093e\u0908 \u0909\u0932\u094d\u0932\u0947\u0916 \u0915\u094b \u092e\u0948\u0928\u0941\u0905\u0932 \u0938\u092e\u0940\u0915\u094d\u0937\u093e \u0915\u0940 \u0906\u0935\u0936\u094d\u092f\u0915\u0924\u093e \u2014 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e \u0911\u091f\u094b-\u092e\u0930\u094d\u091c \u0938\u0940\u092e\u093e \u0938\u0947 \u0915\u092e`,
  feed_msg_3: (n,e)=>`\u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b़ \u092a\u0941\u0928\u0930\u094d\u0928\u093f\u0930\u094d\u092e\u093f\u0924: ${n} \u0907\u0915\u093e\u0907\u092f\u093e\u0902, ${e} \u0938\u0902\u092c\u0902\u0927 \u0938\u0942\u091a\u0940\u092c\u0926\u094d\u0927`,
  feed_msg_4: "\u092c\u0921़\u093e \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923 \u0935\u093f\u0938\u0902\u0917\u0924\u093f \u0938\u0940\u092e\u093e \u0938\u0947 \u0905\u0927\u093f\u0915 \u2014 \u090f\u0928\u093e\u0932\u093f\u091f\u093f\u0915\u094d\u0938 \u0930\u093f\u092a\u094b\u0930\u094d\u091f \u0926\u0947\u0916\u0947\u0902",
  feed_src_1: "CDR \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u0928", feed_src_2: "\u0907\u0915\u093e\u0908 \u0938\u092e\u093e\u0927\u093e\u0928 \u0907\u0902\u091c\u0928", feed_src_3: "\u0917\u094d\u0930\u093e\u092b़ \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u0928", feed_src_4: "\u091c\u094b\u0916\u093f\u092e \u0938\u094d\u0915\u094b\u0930\u093f\u0902\u0917 \u0907\u0902\u091c\u0928",
  feed_time_1: "\u0905\u092d\u0940 \u0905\u092d\u0940", feed_time_2: "5 \u092e\u093f\u0928\u091f \u092a\u0939\u0932\u0947", feed_time_3: "12 \u092e\u093f\u0928\u091f \u092a\u0939\u0932\u0947", feed_time_4: "18 \u092e\u093f\u0928\u091f \u092a\u0939\u0932\u0947",
  communities_title: "\u092a\u093e\u090f \u0917\u090f \u0938\u092e\u0941\u0926\u093e\u092f",
  investigator_query: "\u091c\u093e\u0902\u091a\u0915\u0930\u094d\u0924\u093e \u0916\u094b\u091c", search_placeholder: "\u0935\u094d\u092f\u0915\u094d\u0924\u093f, \u092b़\u094b\u0928, \u0938\u094d\u0925\u093e\u0928 \u0916\u094b\u091c\u0947\u0902\u2026",
  ingested_sources: "\u0926\u0930\u094d\u091c \u0938\u094d\u0930\u094b\u0924", entity_layers: "\u0907\u0915\u093e\u0908 \u092a\u0930\u0924\u0947\u0902",
  about_graph_title: "\u0907\u0938 \u0917\u094d\u0930\u093e\u092b़ \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902",
  about_graph_text: "\u092f\u0939\u093e\u0902 \u0939\u0930 \u0928\u094b\u0921, \u090f\u091c \u0914\u0930 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e \u092e\u093e\u0928 \u0935\u093e\u0938\u094d\u0924\u0935\u093f\u0915 \u092a\u093e\u092f\u0925\u0928 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u0928 \u0926\u094d\u0935\u093e\u0930\u093e \u0917\u0923\u093f\u0924 \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0925\u093e \u2014 \u0939\u093e\u0930\u094d\u0921\u0915\u094b\u0921\u0947\u0921 \u0928\u0939\u0940\u0902\u0964",
  reset_view: "\u0930\u0940\u0938\u0947\u091f \u0935\u094d\u092f\u0942",
  graph_hint: "\u0938\u094d\u0925\u093e\u0928\u093e\u0902\u0924\u0930\u093f\u0924 \u0915\u0930\u0928\u0947 \u0939\u0947\u0924\u0941 \u0916\u0940\u0902\u091a\u0947\u0902 \u00b7 \u091c़\u0942\u092e \u0939\u0947\u0924\u0941 \u0938\u094d\u0915\u094d\u0930\u0949\u0932 \u0915\u0930\u0947\u0902 \u00b7 \u091c\u093e\u0902\u091a \u0939\u0947\u0924\u0941 \u0928\u094b\u0921 \u092a\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u0947\u0902",
  graph_error_title: "\u26a0 \u0917\u094d\u0930\u093e\u092b़ \u0930\u0947\u0902\u0921\u0930\u093f\u0902\u0917 \u0936\u0941\u0930\u0942 \u0928\u0939\u0940\u0902 \u0939\u094b \u0938\u0915\u0940\u0964",
  graph_error_sub: "\u0905\u0928\u094d\u092f \u092a\u0947\u091c \u092a\u094d\u0930\u092d\u093e\u0935\u093f\u0924 \u0928\u0939\u0940\u0902 \u0939\u0948\u0902\u0964",
  empty_select_node: "\u0907\u0938\u0915\u0940 \u091c\u093e\u0902\u091a \u092a\u094d\u0930\u094b\u092b़\u093e\u0907\u0932 \u0926\u0947\u0916\u0928\u0947 \u0939\u0947\u0924\u0941\n\u0917\u094d\u0930\u093e\u092b़ \u092a\u0930 \u090f\u0915 \u0928\u094b\u0921 \u091a\u0941\u0928\u0947\u0902",
  priority_entities_title: "\u091c\u093e\u0902\u091a-\u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0907\u0915\u093e\u0907\u092f\u093e\u0902", priority_entities_sub: "(\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e)",
  type_persons: "\u0935\u094d\u092f\u0915\u094d\u0924\u093f", type_phones: "\u092b़\u094b\u0928 \u0928\u0902\u092c\u0930", type_locations: "\u0938\u094d\u0925\u093e\u0928",
  type_vehicles: "\u0935\u093e\u0939\u0928", type_orgs: "\u0938\u0902\u0917\u0920\u0928", type_accounts: "\u092c\u0948\u0902\u0915 \u0916\u093e\u0924\u0947",
  traced_entity: "\u091f\u094d\u0930\u0947\u0938 \u0915\u0940 \u0917\u0908 \u0907\u0915\u093e\u0908", network_centrality: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e", degree_centrality: "\u0921\u093f\u0917\u094d\u0930\u0940 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e",
  key_attributes: "\u092e\u0941\u0916\u094d\u092f \u0917\u0941\u0923", connections: "\u0938\u0902\u092c\u0902\u0927", aliases: "\u0909\u092a\u0928\u093e\u092e",
  none_on_record: "\u0930\u093f\u0915\u0949\u0930\u094d\u0921 \u092e\u0947\u0902 \u0915\u094b\u0908 \u0928\u0939\u0940\u0902", last_known_location: "\u0905\u0902\u0924\u093f\u092e \u091c\u094d\u091e\u093e\u0924 \u0938\u094d\u0925\u093e\u0928", unrecorded: "\u0905\u0902\u0915\u093f\u0924 \u0928\u0939\u0940\u0902",
  why_score: "\u092f\u0939 \u0938\u094d\u0915\u094b\u0930 \u0915\u094d\u092f\u094b\u0902", source_reliability_mult: "\u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e \u0917\u0941\u0923\u0915",
  human_verify_short: "\u092e\u093e\u0928\u0935 \u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0906\u0935\u0936\u094d\u092f\u0915",
  traced_connections: "\u091f\u094d\u0930\u0947\u0938 \u0915\u093f\u090f \u0917\u090f \u0938\u0902\u092c\u0902\u0927",
  reason_comm: (v)=>`\u0909\u091a\u094d\u091a \u0938\u0902\u091a\u093e\u0930 \u0935\u093f\u0938\u0902\u0917\u0924\u093f \u0938\u094d\u0915\u094b\u0930 (${v})`,
  reason_fin: (v)=>`\u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0932\u0947\u0928\u0926\u0947\u0928 \u0935\u093f\u0938\u0902\u0917\u0924\u093f \u092a\u093e\u0908 \u0917\u0908 (${v})`,
  reason_net: (v)=>`\u0909\u091a\u094d\u091a \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e (${v})`,
  reason_temporal: "\u0917\u0924\u093f\u0935\u093f\u0927\u093f \u090f\u0915 \u091a\u093f\u0939\u094d\u0928\u093f\u0924 \u0938\u092e\u092f \u0935\u093f\u0902\u0921\u094b \u0915\u0947 \u092a\u093e\u0938 \u0915\u0947\u0902\u0926\u094d\u0930\u093f\u0924",
  reason_location: "\u090f\u0915 \u091a\u093f\u0939\u094d\u0928\u093f\u0924 \u0938\u094d\u0925\u093e\u0928 \u0938\u0947 \u0938\u094d\u0925\u093e\u0928 \u0938\u093e\u092e\u094d\u092f",
  reason_none: "\u0915\u094b\u0908 \u092e\u091c\u092c\u0942\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u0917\u0924 \u091c\u094b\u0916\u093f\u092e \u0915\u093e\u0930\u0915 \u0928\u0939\u0940\u0902 \u2014 \u0938\u094d\u0915\u094b\u0930 \u092c\u0947\u0938\u0932\u093e\u0907\u0928 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u094d\u0925\u093f\u0924\u093f \u092a\u0930 \u0906\u0927\u093e\u0930\u093f\u0924",
  persons_of_interest_suffix: "\u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0935\u094d\u092f\u0915\u094d\u0924\u093f",
  aliases_prefix: "\u0909\u092a\u0928\u093e\u092e:", no_aliases: "\u0915\u094b\u0908 \u0909\u092a\u0928\u093e\u092e \u0926\u0930\u094d\u091c \u0928\u0939\u0940\u0902",
  risk_high: "\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u093f\u092e", risk_medium: "\u092e\u0927\u094d\u092f\u092e \u091c\u094b\u0916\u093f\u092e", risk_low: "\u0928\u093f\u092e\u094d\u0928 \u091c\u094b\u0916\u093f\u092e", risk_unrated: "\u0905\u0930\u0947\u091f\u0947\u0921 \u091c\u094b\u0916\u093f\u092e",
  breadcrumb_profiles: "\u0907\u0915\u093e\u0908 \u092a\u094d\u0930\u094b\u092b़\u093e\u0907\u0932",
  pd_alias_label: "\u0909\u092a\u0928\u093e\u092e:", pd_last_known_label: "\u0905\u0902\u0924\u093f\u092e \u091c\u094d\u091e\u093e\u0924:",
  pd_flag_btn: "\u091c\u093e\u0902\u091a \u0939\u0947\u0924\u0941 \u091a\u093f\u0939\u094d\u0928\u093f\u0924 \u0915\u0930\u0947\u0902", pd_flag_btn_done: "\u0938\u092e\u0940\u0915\u094d\u0937\u093e \u0939\u0947\u0924\u0941 \u091a\u093f\u0939\u094d\u0928\u093f\u0924",
  pd_briefing_title: "\u091c\u093e\u0902\u091a \u092c\u094d\u0930\u0940\u092b़\u093f\u0902\u0917", pd_computed_tag: "\u0917\u0923\u093f\u0924",
  pd_briefing_auto: (name, reasons)=>`\u0938\u094d\u0935\u091a\u093e\u0932\u093f\u0924 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0938\u0947 \u092a\u0924\u093e \u091a\u0932\u0924\u093e \u0939\u0948 \u0915\u093f \u003cb\u003e${name}\u003c/b\u003e \u092e\u0947\u0902 ${reasons} \u0926\u093f\u0916\u0924\u093e \u0939\u0948\u0964 \u092f\u0939 \u090f\u0915 \u0917\u0923\u093f\u0924 \u003cb\u003e\u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915\u003c/b\u003e \u0939\u0948, \u0924\u0925\u094d\u092f \u0915\u093e \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937 \u0928\u0939\u0940\u0902 \u2014 \u092f\u0939 \u0915\u0947\u0935\u0932 \u090f\u0915 \u090f\u0938\u093e \u092a\u0948\u091f\u0930\u094d\u0928 \u0926\u0930\u094d\u0936\u093e\u0924\u093e \u0939\u0948 \u091c\u093f\u0938 \u092a\u0930 \u091c\u093e\u0902\u091a\u0915\u0930\u094d\u0924\u093e \u0915\u094b \u0927\u094d\u092f\u093e\u0928 \u0926\u0947\u0928\u093e \u091a\u093e\u0939\u093f\u090f\u0964`,
  pd_briefing_baseline: "\u0915\u093f\u0938\u0940 \u092e\u091c\u092c\u0942\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u0917\u0924 \u091c\u094b\u0916\u093f\u092e \u0915\u093e\u0930\u0915 \u0915\u0947 \u092c\u093f\u0928\u093e \u090f\u0915 \u0906\u0927\u093e\u0930\u092d\u0942\u0924 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u094d\u0925\u093f\u0924\u093f",
  pd_briefing_none: (name)=>`\u003cb\u003e${name}\u003c/b\u003e \u0915\u0947 \u0932\u093f\u090f \u0915\u094b\u0908 \u0917\u0923\u093f\u0924 \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 \u0926\u0930\u094d\u091c \u092a\u0930 \u0928\u0939\u0940\u0902 \u0939\u0948\u0902\u0964 \u092f\u0939 \u0907\u0915\u093e\u0908 \u0915\u0947\u0935\u0932 \u0905\u092a\u0928\u0947 \u0926\u0930\u094d\u091c \u0938\u0902\u092c\u0902\u0927\u094b\u0902 \u0915\u0947 \u092e\u093e\u0927\u094d\u092f\u092e \u0938\u0947 \u0917\u094d\u0930\u093e\u092b़ \u092e\u0947\u0902 \u0926\u093f\u0916\u0924\u0940 \u0939\u0948\u0964`,
  pd_risk_score_label: "\u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 \u0938\u094d\u0915\u094b\u0930", pd_source_mult_label: "\u0932\u093e\u0917\u0942 \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e \u0917\u0941\u0923\u0915",
  pd_confidence_label: "\u0905\u0902\u0924\u0930\u094d\u0928\u093f\u0939\u093f\u0924 \u0907\u0915\u093e\u0908 \u0938\u092e\u093e\u0927\u093e\u0928 \u092e\u0947\u0902 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e",
  pd_alias_corrob: (n)=>`${n} \u0939\u0932 \u0915\u093f\u090f \u0917\u090f \u0909\u092a\u0928\u093e\u092e \u0909\u0932\u094d\u0932\u0947\u0916(\u094b\u0902) \u0926\u094d\u0935\u093e\u0930\u093e \u092a\u0941\u0937\u094d\u091f`,
  pd_no_alias_corrob: "\u0915\u094b\u0908 \u0909\u092a\u0928\u093e\u092e \u092a\u0941\u0937\u094d\u091f\u093f \u0926\u0930\u094d\u091c \u0928\u0939\u0940\u0902",
  pd_degree_centrality: "\u0921\u093f\u0917\u094d\u0930\u0940 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e", pd_betweenness: "\u092c\u093f\u091f\u0935\u0940\u0928\u0928\u0947\u0938", pd_connections: "\u0938\u0902\u092c\u0902\u0927",
  pd_verify_note: "\u092e\u093e\u0928\u0935 \u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0906\u0935\u0936\u094d\u092f\u0915 \u2014 \u092f\u0939 \u0906\u0930\u094b\u092a \u0928\u0939\u0940\u0902 \u0939\u0948",
  pd_connection_matrix_title: "\u0915\u0928\u0947\u0915\u094d\u0936\u0928 \u092e\u0948\u091f\u094d\u0930\u093f\u0915\u094d\u0938", pd_open_explorer: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930 \u092e\u0947\u0902 \u0916\u094b\u0932\u0947\u0902 \u2192",
  pd_identifiers_title: "\u092a\u0939\u091a\u093e\u0928\u0915\u0930\u094d\u0924\u093e", pd_entity_id: "\u0907\u0915\u093e\u0908 \u0906\u0908\u0921\u0940", pd_primary_affiliation: "\u092e\u0941\u0916\u094d\u092f \u0938\u0902\u092c\u0926\u094d\u0927\u0924\u093e",
  pd_known_aliases: "\u091c\u094d\u091e\u093e\u0924 \u0909\u092a\u0928\u093e\u092e", pd_risk_assessment: "\u091c\u094b\u0916\u093f\u092e \u092e\u0942\u0932\u094d\u092f\u093e\u0902\u0915\u0928",
  pd_timeline_title: "\u092a\u0930\u093f\u091a\u093e\u0932\u0928 \u0938\u092e\u092f\u0930\u0947\u0916\u093e", pd_no_timeline: "\u0907\u0938 \u0907\u0915\u093e\u0908 \u0915\u0947 \u0932\u093f\u090f \u0915\u094b\u0908 \u0926\u0930\u094d\u091c \u0938\u094d\u0925\u093e\u0928 \u092f\u093e\u0924\u094d\u0930\u093e \u0928\u0939\u0940\u0902\u0964",
  pd_date_unrecorded: "\u0924\u093f\u0925\u093f \u0905\u0902\u0915\u093f\u0924 \u0928\u0939\u0940\u0902", pd_graph_unavailable: "\u0917\u094d\u0930\u093e\u092b़ \u0909\u092a\u0932\u092c\u094d\u0927 \u0928\u0939\u0940\u0902",
  dl_extraction_model: "\u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937\u0923 \u092e\u0949\u0921\u0932", dl_model_option: "\u0930\u0942\u0932-\u0906\u0927\u093e\u0930\u093f\u0924 NER v1 (regex + gazetteer)",
  dl_merge_threshold: "\u0935\u093f\u0932\u092f \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e \u0938\u0940\u092e\u093e", dl_active_classes: "\u0938\u0915\u094d\u0930\u093f\u092f \u0907\u0915\u093e\u0908 \u0935\u0930\u094d\u0917",
  dl_conflicts_title: "\u0921\u0947\u091f\u093e \u0935\u093f\u0930\u094b\u0927", dl_auto_merge: "\u0911\u091f\u094b-\u0935\u093f\u0932\u092f \u0938\u0941\u091d\u093e\u0935", dl_needs_review: "\u092e\u0948\u0928\u0941\u0905\u0932 \u0938\u092e\u0940\u0915\u094d\u0937\u093e \u091c\u0930\u0942\u0930\u0940",
  dl_source_prefix: "\u0938\u094d\u0930\u094b\u0924:", btn_accept: "\u0938\u094d\u0935\u0940\u0915\u093e\u0930 \u0915\u0930\u0947\u0902", btn_accept_done: "\u2713 \u0938\u094d\u0935\u0940\u0915\u0943\u0924", btn_edit: "\u0938\u0902\u092a\u093e\u0926\u093f\u0924 \u0915\u0930\u0947\u0902",
  alert_edit_msg: "\u092e\u0948\u0928\u0941\u0905\u0932 \u0938\u0941\u0927\u093e\u0930 \u0935\u0930\u094d\u0915\u092b़\u094d\u0932\u094b: \u090f\u0915 \u091c\u093e\u0902\u091a\u0915\u0930\u094d\u0924\u093e \u092f\u0939\u093e\u0902 \u0907\u0938 \u092e\u093f\u0932\u093e\u0928 \u0915\u094b \u0938\u092e\u093e\u092f\u094b\u091c\u093f\u0924 \u092f\u093e \u0905\u0938\u094d\u0935\u0940\u0915\u093e\u0930 \u0915\u0930\u0947\u0917\u093e\u0964 \u092f\u0939 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u092e\u0947\u0902 \u0938\u0915\u094d\u0930\u093f\u092f \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
  mode_sample: "\u0928\u092e\u0942\u0928\u093e \u0926\u0938\u094d\u0924\u093e\u0935\u0947\u095b़", mode_custom: "\u0905\u092a\u0928\u093e \u091f\u0947\u0915\u094d\u0938\u094d\u091f \u092a\u0947\u0938\u094d\u091f \u0915\u0930\u0947\u0902", mode_upload: "\u0938\u094d\u0930\u094b\u0924 \u092b़\u093e\u0907\u0932 \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u0947\u0902",
  upload_title: "\u0938\u094d\u0930\u094b\u0924 \u092b़\u093e\u0907\u0932 \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u0947\u0902", upload_sub: "\u0921\u094d\u0930\u0948\u0917 \u090f\u0902\u0921 \u0921\u094d\u0930\u0949\u092a \u0915\u0930\u0947\u0902 \u092f\u093e \u092c\u094d\u0930\u093e\u0909\u095b़ \u0915\u0930\u0947\u0902 \u2014 \u0907\u0938 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u092e\u0947\u0902 \u0915\u0947\u0935\u0932 \u092a\u094d\u0932\u0947\u0928 \u091f\u0947\u0915\u094d\u0938\u094d\u091f (.txt) \u092b़\u093e\u0907\u0932\u0947\u0902",
  upload_loaded: (name, kb)=>`\u0932\u094b\u0921 \u0915\u093f\u092f\u093e \u0917\u092f\u093e: ${name} (${kb} KB)`,
  upload_txt_only: "\u092f\u0939 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u0915\u0947\u0935\u0932 \u092a\u094d\u0932\u0947\u0928 .txt \u092b़\u093e\u0907\u0932\u0947\u0902 \u092a\u095c\u0925\u0924\u093e \u0939\u0948 \u2014 PDF/DOCX \u092a\u093e\u0930\u094d\u0938\u093f\u0902\u0917 \u0939\u0947\u0924\u0941 \u092a\u094d\u0930\u094b\u0921\u0915\u094d\u0936\u0928 OCR \u092a\u093e\u0907\u092a\u0932\u093e\u0907\u0928 \u091a\u093e\u0939\u093f\u090f (backend/ \u0926\u0947\u0916\u0947\u0902)\u0964",
  upload_read_error: "\u092f\u0939 \u092b़\u093e\u0907\u0932 \u092a\u095c\u0940 \u0928\u0939\u0940\u0902 \u091c\u093e \u0938\u0915\u0940\u0964",
  textarea_placeholder: "FIR \u0905\u0902\u0936, \u0928\u093f\u0917\u0930\u093e\u0928\u0940 \u0928\u094b\u091f \u092f\u093e \u092e\u0941\u0916\u092c\u093f\u0930 \u0930\u093f\u092a\u094b\u0930\u094d\u091f \u091f\u093e\u0907\u092a \u092f\u093e \u092a\u0947\u0938\u094d\u091f \u0915\u0930\u0947\u0902\u2026",
  btn_run_extraction: "\u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937\u0923 \u091a\u0932\u093e\u090f\u0902", btn_example1: "\u0909\u0926\u093e\u0939\u0930\u0923 1 \u0932\u094b\u0921 \u0915\u0930\u0947\u0902", btn_example2: "\u0909\u0926\u093e\u0939\u0930\u0923 2 \u0932\u094b\u0921 \u0915\u0930\u0947\u0902",
  extraction_result_title: "\u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937\u0923 \u092a\u0930\u093f\u0923\u093e\u092e", no_entities_detected: "\u0915\u094b\u0908 \u0938\u0902\u0930\u091a\u093f\u0924 \u0907\u0915\u093e\u0908 \u0928\u0939\u0940\u0902 \u092e\u093f\u0932\u0940", no_text_entered: "(\u0915\u094b\u0908 \u091f\u0947\u0915\u094d\u0938\u094d\u091f \u0926\u0930\u094d\u091c \u0928\u0939\u0940\u0902)",
  source_reliability_label: "\u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e",
  risk_indicator_label: "\u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915",
  tb_assistant: "\u090f\u0906\u0908 \u091c\u093e\u0902\u091a \u0938\u0939\u093e\u092f\u0915",
  badge_evidence_cited: "\u0915\u0947\u0935\u0932 \u0938\u093e\u0915\u094d\u0937\u094d\u092f-\u0909\u0926\u094d\u0927\u0943\u0924 \u0909\u0924\u094d\u0924\u0930",
  asst_placeholder: "\u0915\u093f\u0938\u0940 \u0907\u0915\u093e\u0908, \u0938\u0902\u092c\u0902\u0927, \u092f\u093e \u092e\u093e\u092e\u0932\u0947 \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902 \u092a\u0942\u091b\u0947\u0902\u2026",
  asst_send: "\u092a\u0942\u091b\u0947\u0902",
  asst_welcome: "\u092e\u0948\u0902 \u0915\u0947\u0935\u0932 \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b\u093c \u092e\u0947\u0902 \u092e\u094c\u091c\u0942\u0926 \u0938\u093e\u0915\u094d\u0937\u094d\u092f \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u0930\u0915\u0947 \u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u0915\u0947 \u092c\u093e\u0930\u0947 \u092e\u0947\u0902 \u0938\u0935\u093e\u0932\u094b\u0902 \u0915\u0947 \u091c\u0935\u093e\u092c \u0926\u0947 \u0938\u0915\u0924\u093e \u0939\u0942\u0902 \u2014 \u0939\u0930 \u0909\u0924\u094d\u0924\u0930 \u0909\u0926\u094d\u0927\u0943\u0924 \u0939\u0948\u0964 \u0928\u0940\u091a\u0947 \u090f\u0915 \u092a\u094d\u0930\u0936\u094d\u0928 \u0906\u091c\u093c\u092e\u093e\u090f\u0902, \u092f\u093e \u0905\u092a\u0928\u093e \u0916\u0941\u0926 \u091f\u093e\u0907\u092a \u0915\u0930\u0947\u0902\u0964",
  asst_you: "\u0906\u092a",
  asst_evidence_label: "\u0938\u093e\u0915\u094d\u0937\u094d\u092f",
  asst_confidence_label: "\u0935\u093f\u0936\u094d\u0935\u0938\u0928\u0940\u092f\u0924\u093e",
  asst_source_label: "\u0938\u094d\u0930\u094b\u0924",
  asst_verify_note: "\u26a0 \u092e\u093e\u0928\u0935 \u0938\u0924\u094d\u092f\u093e\u092a\u0928 \u0906\u0935\u0936\u094d\u092f\u0915 \u2014 \u092f\u0939 \u0924\u0925\u094d\u092f \u0915\u093e \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
  asst_graph_verified: "\u0917\u094d\u0930\u093e\u092b\u093c-\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u0938\u0902\u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915 \u0938\u0902\u092c\u0902\u0927\u0964",
  asst_no_entity_found: "\u092e\u0948\u0902 \u0907\u0938\u0947 \u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u0915\u0940 \u0915\u093f\u0938\u0940 \u091c\u094d\u091e\u093e\u0924 \u0907\u0915\u093e\u0908 \u0938\u0947 \u092e\u0947\u0932 \u0928\u0939\u0940\u0902 \u0916\u093f\u0932\u093e \u0938\u0915\u093e\u0964 \u092a\u0942\u0930\u093e \u092f\u093e \u0906\u0902\u0936\u093f\u0915 \u0928\u093e\u092e \u0906\u091c\u093c\u092e\u093e\u090f\u0902, \u091c\u0948\u0938\u0947 \"Rajeev\" \u092f\u093e \"Shree Trading\"\u0964",
  asst_need_two_entities: "\u092e\u0941\u091d\u0947 \u0906\u092a\u0915\u0947 \u092a\u094d\u0930\u0936\u094d\u0928 \u092e\u0947\u0902 \u090f\u0915 \u0907\u0915\u093e\u0908 \u092e\u093f\u0932\u0940, \u0932\u0947\u0915\u093f\u0928 \u0938\u0902\u092c\u0902\u0927 \u092a\u094d\u0930\u0936\u094d\u0928\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u0926\u094b \u091a\u093e\u0939\u093f\u090f\u0964 \u0906\u091c\u093c\u092e\u093e\u090f\u0902: \"Who connects Rajeev Malhotra and Anita Rao?\"",
  asst_path_intro: (a,b)=>`<b>${a}</b> \u0914\u0930 <b>${b}</b> \u0915\u0947 \u092c\u0940\u091a \u0938\u092c\u0938\u0947 \u091b\u094b\u091f\u093e \u0915\u0928\u0947\u0915\u094d\u0936\u0928 \u092a\u0925:`,
  asst_path_none: (a,b)=>`<b>${a}</b> \u0914\u0930 <b>${b}</b> \u0915\u0947 \u092c\u0940\u091a \u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0917\u094d\u0930\u093e\u092b\u093c \u092e\u0947\u0902 \u0915\u094b\u0908 \u092a\u0925 \u0928\u0939\u0940\u0902 \u092e\u093f\u0932\u093e \u2014 \u0935\u0947 \u0905\u0938\u0902\u092c\u0902\u0927\u093f\u0924 \u0938\u092e\u0942\u0939\u094b\u0902 \u0938\u0947 \u0938\u0902\u092c\u0902\u0927\u093f\u0924 \u092a\u094d\u0930\u0924\u0940\u0924 \u0939\u094b\u0924\u0947 \u0939\u0948\u0902, \u092f\u093e \u0915\u0947\u0935\u0932 \u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u0915\u0947 \u092c\u093e\u0939\u0930 \u0915\u0940 \u0907\u0915\u093e\u0907\u092f\u094b\u0902 \u0915\u0947 \u092e\u093e\u0927\u094d\u092f\u092e \u0938\u0947 \u091c\u0941\u0921\u093c\u0947 \u0939\u0948\u0902\u0964`,
  asst_path_hops: (n)=>`${n} \u0939\u0949\u092a(\u094d\u0938)`,
  asst_why_intro: (name, score)=>`<b>${name}</b> \u0915\u093e \u0917\u0923\u0928\u093e \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 \u0938\u094d\u0915\u094b\u0930 <b>${score}/100</b> \u0939\u0948\u0964 \u092f\u0939 \u0926\u0930\u094d\u0936\u093e\u0924\u093e \u0939\u0948:`,
  asst_why_none: (name)=>`<b>${name}</b> \u0915\u0947 \u0932\u093f\u090f \u0915\u094b\u0908 \u0917\u0923\u0928\u093e \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 \u0926\u0930\u094d\u091c \u0928\u0939\u0940\u0902 \u0939\u0948 \u2014 \u0907\u0938 \u0907\u0915\u093e\u0908 \u0915\u0947 \u0932\u093f\u090f \u0915\u094b\u0908 \u0905\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u092a\u0948\u091f\u0930\u094d\u0928 \u0928\u0939\u0940\u0902 \u092a\u093e\u092f\u093e \u0917\u092f\u093e\u0964`,
  asst_connections_intro: (name, n)=>`<b>${name}</b> \u0915\u0947 <b>${n}</b> \u0926\u0930\u094d\u091c \u0938\u0902\u092c\u0902\u0927 \u0939\u0948\u0902:`,
  asst_connections_none: (name)=>`<b>${name}</b> \u0915\u0947 \u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0917\u094d\u0930\u093e\u092b\u093c \u092e\u0947\u0902 \u0915\u094b\u0908 \u0926\u0930\u094d\u091c \u0938\u0902\u092c\u0902\u0927 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964`,
  asst_top_priority_intro: "\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e (\u0921\u093f\u0917\u094d\u0930\u0940 + \u092c\u093f\u091f\u0935\u0940\u0928\u0928\u0947\u0938 + \u092a\u0947\u091c\u0930\u0948\u0902\u0915) \u0915\u0947 \u0905\u0928\u0941\u0938\u093e\u0930 \u0936\u0940\u0930\u094d\u0937 \u091c\u093e\u0902\u091a-\u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0907\u0915\u093e\u0907\u092f\u093e\u0902:",
  asst_summary_intro: "\u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b\u093c \u0938\u0947 \u0938\u0940\u0927\u0947 \u0917\u0923\u0928\u093e \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u092e\u093e\u092e\u0932\u093e \u0938\u093e\u0930\u093e\u0902\u0936:",
  asst_summary_entities: (n)=>`${n} \u0907\u0915\u093e\u0907\u092f\u093e\u0902`,
  asst_summary_edges: (n)=>`${n} \u0938\u0902\u092c\u0902\u0927`,
  asst_summary_communities: (n)=>`${n} \u092a\u093e\u090f \u0917\u090f \u0938\u092e\u0941\u0926\u093e\u092f`,
  asst_summary_highrisk: (n)=>`${n} \u0909\u091a\u094d\u091a-\u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915`,
  asst_summary_suspicious: (n)=>`${n} \u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0932\u093f\u0902\u0915`,
  asst_financial_intro: "\u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u092e\u0947\u0902 \u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923:",
  asst_financial_none: "\u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u092e\u0947\u0902 \u0915\u094b\u0908 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923 \u0926\u0930\u094d\u091c \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
  asst_suspicious_intro: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u092e\u0947\u0902 \u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u092e\u0947\u0902 \u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u092f\u093e \u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0932\u093f\u0902\u0915:",
  asst_suspicious_none: "\u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u092e\u0947\u0902 \u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u092e\u0947\u0902 \u0915\u094b\u0908 \u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0932\u093f\u0902\u0915 \u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0928\u0939\u0940\u0902 \u0939\u0948\u0964",
  asst_entity_profile_intro: (name, type)=>`<b>${name}</b> (${type}):`,
  asst_fallback: "\u092e\u0941\u091d\u0947 \u0905\u092d\u0940 \u0907\u0938\u0915\u093e \u0909\u0924\u094d\u0924\u0930 \u0926\u0947\u0928\u093e \u0928\u0939\u0940\u0902 \u0906\u0924\u093e\u0964 \u092e\u0948\u0902 \u0907\u0938 \u0924\u0930\u0939 \u0915\u0947 \u092a\u094d\u0930\u0936\u094d\u0928\u094b\u0902 \u092e\u0947\u0902 \u092e\u0926\u0926 \u0915\u0930 \u0938\u0915\u0924\u093e \u0939\u0942\u0902:",
  asst_amount_label: "\u0930\u093e\u0936\u093f",
  asst_between_label: "\u0915\u0947 \u092c\u0940\u091a",
  asst_relationship_label: "\u0938\u0902\u092c\u0902\u0927",
  asst_typing: "\u0938\u094b\u091a \u0930\u0939\u093e \u0939\u0942\u0902\u2026",
  chip_who_connects: "Rajeev Malhotra \u0914\u0930 Anita Rao \u0915\u094b \u0915\u094c\u0928 \u091c\u094b\u0921\u093c\u0924\u093e \u0939\u0948?",
  chip_why_flagged: "Vikram Solanki \u0915\u094b \u0915\u094d\u092f\u094b\u0902 \u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0939\u0948?",
  chip_top_priority: "\u0936\u0940\u0930\u094d\u0937 \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e \u0907\u0915\u093e\u0907\u092f\u093e\u0902 \u0926\u093f\u0916\u093e\u090f\u0902",
  chip_summarize: "\u0907\u0938 \u092e\u093e\u092e\u0932\u0947 \u0915\u093e \u0938\u093e\u0930\u093e\u0902\u0936 \u0926\u0947\u0902",
  chip_suspicious: "\u0938\u0902\u0926\u093f\u0917\u094d\u0927 \u0932\u093f\u0902\u0915 \u0926\u093f\u0916\u093e\u090f\u0902",
  chip_financial: "\u091a\u093f\u0928\u094d\u0939\u093f\u0924 \u0935\u093f\u0924\u094d\u0924\u0940\u092f \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923 \u0926\u093f\u0916\u093e\u090f\u0902",
},
mr: {
  gov_strip: "\u0936\u093e\u0938\u0915\u0940\u092f \u0915\u093e\u092f\u062f\u0947\u0936\u0940\u0930-\u0905\u0902\u092e\u0932\u092c\u091c\u093e\u0935\u0923\u0940 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u094d\u092f \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a",
  gov_strip_synthetic: "\u0915\u0947\u0935\u0933 \u0915\u0943\u0924\u094d\u0930\u093f\u092e \u092a\u094d\u0930\u093e\u0924\u094d\u092f\u0915\u094d\u0937\u093f\u0915 \u0921\u0947\u091f\u093e",
  gov_strip_verify: "\u0938\u0930\u094d\u0935 \u0906\u0909\u091f\u092a\u0941\u091f\u0938\u093e\u0920\u0940 \u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915",
  land_nav_1: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\u093e\u0924\u094d\u092e\u0915 \u0915\u094d\u0937\u092e\u0924\u093e", land_nav_2: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u092a\u094d\u0930\u0935\u0947\u0936 \u092a\u094d\u0930\u094b\u091f\u094b\u0915\u0949\u0932", land_nav_3: "\u0936\u093e\u0938\u0915\u0940\u092f \u0905\u0938\u094d\u0935\u0940\u0915\u0943\u0924\u0940",
  hero_title: "\u0938\u0902\u092c\u0902\u0927\u093e\u091a\u093e \u0927\u093e\u0917\u093e",
  hero_subtitle: "\u0917\u0941\u0928\u094d\u0939\u094d\u092f\u093e\u091a\u094d\u092f\u093e \u0905\u0926\u0943\u0936\u094d\u092f \u0928\u0947\u091f\u0935\u0930\u094d\u0915\u091a\u093e \u0936\u094b\u0927. \u0918\u091f\u0915 \u0928\u093f\u0930\u093e\u0915\u0930\u0923, \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0906\u0923\u093f \u092a\u0941\u0930\u093e\u0935\u094d\u092f\u093e\u0927\u093e\u0930\u093f\u0924 \u0924\u092a\u093e\u0938 \u0938\u0942\u0924\u094d\u0930\u093e\u0902\u0938\u093e\u0920\u0940 \u090f\u0915\u0924\u094d\u0930\u093f\u0924 \u0924\u092a\u093e\u0938 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u094d\u092f \u092a\u094d\u0932\u0945\u091f\u092b\u0949\u0930\u094d\u092e \u2014 \u0938\u0902\u0938\u094d\u0925\u093e\u0924\u094d\u092e\u0915 \u091c\u092c\u093e\u092c\u0926\u0947\u0939\u0940\u0938\u093e\u0920\u0940 \u092c\u0928\u0935\u0932\u0947\u0932\u0947, \u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924 \u0906\u0930\u094b\u092a\u093e\u0938\u093e\u0920\u0940 \u0928\u0935\u094d\u0939\u0947.",
  btn_request_access: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930\u0938\u093e\u0920\u0940 \u0935\u093f\u0928\u0902\u0924\u0940 \u0915\u0930\u093e \u2192",
  btn_view_briefing: "\u092c\u094d\u0930\u0940\u092b\u093f\u0902\u0917 \u092a\u0939\u093e",
  caps_title: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\u093e\u0924\u094d\u092e\u0915 \u0915\u094d\u0937\u092e\u0924\u093e", caps_subtitle: "\u092a\u094d\u0930\u0917\u0924 \u0924\u092a\u093e\u0938 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u094d\u092f\u093e\u0938\u093e\u0920\u0940 \u092e\u0942\u0932\u092d\u0942\u0924 \u092e\u0949\u0921\u094d\u092f\u0942\u0932\u094d\u0938.",
  cap1_title: "\u0921\u0947\u091f\u093e \u090f\u0915\u0940\u0915\u0930\u0923", cap1_desc: "FIR, CDR, \u0906\u0930\u094d\u0925\u093f\u0915 \u0928\u094b\u0902\u0926\u0940 \u0906\u0923\u093f \u0918\u092a\u0932\u093e \u0905\u0939\u0935\u093e\u0932 \u090f\u0915\u093e \u0938\u0902\u0930\u091a\u093f\u0924 \u0924\u092a\u093e\u0938 \u091c\u093e\u0917\u0947\u0924 \u090f\u0915\u0924\u094d\u0930\u093f\u0924 \u0915\u0930\u093e.",
  cap2_title: "\u0918\u091f\u0915 \u0909\u0924\u093e\u0930\u093e \u0906\u0923\u093f \u0928\u093f\u0930\u093e\u0915\u0930\u0923", cap2_desc: "\u0935\u094d\u092f\u0915\u094d\u0924\u0940, \u092b\u094b\u0928, \u0935\u093e\u0939\u0928\u0947 \u0906\u0923\u093f \u0938\u0902\u0938\u094d\u0925\u093e \u092f\u093e\u0902\u091a\u0940 \u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924 \u0913\u0933\u0916 \u2014 \u0921\u0941\u092a\u094d\u0932\u093f\u0915\u0947\u091f \u0909\u0932\u094d\u0932\u0947\u0916\u093e\u0902\u091a\u094d\u092f\u093e \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e-\u0917\u0941\u0923 \u0935\u093f\u0932\u0940\u0928\u0940\u0915\u0930\u0923\u093e\u0938\u0939.",
  cap3_title: "\u0938\u0902\u092c\u0902\u0927 \u092e\u0945\u092a\u093f\u0902\u0917", cap3_desc: "\u0917\u0941\u092a\u094d\u0924 \u0928\u0947\u091f\u0935\u0930\u094d\u0915\u091a\u0947 \u0926\u0943\u0936\u094d\u092f\u0940\u0915\u0930\u0923. \u0906\u0930\u094d\u0925\u093f\u0915 \u092a\u094d\u0930\u0935\u093e\u0939, \u0938\u0902\u0935\u093e\u0926 \u0926\u0941\u0935\u093e \u0906\u0923\u093f \u0936\u094d\u0930\u0947\u0923\u0940\u092c\u0926\u094d\u0927 \u0930\u091a\u0928\u093e \u0917\u0924\u093f\u0936\u0940\u0932\u092a\u0923\u0947 \u091f\u094d\u0930\u0947\u0938 \u0915\u0930\u093e.",
  cap3_module: "\u092e\u0941\u0916\u094d\u092f \u092e\u0949\u0921\u094d\u092f\u0942\u0932", cap3_visual: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0917\u094d\u0930\u093e\u092b \u0926\u0943\u0936\u094d\u092f\u0940\u0915\u0930\u0923",
  cap4_title: "\u0938\u094d\u092a\u0937\u094d\u091f\u0940\u0915\u0930\u0923\u0940\u092f \u091c\u094b\u0916\u0940\u092e \u0917\u0941\u0923\u093e\u0902\u0915\u0928", cap4_desc: "\u092a\u093e\u0930\u0926\u0930\u094d\u0936\u0915, \u0938\u094d\u0930\u094b\u0924-\u0935\u091c\u0928\u093e\u0902\u0915\u093f\u0924 \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 \u2014 \u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0917\u0941\u0923 \u092a\u0942\u0930\u094d\u0923\u092a\u0923\u0947 \u092a\u0941\u0930\u093e\u0935\u094d\u092f\u093e\u0936\u0940 \u091c\u094b\u0921\u0932\u0947\u0932\u093e, \u0928\u0947\u0939\u092e\u0940 \u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915. \u0915\u0927\u0940\u0939\u0940 \u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924 \u0906\u0930\u094b\u092a \u0928\u093e\u0939\u0940.",
  btn_view_docs: "\u0926\u0938\u094d\u0924\u090f\u0935\u091c \u092a\u0939\u093e",
  footer_copyright: "\u00a9 2026 \u0938\u0942\u0924\u094d\u0930 \u0924\u092a\u093e\u0938 \u092c\u0941\u0926\u094d\u0927\u0940\u092e\u0924\u094d\u0924\u093e \u092a\u094d\u0932\u0945\u091f\u092b\u0949\u0930\u094d\u092e. \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u2014 \u0915\u0947\u0935\u0933 \u092a\u094d\u0930\u093e\u0924\u094d\u092f\u0915\u094d\u0937\u093f\u0915\u093e\u0938\u093e\u0920\u0940.",
  footer_link1: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924 \u092a\u094d\u0930\u0935\u0947\u0936 \u092a\u094d\u0930\u094b\u091f\u094b\u0915\u0949\u0932", footer_link2: "\u0917\u094b\u092a\u0928\u0940\u092f\u0924\u093e \u0927\u094b\u0930\u0923", footer_link3: "\u0936\u093e\u0938\u0915\u0940\u092f \u0905\u0938\u094d\u0935\u0940\u0915\u0943\u0924\u0940", footer_link4: "\u092a\u094d\u0930\u0936\u093e\u0938\u0915\u093e\u0936\u0940 \u0938\u0902\u092a\u0930\u094d\u0915 \u0938\u093e\u0927\u093e",
  stamp_demo: "\u0921\u0947\u092e\u094b \u00b7 \u0915\u0943\u0924\u094d\u0930\u093f\u092e \u0921\u0947\u091f\u093e",
  brand_tagline: "\u0907\u0902\u091f\u0947\u0932\u093f\u091c\u0928\u094d\u0938 \u092a\u094d\u0932\u0945\u091f\u092b\u0949\u0930\u094d\u092e",
  nav_landing: "← मुख्यपृष्ठ / माहिती",
  nav_command: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930", nav_graph: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930", nav_profiles: "\u0918\u091f\u0915 \u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932",
  nav_datalab: "\u0921\u0947\u091f\u093e \u0932\u0945\u092c", nav_report: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0905\u0939\u0935\u093e\u0932", nav_assistant: "\u090f\u0906\u092f \u0938\u0939\u093e\u092f\u094d\u092f\u0915", nav_settings: "\u0938\u0947\u091f\u093f\u0902\u0917\u094d\u091c", nav_security: "\u0938\u0941\u0930\u0915\u094d\u0937\u093e",
  sidebar_gov_note: "\u0936\u093e\u0938\u0915\u0940\u092f \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a\n\u0915\u0947\u0935\u0933 \u0915\u0943\u0924\u094d\u0930\u093f\u092e \u0921\u0947\u091f\u093e",
  meta_entities: "\u0928\u094b\u0921\u094d\u0938", meta_links: "\u0926\u0941\u0935\u0947",
  case_id_label: "\u092a\u094d\u0930\u0915\u0930\u0923 \u0906\u092f\u0921\u0940", entities_resolved_label: "\u0928\u093f\u0930\u093e\u0915\u0930\u0923 \u0915\u0947\u0932\u0947\u0932\u0947 \u0918\u091f\u0915", engine_status_label: "\u0907\u0902\u091c\u093f\u0928 \u0938\u094d\u0925\u093f\u0924\u0940", live_data: "\u0932\u093e\u0907\u0935\u094d\u200d\u0939\u0947\u0930 \u0921\u0947\u091f\u093e",
  tb_command: "\u0915\u092e\u093e\u0902\u0921 \u0938\u0947\u0902\u091f\u0930", badge_secure: "\u0915\u0928\u0947\u0915\u094d\u0936\u0928 \u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924",
  tb_graph: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930", badge_secure_short: "\u0938\u0941\u0930\u0915\u094d\u0937\u093f\u0924", active_graph: "\u0938\u0915\u094d\u0930\u093f\u092f \u0917\u094d\u0930\u093e\u092b: \u0911\u092a\u0930\u0947\u0936\u0928 \u0915\u0947\u0938 MH/CID/2026/0417",
  tb_profiles: "\u0918\u091f\u0915 \u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932", persons_of_interest: "\u0938\u0902\u0936\u092f\u093f\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u0940",
  tb_datalab: "\u0921\u0947\u091f\u093e \u0932\u0945\u092c \u0935\u0930\u094d\u0915\u0938\u094d\u092a\u0947\u0938", badge_doc_analysis: "\u0926\u0938\u094d\u0924\u090f\u0935\u091c \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923",
  tb_report: "\u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0905\u0939\u0935\u093e\u0932", badge_tagged: "\u0935\u0938\u094d\u0924\u0941\u0938\u094d\u0925\u093f\u0924\u0940 / \u0905\u0928\u0941\u092e\u093e\u0928 / \u0938\u0942\u091a\u0928\u093e \u091f\u0945\u0917",
  stat_live: "\u0932\u093e\u0907\u0935\u094d\u200d\u0939\u0947\u0930", stat_flagged: "\u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924", stat_detected: "\u0906\u0922\u0933\u0932\u0947", stat_monitored: "\u0926\u0947\u0916\u0930\u0947\u0916\u0940\u0916\u093e\u0932\u0940",
  stat_entities_resolved: "\u0928\u093f\u0930\u093e\u0915\u0930\u0923 \u0915\u0947\u0932\u0947\u0932\u0947 \u0918\u091f\u0915", stat_high_priority: "\u0909\u091a\u094d\u091a-\u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915",
  stat_communities: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u092e\u0941\u0926\u093e\u092f", stat_suspicious_links: "\u0938\u0902\u0936\u092f\u093f\u0924 \u0926\u0941\u0935\u0947",
  feed_title: "\u0932\u093e\u0907\u0935\u094d\u200d\u0939\u0947\u0930 \u0924\u092a\u093e\u0938 \u092b\u0940\u0921", source_prefix: "\u0938\u094d\u0930\u094b\u0924:",
  feed_sev_critical: "\u0917\u0902\u092d\u0940\u0930", feed_sev_warning: "\u0907\u0936\u093e\u0930\u093e", feed_sev_info: "\u092e\u093e\u0939\u093f\u0924\u0940",
  feed_msg_1: (a,b)=>`\u0938\u0902\u0935\u093e\u0926 \u0935\u093e\u0922 \u0906\u0922\u0933\u0932\u0940: ${a} \u2194 ${b} \u2014 48 \u0924\u093e\u0938\u093e\u0902\u092e\u0927\u094d\u092f\u0947 27 \u0915\u0949\u0932`,
  feed_msg_2: (n)=>`${n} \u0918\u091f\u0915 \u0909\u0932\u094d\u0932\u0947\u0916 \u092a\u0921\u0924\u093e\u0933\u0923\u0940\u0938\u093e\u0920\u0940 \u0906\u0935\u0936\u094d\u092f\u0915 \u2014 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e \u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924-\u0935\u093f\u0932\u0940\u0928\u0940\u0915\u0930\u0923 \u092e\u0930\u094d\u092f\u093e\u0926\u0947\u092a\u0947\u0915\u094d\u0937\u093e \u0915\u092e\u0940`,
  feed_msg_3: (n,e)=>`\u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b \u092a\u0941\u0928\u094d\u0939\u093e \u0924\u092f\u093e\u0930: ${n} \u0918\u091f\u0915, ${e} \u0938\u0902\u092c\u0902\u0927 \u0938\u092e\u093e\u0935\u093f\u0937\u094d\u091f`,
  feed_msg_4: "\u092e\u094b\u0920\u093e \u0906\u0930\u094d\u0925\u093f\u0915 \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923 \u0935\u093f\u0938\u0902\u0917\u0924\u0940 \u092e\u0930\u094d\u092f\u093e\u0926\u0947\u092a\u0947\u0915\u094d\u0937\u093e \u091c\u093e\u0938\u094d\u0924 \u2014 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0905\u0939\u0935\u093e\u0932 \u092a\u0939\u093e",
  feed_src_1: "CDR \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u093f\u0928", feed_src_2: "\u0918\u091f\u0915 \u0928\u093f\u0930\u093e\u0915\u0930\u0923 \u0907\u0902\u091c\u093f\u0928", feed_src_3: "\u0917\u094d\u0930\u093e\u092b \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u093f\u0928", feed_src_4: "\u091c\u094b\u0916\u0940\u092e \u0917\u0941\u0923\u093e\u0902\u0915\u0928 \u0907\u0902\u091c\u093f\u0928",
  feed_time_1: "\u0906\u0924\u094d\u0924\u093e", feed_time_2: "5 \u092e\u093f\u0928\u093f\u091f\u093e\u0902\u092a\u0942\u0930\u094d\u0935\u0940", feed_time_3: "12 \u092e\u093f\u0928\u093f\u091f\u093e\u0902\u092a\u0942\u0930\u094d\u0935\u0940", feed_time_4: "18 \u092e\u093f\u0928\u093f\u091f\u093e\u0902\u092a\u0942\u0930\u094d\u0935\u0940",
  communities_title: "\u0906\u0922\u0933\u0932\u0947\u0932\u0947 \u0938\u092e\u0941\u0926\u093e\u092f",
  investigator_query: "\u0924\u092a\u093e\u0938 \u0905\u0927\u093f\u0915\u093e\u0930\u0940 \u0936\u094b\u0927", search_placeholder: "\u0935\u094d\u092f\u0915\u094d\u0924\u0940, \u092b\u094b\u0928, \u0920\u093f\u0915\u093e\u0923 \u0936\u094b\u0927\u093e\u2026",
  ingested_sources: "\u0938\u092e\u093e\u0935\u093f\u0937\u094d\u091f \u0938\u094d\u0930\u094b\u0924", entity_layers: "\u0918\u091f\u0915 \u0925\u0930",
  about_graph_title: "\u092f\u093e \u0917\u094d\u0930\u093e\u092b\u092c\u0926\u094d\u0926\u0932",
  about_graph_text: "\u092f\u0947\u0925\u0940\u0932 \u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0928\u094b\u0921, \u090f\u091c \u0906\u0923\u093f \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e \u092e\u0942\u0932\u094d\u092f \u0916\u0930\u094d\u092f\u093e Python \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923 \u0907\u0902\u091c\u093f\u0928\u0926\u094d\u0935\u093e\u0930\u0947 \u0917\u0923\u0932\u0947 \u0917\u0947\u0932\u0947 \u0906\u0939\u0947 \u2014 \u0939\u093e\u0930\u094d\u0921\u0915\u094b\u0921 \u0928\u0935\u094d\u0939\u0947.",
  reset_view: "\u0930\u0940\u0938\u0947\u091f \u0935\u094d\u200d\u092f\u0942",
  graph_hint: "\u0938\u094d\u0925\u093e\u0928\u093e\u0902\u0924\u0930\u093f\u0924 \u0915\u0930\u0923\u094d\u092f\u093e\u0938\u093e\u0920\u0940 \u0913\u0922\u093e \u00b7 \u095e\u0942\u092e\u0938\u093e\u0920\u0940 \u0938\u094d\u0915\u094d\u0930\u0949\u0932 \u0915\u0930\u093e \u00b7 \u0924\u092a\u093e\u0938\u093e\u0938\u093e\u0920\u0940 \u0928\u094b\u0921\u0935\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u093e",
  graph_error_title: "\u26a0 \u0917\u094d\u0930\u093e\u092b \u0930\u0947\u0902\u0921\u0930\u093f\u0902\u0917 \u0938\u0941\u0930\u0942 \u0939\u094b\u090a \u0936\u0915\u0932\u0947 \u0928\u093e\u0939\u0940.",
  graph_error_sub: "\u0907\u0924\u0930 \u092a\u0947\u091c\u0947\u0938 \u092a\u094d\u0930\u092d\u093e\u0935\u093f\u0924 \u0939\u094b\u0924 \u0928\u093e\u0939\u0940\u0924.",
  empty_select_node: "\u0924\u092a\u093e\u0938\u0940 \u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932, \u091c\u094b\u0916\u0940\u092e \u0917\u0941\u0923\n\u0906\u0923\u093f \u0938\u0902\u092c\u0902\u0927\u093f\u0924 \u0918\u091f\u0915 \u092a\u093e\u0939\u0923\u094d\u092f\u093e\u0938\u093e\u0920\u0940 \u0917\u094d\u0930\u093e\u092b\u0935\u0930\u0940\u0932 \u090f\u0916\u093e\u0926\u094d\u092f\u093e \u0928\u094b\u0921\u0935\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u093e",
  priority_entities_title: "\u0924\u092a\u093e\u0938-\u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f \u0918\u091f\u0915", priority_entities_sub: "(\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e)",
  type_persons: "\u0935\u094d\u092f\u0915\u094d\u0924\u0940", type_phones: "\u092b\u094b\u0928 \u0928\u0902\u092c\u0930", type_locations: "\u0920\u093f\u0915\u093e\u0923\u0947",
  type_vehicles: "\u0935\u093e\u0939\u0928\u0947", type_orgs: "\u0938\u0902\u0938\u094d\u0925\u093e", type_accounts: "\u092c\u0945\u0902\u0915 \u0916\u093e\u0924\u0940",
  traced_entity: "\u0936\u094b\u0927\u0932\u0947\u0932\u0947 \u0918\u091f\u0915", network_centrality: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e", degree_centrality: "\u0921\u093f\u0917\u094d\u0930\u0940 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e",
  key_attributes: "\u092e\u0941\u0916\u094d\u092f \u0917\u0941\u0923\u0927\u0930\u094d\u092e", connections: "\u0938\u0902\u092c\u0902\u0927", aliases: "\u0909\u092a\u0928\u093e\u0935\u0947",
  none_on_record: "\u0928\u094b\u0902\u0926 \u0928\u093e\u0939\u0940", last_known_location: "\u0936\u0947\u0935\u091f\u091a\u0947 \u0938\u094d\u0925\u0933", unrecorded: "\u0928\u094b\u0902\u0926 \u0928\u093e\u0939\u0940",
  why_score: "\u0939\u093e \u0917\u0941\u0923 \u0915\u093e", source_reliability_mult: "\u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e \u0917\u0941\u0923\u0915",
  human_verify_short: "\u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915",
  traced_connections: "\u0936\u094b\u0927\u0932\u0947\u0932\u0947 \u0938\u0902\u092c\u0902\u0927",
  reason_comm: (v)=>`\u0909\u091a\u094d\u091a \u0938\u0902\u0935\u093e\u0926 \u0935\u093f\u0938\u0902\u0917\u0924\u0940 \u0917\u0941\u0923 (${v})`,
  reason_fin: (v)=>`\u0906\u0930\u094d\u0925\u093f\u0915 \u0935\u094d\u092f\u0935\u0939\u093e\u0930 \u0935\u093f\u0938\u0902\u0917\u0924\u0940 \u0906\u0922\u0933\u0932\u0940 (${v})`,
  reason_net: (v)=>`\u0909\u091a\u094d\u091a \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e (${v})`,
  reason_temporal: "\u090f\u0916\u093e\u0926\u094d\u092f\u093e \u091a\u093f\u0939\u094d\u0928\u093e\u0902\u0915\u093f\u0924 \u0915\u093e\u0933\u0916\u0902\u0921\u093e\u091c\u0935\u0933 \u0915\u094d\u0930\u093f\u092f\u093e\u0915\u0932\u093e\u092a \u090f\u0915\u0924\u094d\u0930\u093f\u0924",
  reason_location: "\u091a\u093f\u0939\u094d\u0928\u093e\u0902\u0915\u093f\u0924 \u0920\u093f\u0915\u093e\u0923\u093e\u0936\u0940 \u0920\u093f\u0915\u093e\u0923 \u0938\u093e\u092e\u094d\u092f",
  reason_none: "\u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u092e\u091c\u092c\u0942\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u0917\u0924 \u091c\u094b\u0916\u0940\u092e \u0918\u091f\u0915 \u0928\u093e\u0939\u0940\u0924 \u2014 \u0917\u0941\u0923 \u092e\u0942\u0932\u092d\u0942\u0924 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u094d\u0925\u093f\u0924\u0940\u0935\u0930 \u0906\u0927\u093e\u0930\u093f\u0924",
  persons_of_interest_suffix: "\u0938\u0902\u0936\u092f\u093f\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u0940",
  aliases_prefix: "\u0909\u092a\u0928\u093e\u0935\u0947:", no_aliases: "\u0909\u092a\u0928\u093e\u0935\u0947 \u0928\u094b\u0902\u0926\u0935\u0932\u0947\u0932\u0940 \u0928\u093e\u0939\u0940\u0924",
  risk_high: "\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u0940\u092e", risk_medium: "\u092e\u0927\u094d\u092f\u092e \u091c\u094b\u0916\u0940\u092e", risk_low: "\u0915\u092e\u0940 \u091c\u094b\u0916\u0940\u092e", risk_unrated: "\u0905\u0928\u0921\u0947\u091f\u0947\u0921 \u091c\u094b\u0916\u0940\u092e",
  breadcrumb_profiles: "\u0918\u091f\u0915 \u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932",
  pd_alias_label: "\u0909\u092a\u0928\u093e\u0935:", pd_last_known_label: "\u0936\u0947\u0935\u091f\u091a\u0947 \u0938\u094d\u0925\u0933:",
  pd_flag_btn: "\u0924\u092a\u093e\u0938\u093e\u0938\u093e\u0920\u0940 \u091a\u093f\u0939\u094d\u0928\u093e\u0902\u0915\u093f\u0924 \u0915\u0930\u093e", pd_flag_btn_done: "\u092a\u0941\u0928\u0930\u093e\u0935\u0932\u094b\u0915\u0928\u093e\u0938\u093e\u0920\u0940 \u091a\u093f\u0939\u094d\u0928\u093e\u0902\u0915\u093f\u0924",
  pd_briefing_title: "\u0924\u092a\u093e\u0938 \u092c\u094d\u0930\u0940\u092b\u093f\u0902\u0917", pd_computed_tag: "\u0917\u0923\u0932\u0947\u0932\u0947",
  pd_briefing_auto: (name, reasons)=>`\u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924 \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u0923\u093e\u0928\u0941\u0938\u093e\u0930 \u003cb\u003e${name}\u003c/b\u003e \u092e\u0927\u094d\u092f\u0947 ${reasons} \u0926\u093f\u0938\u0942\u0928 \u092f\u0947\u0924\u0947. \u0939\u0947 \u090f\u0915 \u0917\u0923\u0932\u0947\u0932\u0947 \u003cb\u003e\u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915\u003c/b\u003e \u0906\u0939\u0947, \u0935\u0938\u094d\u0924\u0941\u0938\u094d\u0925\u093f\u0924\u0940 \u0928\u0935\u094d\u0939\u0947 \u2014 \u0939\u0947 \u092b\u0915\u094d\u0924 \u0924\u092a\u093e\u0938 \u0905\u0927\u093f\u0915\u093e\u0930\u094d\u092f\u093e\u0928\u0947 \u0932\u0915\u094d\u0937 \u0926\u0947\u0923\u094d\u092f\u093e\u091c\u094b\u0917\u094d\u092f\u093e \u092a\u0945\u091f\u0930\u094d\u0928\u0938\u093e\u0920\u0940 \u0906\u0939\u0947.`,
  pd_briefing_baseline: "\u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u092e\u091c\u092c\u0942\u0924 \u0935\u094d\u092f\u0915\u094d\u0924\u093f\u0917\u0924 \u091c\u094b\u0916\u0940\u092e \u0918\u091f\u0915\u093e\u0902\u0936\u093f\u0935\u093e\u092f \u092e\u0942\u0932\u092d\u0942\u0924 \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u094d\u0925\u093f\u0924\u093f",
  pd_briefing_none: (name)=>`\u003cb\u003e${name}\u003c/b\u003e \u0938\u093e\u0920\u0940 \u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u0917\u0923\u0932\u0947\u0932\u0947 \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 \u0928\u094b\u0902\u0926\u0940\u0935\u0930 \u0928\u093e\u0939\u0940\u0924. \u0939\u0947 \u0918\u091f\u0915 \u092b\u0915\u094d\u0924 \u0924\u094d\u092f\u093e\u091a\u094d\u092f\u093e \u0928\u094b\u0902\u0926\u0935\u0932\u0947\u0932\u094d\u092f\u093e \u0938\u0902\u092c\u0902\u0927\u093e\u0902\u092e\u0941\u0933\u0947 \u0917\u094d\u0930\u093e\u092b\u092e\u0927\u094d\u092f\u0947 \u0926\u093f\u0938\u0924\u0947.`,
  pd_risk_score_label: "\u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 \u0917\u0941\u0923", pd_source_mult_label: "\u0932\u093e\u0917\u0942 \u0915\u0947\u0932\u0947\u0932\u093e \u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e \u0917\u0941\u0923\u0915",
  pd_confidence_label: "\u0918\u091f\u0915 \u0928\u093f\u0930\u093e\u0915\u0930\u0923\u093e\u0924\u0940\u0932 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e",
  pd_alias_corrob: (n)=>`${n} \u0928\u093f\u0930\u093e\u0915\u0930\u0923 \u0915\u0947\u0932\u0947\u0932\u094d\u092f\u093e \u0909\u092a\u0928\u093e\u0935 \u0909\u0932\u094d\u0932\u0947\u0916\u093e\u0902\u0938\u0939 \u092a\u0941\u0937\u094d\u091f\u0940\u0915\u0943\u0924`,
  pd_no_alias_corrob: "\u0909\u092a\u0928\u093e\u0935 \u092a\u0941\u0937\u094d\u091f\u0940\u0915\u0930\u0923 \u0928\u094b\u0902\u0926 \u0928\u093e\u0939\u0940",
  pd_degree_centrality: "\u0921\u093f\u0917\u094d\u0930\u0940 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u093e", pd_betweenness: "\u092c\u093f\u091f\u0935\u0940\u0928\u0928\u0947\u0938", pd_connections: "\u0938\u0902\u092c\u0902\u0927",
  pd_verify_note: "\u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915 \u2014 \u0939\u093e \u0906\u0930\u094b\u092a \u0928\u0935\u094d\u0939\u0947",
  pd_connection_matrix_title: "\u0915\u0928\u0947\u0915\u094d\u0936\u0928 \u092e\u0945\u091f\u094d\u0930\u093f\u0915\u094d\u0938", pd_open_explorer: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u090f\u0915\u094d\u0938\u094d\u092a\u094d\u0932\u094b\u0930\u0930\u092e\u0927\u094d\u092f\u0947 \u0909\u0918\u0921\u093e \u2192",
  pd_identifiers_title: "\u0913\u0933\u0916 \u0924\u092a\u0936\u0940\u0932", pd_entity_id: "\u0918\u091f\u0915 \u0906\u092f\u0921\u0940", pd_primary_affiliation: "\u092e\u0941\u0916\u094d\u092f \u0938\u0902\u0932\u0917\u094d\u0928\u0924\u093e",
  pd_known_aliases: "\u091c\u094d\u091e\u093e\u0924 \u0909\u092a\u0928\u093e\u0935", pd_risk_assessment: "\u091c\u094b\u0916\u0940\u092e \u092e\u0942\u0932\u094d\u092f\u092e\u093e\u092a\u0928",
  pd_timeline_title: "\u0915\u093e\u0930\u094d\u092f\u093e\u0928\u094d\u0935\u092f\u0928 \u0915\u093e\u0932\u0930\u0947\u0937\u093e", pd_no_timeline: "\u092f\u093e \u0918\u091f\u0915\u093e\u0938\u093e\u0920\u0940 \u0938\u094d\u0925\u0933 \u092d\u0947\u091f\u0940\u091a\u0940 \u0928\u094b\u0902\u0926 \u0928\u093e\u0939\u0940.",
  pd_date_unrecorded: "\u0924\u093e\u0930\u0940\u0916 \u0928\u094b\u0902\u0926 \u0928\u093e\u0939\u0940", pd_graph_unavailable: "\u0917\u094d\u0930\u093e\u092b \u0909\u092a\u0932\u092c\u094d\u0927 \u0928\u093e\u0939\u0940",
  dl_extraction_model: "\u0909\u0924\u093e\u0930\u093e \u092e\u0949\u0921\u0947\u0932", dl_model_option: "\u0928\u093f\u092f\u092e-\u0906\u0927\u093e\u0930\u093f\u0924 NER v1 (regex + gazetteer)",
  dl_merge_threshold: "\u0935\u093f\u0932\u0940\u0928\u0940\u0915\u0930\u0923 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e \u092e\u0930\u094d\u092f\u093e\u0926\u093e", dl_active_classes: "\u0938\u0915\u094d\u0930\u093f\u092f \u0918\u091f\u0915 \u0935\u0930\u094d\u0917",
  dl_conflicts_title: "\u0921\u0947\u091f\u093e \u0938\u0902\u0918\u0930\u094d\u0937", dl_auto_merge: "\u0938\u094d\u0935\u092f\u0902\u091a\u0932\u093f\u0924-\u0935\u093f\u0932\u0940\u0928\u0940\u0915\u0930\u0923 \u0938\u0941\u091a\u0935\u0932\u0947", dl_needs_review: "\u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915",
  dl_source_prefix: "\u0938\u094d\u0930\u094b\u0924:", btn_accept: "\u0938\u094d\u0935\u0940\u0915\u093e\u0930\u093e", btn_accept_done: "\u2713 \u0938\u094d\u0935\u0940\u0915\u093e\u0930\u0932\u0947", btn_edit: "\u0938\u0902\u092a\u093e\u0926\u093f\u0924 \u0915\u0930\u093e",
  alert_edit_msg: "\u092e\u093e\u0928\u0935\u0940 \u0926\u0941\u0930\u0941\u0938\u094d\u0924\u0940\u0915\u0930\u0923 \u0915\u093e\u0930\u094d\u092f\u092a\u094d\u0930\u0935\u093e\u0939: \u090f\u0915 \u0924\u092a\u093e\u0938 \u0905\u0927\u093f\u0915\u093e\u0930\u0940 \u092f\u0947\u0925\u0947 \u0939\u093e \u091c\u0941\u0933\u0923\u0940 \u0938\u092e\u093e\u092f\u094b\u091c\u093f\u0924 \u0915\u093f\u0902\u0935\u093e \u0928\u093e\u0915\u093e\u0930\u0947\u0932. \u0939\u0947 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a\u092e\u0927\u094d\u092f\u0947 \u0938\u0915\u094d\u0930\u093f\u092f \u0928\u093e\u0939\u0940.",
  mode_sample: "\u0928\u092e\u0942\u0928\u093e \u0926\u0938\u094d\u0924\u090f\u0935\u091c", mode_custom: "\u0938\u094d\u0935\u0924\u0903\u091a\u093e \u092e\u091c\u0915\u0942\u0930 \u091f\u093e\u0907\u092a \u0915\u0930\u093e", mode_upload: "\u0938\u094d\u0930\u094b\u0924 \u095e\u093e\u0907\u0932 \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u093e",
  upload_title: "\u0938\u094d\u0930\u094b\u0924 \u095e\u093e\u0907\u0932 \u0905\u092a\u0932\u094b\u0921 \u0915\u0930\u093e", upload_sub: "\u0921\u094d\u0930\u0945\u0917 \u0905\u0945\u0902\u0921 \u0921\u094d\u0930\u0949\u092a \u0915\u0930\u093e \u0915\u093f\u0902\u0935\u093e \u092c\u094d\u0930\u093e\u0909\u095b \u0915\u0930\u093e \u2014 \u092f\u093e \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a\u092e\u0927\u094d\u092f\u0947 \u092b\u0915\u094d\u0924 \u0938\u093e\u0927\u0940 \u092e\u091c\u0915\u0942\u0930 (.txt) \u095e\u093e\u0907\u0932\u094d\u0938",
  upload_loaded: (name, kb)=>`\u0932\u094b\u0921 \u0915\u0947\u0932\u0947: ${name} (${kb} KB)`,
  upload_txt_only: "\u0939\u0947 \u092a\u094d\u0930\u094b\u091f\u094b\u091f\u093e\u0907\u092a \u092b\u0915\u094d\u0924 \u0938\u093e\u0927\u0940 .txt \u095e\u093e\u0907\u0932\u094d\u0938 \u0935\u093e\u091a\u0924\u0947 \u2014 PDF/DOCX \u092a\u093e\u0930\u094d\u0938\u093f\u0902\u0917\u0938\u093e\u0920\u0940 \u092a\u094d\u0930\u094b\u0921\u0915\u094d\u0936\u0928 OCR \u092a\u093e\u0907\u092a\u0932\u093e\u0907\u0928 \u0906\u0935\u0936\u094d\u092f\u0915 (backend/ \u092a\u0939\u093e).",
  upload_read_error: "\u0939\u0940 \u095e\u093e\u0907\u0932 \u0935\u093e\u091a\u0924\u093e \u0906\u0932\u0940 \u0928\u093e\u0939\u0940.",
  textarea_placeholder: "FIR \u0909\u0924\u093e\u0930\u093e, \u0918\u092a\u0932\u093e \u091f\u0940\u092a \u0915\u093f\u0902\u0935\u093e \u092e\u093e\u0939\u093f\u0924\u0940\u0926\u093e\u0930 \u0905\u0939\u0935\u093e\u0932 \u091f\u093e\u0907\u092a \u0915\u093f\u0902\u0935\u093e \u092a\u0947\u0938\u094d\u091f \u0915\u0930\u093e\u2026",
  btn_run_extraction: "\u0909\u0924\u093e\u0930\u093e \u091a\u093e\u0932\u0935\u093e", btn_example1: "\u0909\u0926\u093e\u0939\u0930\u0923 1 \u0932\u094b\u0921 \u0915\u0930\u093e", btn_example2: "\u0909\u0926\u093e\u0939\u0930\u0923 2 \u0932\u094b\u0921 \u0915\u0930\u093e",
  extraction_result_title: "\u0909\u0924\u093e\u0930\u093e \u0928\u093f\u0915\u093e\u0932", no_entities_detected: "\u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u0938\u0902\u0930\u091a\u093f\u0924 \u0918\u091f\u0915 \u0906\u0922\u0933\u0932\u0947 \u0928\u093e\u0939\u0940\u0924", no_text_entered: "(\u0915\u094b\u0923\u0924\u093e\u0939\u0940 \u092e\u091c\u0915\u0942\u0930 \u0928\u093e\u0939\u0940)",
  source_reliability_label: "\u0938\u094d\u0930\u094b\u0924 \u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e",
  risk_indicator_label: "\u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915",
  tb_assistant: "\u090f\u0906\u092f \u0924\u092a\u093e\u0938 \u0938\u0939\u093e\u092f\u094d\u092f\u0915",
  badge_evidence_cited: "\u0915\u0947\u0935\u0933 \u092a\u0941\u0930\u093e\u0935\u094d\u092f\u093e\u0935\u0930 \u0906\u0927\u093e\u0930\u093f\u0924 \u0909\u0924\u094d\u0924\u0930\u0947",
  asst_placeholder: "\u090f\u0916\u093e\u0926\u094d\u092f\u093e \u0918\u091f\u0915\u093e\u092c\u0926\u094d\u0926\u0932, \u0938\u0902\u092c\u0902\u0927\u093e\u092c\u0926\u094d\u0926\u0932 \u0915\u093f\u0902\u0935\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u092c\u0926\u094d\u0926\u0932 \u0935\u093f\u091a\u093e\u0930\u093e\u2026",
  asst_send: "\u0935\u093f\u091a\u093e\u0930\u093e",
  asst_welcome: "\u092e\u0940 \u092b\u0915\u094d\u0924 \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b\u092e\u0927\u0940\u0932 \u092a\u0941\u0930\u093e\u0935\u094d\u092f\u093e\u091a\u093e \u0935\u093e\u092a\u0930 \u0915\u0930\u0942\u0928 \u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u092c\u0926\u094d\u0926\u0932\u091a\u094d\u092f\u093e \u092a\u094d\u0930\u0936\u094d\u0928\u093e\u0902\u091a\u0940 \u0909\u0924\u094d\u0924\u0930\u0947 \u0926\u0947\u090a \u0936\u0915\u0924\u094b \u2014 \u092a\u094d\u0930\u0924\u094d\u092f\u0947\u0915 \u0909\u0924\u094d\u0924\u0930 \u0909\u0926\u094d\u0927\u0943\u0924 \u0906\u0939\u0947. \u0916\u093e\u0932\u0940\u0932 \u092a\u094d\u0930\u0936\u094d\u0928 \u0935\u093e\u092a\u0930\u0942\u0928 \u092a\u0939\u093e, \u0915\u093f\u0902\u0935\u093e \u0938\u094d\u0935\u0924\u0903\u091a\u093e \u091f\u093e\u0907\u092a \u0915\u0930\u093e.",
  asst_you: "\u0924\u0941\u092e\u094d\u0939\u0940",
  asst_evidence_label: "\u092a\u0941\u0930\u093e\u0935\u093e",
  asst_confidence_label: "\u0935\u093f\u0936\u094d\u0935\u093e\u0938\u093e\u0930\u094d\u0939\u0924\u093e",
  asst_source_label: "\u0938\u094d\u0930\u094b\u0924",
  asst_verify_note: "\u26a0 \u092e\u093e\u0928\u0935\u0940 \u092a\u0921\u0924\u093e\u0933\u0923\u0940 \u0906\u0935\u0936\u094d\u092f\u0915 \u2014 \u0939\u093e \u0935\u0938\u094d\u0924\u0941\u0938\u094d\u0925\u093f\u0924\u0940\u091a\u093e \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937 \u0928\u093e\u0939\u0940.",
  asst_graph_verified: "\u0917\u094d\u0930\u093e\u092b-\u0938\u0924\u094d\u092f\u093e\u092a\u093f\u0924 \u0938\u0902\u0930\u091a\u0928\u093e\u0924\u094d\u092e\u0915 \u0938\u0902\u092c\u0902\u0927.",
  asst_no_entity_found: "\u092e\u0940 \u0939\u0947 \u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u0924\u0940\u0932 \u0915\u094b\u0923\u0924\u094d\u092f\u093e\u0939\u0940 \u091c\u094d\u091e\u093e\u0924 \u0918\u091f\u0915\u093e\u0936\u0940 \u091c\u0941\u0933\u0935\u0942 \u0936\u0915\u0932\u094b \u0928\u093e\u0939\u0940. \u0938\u0902\u092a\u0942\u0930\u094d\u0923 \u0915\u093f\u0902\u0935\u093e \u0906\u0902\u0936\u093f\u0915 \u0928\u093e\u0935 \u0935\u093e\u092a\u0930\u0942\u0928 \u092a\u0939\u093e, \u091c\u0938\u0947 \u0915\u0940 \"Rajeev\" \u0915\u093f\u0902\u0935\u093e \"Shree Trading\".",
  asst_need_two_entities: "\u0924\u0941\u092e\u091a\u094d\u092f\u093e \u092a\u094d\u0930\u0936\u094d\u0928\u093e\u0924 \u092e\u0932\u093e \u090f\u0915 \u0918\u091f\u0915 \u0938\u093e\u092a\u0921\u0932\u093e, \u092a\u0923 \u0938\u0902\u092c\u0902\u0927 \u092a\u094d\u0930\u0936\u094d\u0928\u093e\u0902\u0938\u093e\u0920\u0940 \u0926\u094b\u0928 \u0906\u0935\u0936\u094d\u092f\u0915 \u0906\u0939\u0947\u0924. \u0935\u093e\u092a\u0930\u0942\u0928 \u092a\u0939\u093e: \"Who connects Rajeev Malhotra and Anita Rao?\"",
  asst_path_intro: (a,b)=>`<b>${a}</b>  \u0906\u0923\u093f  <b>${b}</b>  \u092f\u093e\u0902\u091a\u094d\u092f\u093e\u092e\u0927\u0940\u0932 \u0938\u0930\u094d\u0935\u093e\u0924 \u0915\u092e\u0940 \u091c\u094b\u0921\u0923\u0940 \u092e\u093e\u0930\u094d\u0917:`,
  asst_path_none: (a,b)=>`<b>${a}</b>  \u0906\u0923\u093f  <b>${b}</b>  \u092f\u093e\u0902\u091a\u094d\u092f\u093e\u092e\u0927\u094d\u092f\u0947 \u0938\u0927\u094d\u092f\u093e\u091a\u094d\u092f\u093e \u0917\u094d\u0930\u093e\u092b\u092e\u0927\u094d\u092f\u0947 \u0915\u094b\u0923\u0924\u093e\u0939\u0940 \u092e\u093e\u0930\u094d\u0917 \u0938\u093e\u092a\u0921\u0932\u093e \u0928\u093e\u0939\u0940 \u2014 \u0924\u0947 \u0905\u0938\u0902\u092c\u0902\u0927\u093f\u0924 \u0917\u091f\u093e\u0902\u0936\u0940 \u0938\u0902\u092c\u0902\u0927\u093f\u0924 \u0905\u0938\u0942 \u0936\u0915\u0924\u093e\u0924, \u0915\u093f\u0902\u0935\u093e \u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u092c\u093e\u0939\u0947\u0930\u0940\u0932 \u0918\u091f\u0915\u093e\u0902\u092e\u093e\u0930\u094d\u092b\u0924\u091a \u091c\u094b\u0921\u0932\u0947\u0932\u0947 \u0906\u0939\u0947\u0924.`,
  asst_path_hops: (n)=>`${n} \u091f\u092a\u094d\u092a\u0947`,
  asst_why_intro: (name, score)=>`<b>${name}</b> \u091a\u093e \u0917\u0923\u0928\u093e \u0915\u0947\u0932\u0947\u0932\u093e \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 \u0917\u0941\u0923 <b>${score}/100</b> \u0906\u0939\u0947. \u0939\u0947 \u092f\u093e\u0935\u0930\u0942\u0928 \u0926\u093f\u0938\u0924\u0947:`,
  asst_why_none: (name)=>`<b>${name}</b> \u0938\u093e\u0920\u0940 \u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u0917\u0923\u0928\u093e \u0915\u0947\u0932\u0947\u0932\u0947 \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 \u0928\u094b\u0902\u0926\u0940\u0935\u0930 \u0928\u093e\u0939\u0940\u0924 \u2014 \u092f\u093e \u0918\u091f\u0915\u093e\u0938\u093e\u0920\u0940 \u0915\u094b\u0923\u0924\u093e\u0939\u0940 \u0905\u0938\u093e\u092e\u093e\u0928\u094d\u092f \u092a\u0945\u091f\u0930\u094d\u0928 \u0906\u0922\u0933\u0932\u093e \u0928\u093e\u0939\u0940.`,
  asst_connections_intro: (name, n)=>`<b>${name}</b> \u091a\u0947 <b>${n}</b> \u0928\u094b\u0902\u0926\u0935\u0932\u0947\u0932\u0947 \u0938\u0902\u092c\u0902\u0927 \u0906\u0939\u0947\u0924:`,
  asst_connections_none: (name)=>`<b>${name}</b> \u091a\u093e \u0938\u0927\u094d\u092f\u093e\u091a\u094d\u092f\u093e \u0917\u094d\u0930\u093e\u092b\u092e\u0927\u094d\u092f\u0947 \u0915\u094b\u0923\u0924\u093e\u0939\u0940 \u0928\u094b\u0902\u0926\u0935\u0932\u0947\u0932\u093e \u0938\u0902\u092c\u0902\u0927 \u0928\u093e\u0939\u0940.`,
  asst_top_priority_intro: "\u092e\u093f\u0936\u094d\u0930\u093f\u0924 \u0915\u0947\u0902\u0926\u094d\u0930\u0940\u092f\u0924\u0947\u0928\u0941\u0938\u093e\u0930 (\u0921\u093f\u0917\u094d\u0930\u0940 + \u092c\u093f\u091f\u0935\u0940\u0928\u0928\u0947\u0938 + \u092a\u0947\u091c\u0930\u0901\u0915) \u0936\u0940\u0930\u094d\u0937 \u0924\u092a\u093e\u0938-\u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f \u0918\u091f\u0915:",
  asst_summary_intro: "\u0938\u0927\u094d\u092f\u093e\u091a\u094d\u092f\u093e \u0928\u0949\u0932\u0947\u091c \u0917\u094d\u0930\u093e\u092b\u0935\u0930\u0942\u0928 \u0925\u0947\u091f \u0924\u092f\u093e\u0930 \u0915\u0947\u0932\u0947\u0932\u093e \u092a\u094d\u0930\u0915\u0930\u0923 \u0938\u093e\u0930\u093e\u0902\u0936:",
  asst_summary_entities: (n)=>`${n} \u0918\u091f\u0915`,
  asst_summary_edges: (n)=>`${n} \u0938\u0902\u092c\u0902\u0927`,
  asst_summary_communities: (n)=>`${n} \u0906\u0922\u0933\u0932\u0947\u0932\u0947 \u0938\u092e\u0941\u0926\u093e\u092f`,
  asst_summary_highrisk: (n)=>`${n} \u0909\u091a\u094d\u091a-\u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915`,
  asst_summary_suspicious: (n)=>`${n} \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0938\u0902\u0936\u092f\u093f\u0924 \u0926\u0941\u0935\u0947`,
  asst_financial_intro: "\u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u0924\u0940\u0932 \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0906\u0930\u094d\u0925\u093f\u0915 \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923\u0947:",
  asst_financial_none: "\u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u0924 \u0915\u094b\u0923\u0924\u0947\u0939\u0940 \u0906\u0930\u094d\u0925\u093f\u0915 \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923 \u0928\u094b\u0902\u0926\u0935\u0932\u0947\u0932\u0947 \u0928\u093e\u0939\u0940.",
  asst_suspicious_intro: "\u0928\u0947\u091f\u0935\u0930\u094d\u0915\u092e\u0927\u0940\u0932 \u0938\u0927\u094d\u092f\u093e\u091a\u0947 \u0938\u0902\u0936\u092f\u093f\u0924 \u0915\u093f\u0902\u0935\u093e \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0926\u0941\u0935\u0947:",
  asst_suspicious_none: "\u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u0924 \u0938\u0927\u094d\u092f\u093e \u0915\u094b\u0923\u0924\u093e\u0939\u0940 \u0938\u0902\u0936\u092f\u093f\u0924 \u0926\u0941\u0935\u093e \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0928\u093e\u0939\u0940.",
  asst_entity_profile_intro: (name, type)=>`<b>${name}</b> (${type}):`,
  asst_fallback: "\u092e\u0932\u093e \u0905\u091c\u0942\u0928 \u092f\u093e\u091a\u0947 \u0909\u0924\u094d\u0924\u0930 \u0915\u0938\u0947 \u0926\u094d\u092f\u093e\u0935\u0947 \u0939\u0947 \u092e\u093e\u0939\u0940\u0924 \u0928\u093e\u0939\u0940. \u092e\u0940 \u0905\u0936\u093e \u092a\u094d\u0930\u0936\u094d\u0928\u093e\u0902\u092e\u0927\u094d\u092f\u0947 \u092e\u0926\u0924 \u0915\u0930\u0942 \u0936\u0915\u0924\u094b:",
  asst_amount_label: "\u0930\u0915\u094d\u0915\u092e",
  asst_between_label: "\u0926\u0930\u092e\u094d\u092f\u093e\u0928",
  asst_relationship_label: "\u0938\u0902\u092c\u0902\u0927",
  asst_typing: "\u0935\u093f\u091a\u093e\u0930 \u0915\u0930\u0924 \u0906\u0939\u0947\u2026",
  chip_who_connects: "Rajeev Malhotra \u0906\u0923\u093f Anita Rao \u092f\u093e\u0902\u0928\u093e \u0915\u094b\u0923 \u091c\u094b\u0921\u0924\u0947?",
  chip_why_flagged: "Vikram Solanki \u0932\u093e \u0915\u093e \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0915\u0947\u0932\u0947 \u0906\u0939\u0947?",
  chip_top_priority: "\u0936\u0940\u0930\u094d\u0937 \u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f \u0918\u091f\u0915 \u0926\u093e\u0916\u0935\u093e",
  chip_summarize: "\u092f\u093e \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u091a\u093e \u0938\u093e\u0930\u093e\u0902\u0936 \u0926\u094d\u092f\u093e",
  chip_suspicious: "\u0938\u0902\u0936\u092f\u093f\u0924 \u0926\u0941\u0935\u0947 \u0926\u093e\u0916\u0935\u093e",
  chip_financial: "\u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924 \u0906\u0930\u094d\u0925\u093f\u0915 \u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923\u0947 \u0926\u093e\u0916\u0935\u093e",
},
};

let CURRENT_LANG = "en";
function t(key, ...args){
  const dict = I18N[CURRENT_LANG] || I18N.en;
  const entry = (key in dict) ? dict[key] : (I18N.en[key] !== undefined ? I18N.en[key] : key);
  return typeof entry === "function" ? entry(...args) : entry;
}
function applyStaticI18n(){
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const val = t(el.dataset.i18n);
    if(el.dataset.i18nAttr){ el.setAttribute(el.dataset.i18nAttr, val); }
    else { el.textContent = val; }
  });
  document.querySelectorAll("[data-i18n-html]").forEach(el=>{ el.innerHTML = t(el.dataset.i18nHtml); });
  document.documentElement.lang = CURRENT_LANG;
}

const TYPE_META = {
  person:       {labelKey:"type_persons", color:"#2554e8", icon:"person"},
  phone:        {labelKey:"type_phones", color:"#e08a00", icon:"phone"},
  location:     {labelKey:"type_locations", color:"#16a34a", icon:"pin"},
  vehicle:      {labelKey:"type_vehicles", color:"#7c3aed", icon:"vehicle"},
  organization: {labelKey:"type_orgs", color:"#0e9aa7", icon:"org"},
  account:      {labelKey:"type_accounts", color:"#db2777", icon:"account"},
};
const ICONS = {
  person: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/></svg>',
  phone: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="6" y="2" width="12" height="20" rx="2"/><line x1="10" y1="18" x2="14" y2="18"/></svg>',
  pin: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.5"/></svg>',
  vehicle: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 13l1.5-5A2 2 0 0 1 6.4 6.5h11.2A2 2 0 0 1 19.5 8l1.5 5"/><rect x="3" y="13" width="18" height="5" rx="1.5"/><circle cx="7.5" cy="18" r="1.5"/><circle cx="16.5" cy="18" r="1.5"/></svg>',
  org: '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="4" y="3" width="16" height="18"/><line x1="9" y1="8" x2="9" y2="8.01"/><line x1="15" y1="8" x2="15" y2="8.01"/><line x1="9" y1="13" x2="9" y2="13.01"/><line x1="15" y1="13" x2="15" y2="13.01"/></svg>',
  account: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="6" width="18" height="13" rx="1.5"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
};

/* ---------------- LANGUAGE SWITCHER ---------------- */
function applyLanguage(lang){
  CURRENT_LANG = lang;
  document.querySelectorAll(".lang-btn").forEach(b=> b.classList.toggle("active", b.dataset.lang===lang));
  applyStaticI18n();
  renderLegend();
  renderCommandCenter();
  renderEpGrid();
  renderChips();
  renderSampleDocs();
  renderConflicts(parseInt(document.getElementById("thresh-slider").value,10)/100);
  renderReportPage();
  if(window.__reselectCurrentNode) window.__reselectCurrentNode();
  if(CURRENT_PROFILE_ID) openProfileDetail(CURRENT_PROFILE_ID);
  if(typeof asstRenderSuggestions === "function") asstRenderSuggestions();
  if(typeof ASST_HISTORY !== "undefined" && ASST_HISTORY.length === 1 && ASST_HISTORY[0].role === "assistant"){
    ASST_HISTORY[0] = {role:"assistant", html:`<div>${t('asst_welcome')}</div>`};
    asstRenderMessages();
  }
}
document.querySelectorAll(".lang-btn").forEach(btn=>{
  btn.addEventListener("click", ()=> applyLanguage(btn.dataset.lang));
});

/* ---------------- LANDING <-> APP ---------------- */
function enterApp(){
  document.getElementById("landing").classList.remove("hide"); // reset display if any
  document.getElementById("landing").classList.add("hide");
  document.getElementById("app").classList.add("show");
}

function exitToLanding(){
  document.getElementById("app").classList.remove("show");
  document.getElementById("landing").classList.remove("hide");
  const sidebar = document.getElementById("sidebar");
  if(sidebar) sidebar.classList.remove("open");
  window.scrollTo({top: 0, behavior: "smooth"});
}

document.getElementById("btn-enter-app").addEventListener("click", enterApp);
document.getElementById("btn-view-briefing").addEventListener("click", ()=>{
  document.getElementById("briefing-section").scrollIntoView({behavior:"smooth"});
});
document.getElementById("btn-view-docs").addEventListener("click", enterApp);

const brandBtn = document.getElementById("sb-brand-btn");
if(brandBtn) brandBtn.addEventListener("click", exitToLanding);

/* ---- Animate sidebar brand name SUTRA <-> सूत्र in sync with CSS ---- */
(function(){
  const nameEl = document.getElementById("sb-brand-name");
  if(!nameEl) return;
  const EN = "S\u016aTRA";
  const HI = "\u0938\u0942\u0924\u094d\u0930";
  let showingEn = true;
  // Sync with CSS animation: switch text at the 40% point of 5s = 2000ms
  // EN visible 0-35%, fade 35-45% -> switch text at 40% = 2000ms
  // HI visible 45-80%, fade 80-90% -> switch at 85% = 4250ms
  function cycle(){
    setTimeout(()=>{
      nameEl.style.transition = "opacity 0.4s";
      nameEl.style.opacity = "0";
      setTimeout(()=>{
        showingEn = !showingEn;
        nameEl.textContent = showingEn ? EN : HI;
        if(!showingEn){
          nameEl.style.fontFamily = "'Noto Sans Devanagari','Mangal',Georgia,serif";
          nameEl.style.fontSize = "13px";
        } else {
          nameEl.style.fontFamily = "";
          nameEl.style.fontSize = "";
        }
        nameEl.style.opacity = "1";
      }, 400);
    }, showingEn ? 1750 : 1750);
  }
  // Continuous loop
  (function tick(){
    cycle();
    setTimeout(tick, 3500);
  })();
})();


const backLandingBtn = document.getElementById("btn-back-landing");
if(backLandingBtn) backLandingBtn.addEventListener("click", exitToLanding);

const mobBrandBtn = document.getElementById("mobile-brand-btn");
if(mobBrandBtn) mobBrandBtn.addEventListener("click", exitToLanding);

const topbarLandingBtn = document.getElementById("topbar-landing-btn");
if(topbarLandingBtn) topbarLandingBtn.addEventListener("click", exitToLanding);

/* ---------------- SIDEBAR NAV ---------------- */
document.querySelectorAll(".sb-item[data-page]").forEach(item=>{
  item.addEventListener("click", ()=>{
    document.querySelectorAll(".sb-item[data-page]").forEach(i=>i.classList.remove("active"));
    item.classList.add("active");
    document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
    document.querySelector(`.page[data-page="${item.dataset.page}"]`).classList.add("active");
    document.getElementById("sidebar").classList.remove("open");
  });
});
document.getElementById("btn-toggle-sidebar").addEventListener("click", ()=> document.getElementById("sidebar").classList.toggle("open"));
function goToPage(name){
  document.querySelectorAll(".sb-item[data-page]").forEach(i=>i.classList.toggle("active", i.dataset.page===name));
  document.querySelectorAll(".page").forEach(p=>p.classList.toggle("active", p.dataset.page===name));
}

/* ---------------- COMMAND CENTER ---------------- */
const personNodes = DATA.nodes.filter(n=>n.type==="person");
const suspiciousEdges = DATA.edges.filter(e=>e.suspicious);
const highRiskCount = (DATA.risk||[]).filter(r=>r.risk_indicator_score>=45).length;

function renderCommandCenter(){
  document.getElementById("stat-grid").innerHTML = `
    <div class="stat-card"><div class="tag up">${t('stat_live')}</div><div class="l">${t('stat_entities_resolved')}</div><div class="v">${DATA.nodes.length}</div></div>
    <div class="stat-card"><div class="tag">${t('stat_flagged')}</div><div class="l">${t('stat_high_priority')}</div><div class="v">${highRiskCount}</div></div>
    <div class="stat-card"><div class="tag">${t('stat_detected')}</div><div class="l">${t('stat_communities')}</div><div class="v">${DATA.communities.length}</div></div>
    <div class="stat-card"><div class="tag">${t('stat_monitored')}</div><div class="l">${t('stat_suspicious_links')}</div><div class="v">${suspiciousEdges.length}</div></div>
  `;
  document.querySelector('[data-page="command"] h2').textContent = t('tb_command');
  document.querySelector('[data-page="command"] .badge-secure').textContent = t('badge_secure');

  const topPersonEdge = suspiciousEdges.find(e=> {
    const s = DATA.nodes.find(n=>n.id===(e.source.id||e.source));
    return s && s.type==="phone";
  }) || suspiciousEdges[0];
  const srcLabel = topPersonEdge ? DATA.id_to_label[topPersonEdge.source.id||topPersonEdge.source] : "\u2014";
  const tgtLabel = topPersonEdge ? DATA.id_to_label[topPersonEdge.target.id||topPersonEdge.target] : "\u2014";
  const reviewCount = DATA.resolution.filter(r=>r.confidence<0.6 && r.confidence>=0.4).length;

  const feedItems = [
    {sev:"critical", text:t('feed_msg_1', srcLabel, tgtLabel), time:t('feed_time_1'), src:t('feed_src_1')},
    {sev:"warning", text:t('feed_msg_2', reviewCount), time:t('feed_time_2'), src:t('feed_src_2')},
    {sev:"info", text:t('feed_msg_3', DATA.nodes.length, DATA.edges.length), time:t('feed_time_3'), src:t('feed_src_3')},
    {sev:"critical", text:t('feed_msg_4'), time:t('feed_time_4'), src:t('feed_src_4')},
  ];
  document.getElementById("live-feed-list").innerHTML = feedItems.map(f=>`
    <div class="feed-item">
      <div class="feed-head"><span class="feed-sev ${f.sev}">${t('feed_sev_'+f.sev)}</span><span class="feed-time">${f.time}</span></div>
      <div class="feed-text">${f.text}</div>
      <div class="feed-src">${t('source_prefix')} ${f.src}</div>
    </div>`).join("");

  const commColors = ["#2554e8","#e08a00","#7c3aed","#16a34a","#dc2626","#0e9aa7","#db2777"];
  document.getElementById("community-list").innerHTML = DATA.priority_ranking.slice(0,6).map((id,i)=>{
    const n = DATA.nodes.find(x=>x.id===id);
    if(!n) return "";
    return `<div class="community-row"><div class="community-dot" style="background:${commColors[i%commColors.length]}"></div>
      <div class="name">${n.label}</div><div class="n">${t((TYPE_META[n.type]||TYPE_META.person).labelKey)}</div></div>`;
  }).join("");
  document.getElementById("feed-title-el").textContent = t('feed_title');
  document.getElementById("communities-title-el").textContent = t('communities_title');
}

/* ---------------- ROLE CLASSIFICATION BADGES ---------------- */
function getRoleBadge(role){
  if(!role) return "";
  const r = role.toLowerCase();
  if(r.includes("orchestrator")) return `<span class="role-badge role-orchestrator">ORCHESTRATOR</span>`;
  if(r.includes("broker") || r.includes("intermediary")) return `<span class="role-badge role-broker">STRATEGIC BROKER</span>`;
  if(r.includes("mule") || r.includes("financial")) return `<span class="role-badge role-mule">FINANCIAL CONDUIT</span>`;
  if(r.includes("communicator") || r.includes("caller")) return `<span class="role-badge role-communicator">KEY COMMUNICATOR</span>`;
  return `<span class="role-badge role-associate">NETWORK ASSOCIATE</span>`;
}

/* ---------------- ENTITY PROFILES GRID ---------------- */
function riskLevelLabel(level){
  return {HIGH:t('risk_high'), MEDIUM:t('risk_medium'), LOW:t('risk_low')}[level] || t('risk_unrated');
}
function renderEpGrid(){
  document.querySelector('[data-page="profiles"] h2').textContent = t('tb_profiles');
  document.querySelector('[data-page="profiles"] .badge-secure').textContent = personNodes.length + " " + t('persons_of_interest');
  document.getElementById("ep-grid").innerHTML = personNodes.map(n=>{
    const aliasStr = (n.aliases && n.aliases.length) ? `${t('aliases_prefix')} ${n.aliases.join(", ")}` : t('no_aliases');
    return `<div class="ep-card" data-id="${n.id}">
      <div class="ep-top"><div class="ep-avatar">${ICONS.person}</div><div><div class="name">${n.label}</div><div class="id">${n.id}</div></div></div>
      <div style="margin-bottom:8px;">${getRoleBadge(n.role)}</div>
      <div class="aliases">${aliasStr}</div>
      <div class="risk-pill ${n.risk_level||'UNRATED'}">${riskLevelLabel(n.risk_level)}</div>
    </div>`;
  }).join("");
  document.querySelectorAll(".ep-card").forEach(card=>{
    card.addEventListener("click", ()=> openProfileDetail(card.dataset.id));
  });
}

/* ---------------- NETWORK EXPLORER (D3) ---------------- */
const activeTypes = new Set(Object.keys(TYPE_META));
function renderLegend(){
  document.getElementById("legend-list").innerHTML = Object.entries(TYPE_META).map(([key,m])=>{
    const off = activeTypes.has(key) ? "" : "off";
    return `<div class="legend-row2 ${off}" data-type="${key}" style="color:${m.color}"><span>${ICONS[m.icon]}</span><span style="color:var(--ink-dim)">${t(m.labelKey)}</span></div>`;
  }).join("");
  document.querySelectorAll(".legend-row2").forEach(row=>{
    row.addEventListener("click", ()=>{
      const t2 = row.dataset.type;
      if(activeTypes.has(t2)) activeTypes.delete(t2); else activeTypes.add(t2);
      renderLegend(); if(window.__updateVisibility) window.__updateVisibility();
    });
  });
}

const topRanked = DATA.priority_ranking.slice(0,5).map(id => DATA.nodes.find(n=>n.id===id)).filter(Boolean);

function getRiskReasons(d){
  if(!d.risk) return [];
  const b = d.risk.breakdown;
  const reasons = [];
  if(b.communication_anomaly>0.4) reasons.push(t('reason_comm', b.communication_anomaly));
  if(b.financial_anomaly>0.3) reasons.push(t('reason_fin', b.financial_anomaly));
  if(b.network_centrality>0.4) reasons.push(t('reason_net', b.network_centrality));
  if(b.temporal_proximity>0.5) reasons.push(t('reason_temporal'));
  if(b.location_correlation>0.5) reasons.push(t('reason_location'));
  if(reasons.length===0) reasons.push(t('reason_none'));
  return reasons;
}

let CURRENT_SELECTED_NODE = null;
(function initGraph(){
  try {
    if (typeof d3 === "undefined") throw new Error("d3 failed to load");
    const svg = d3.select("#graph");
    const gRoot = svg.append("g");
    const gLinks = gRoot.append("g");
    const gNodes = gRoot.append("g");
    function sizeSvg(){ const wrap = document.getElementById("graph-wrap"); return {w: wrap.clientWidth||900, h: wrap.clientHeight||600}; }
    let {w,h} = sizeSvg();
    svg.attr("viewBox", `0 0 ${w} ${h}`);
    const zoom = d3.zoom().scaleExtent([0.35,3]).on("zoom", (ev)=>{ gRoot.attr("transform", ev.transform); });
    svg.call(zoom);

    const nodes = DATA.nodes.map(n=>Object.assign({}, n));
    const links = DATA.edges.map(e=>Object.assign({}, e));

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d=>d.id).distance(l=> l.suspicious?110:90).strength(0.5))
      .force("charge", d3.forceManyBody().strength(-320))
      .force("center", d3.forceCenter(w/2, h/2))
      .force("collision", d3.forceCollide().radius(26));

    function curvedPath(d){
      const dx = d.target.x - d.source.x, dy = d.target.y - d.source.y;
      const dr = Math.sqrt(dx*dx+dy*dy) * 1.5;
      return `M${d.source.x},${d.source.y} A${dr},${dr} 0 0,1 ${d.target.x},${d.target.y}`;
    }

    const link = gLinks.selectAll("path").data(links).join("path")
      .attr("class", d=> "link" + (d.suspicious? " suspicious":""))
      .attr("stroke-width", d=> d.suspicious?1.6:1);
    const linkLabel = gLinks.selectAll("text").data(links.filter(l=>l.display_label)).join("text")
      .attr("class","link-label").text(d=>d.display_label);

    const keyNodeId = DATA.priority_ranking[0];
    function boxSize(d){ const base = d.type==="person" ? 30 : 26; return d.id===keyNodeId ? base+4 : base; }

    const nodeG = gNodes.selectAll("g.node").data(nodes).join("g")
      .attr("class", d=> "node" + (d.id===keyNodeId?" key":""))
      .call(d3.drag()
        .on("start",(ev,d)=>{ if(!ev.active) simulation.alphaTarget(0.25).restart(); d.fx=d.x; d.fy=d.y; })
        .on("drag",(ev,d)=>{ d.fx=ev.x; d.fy=ev.y; })
        .on("end",(ev,d)=>{ if(!ev.active) simulation.alphaTarget(0); d.fx=null; d.fy=null; }));

    nodeG.append("rect").attr("class","node-box")
      .attr("width", d=>boxSize(d)).attr("height", d=>boxSize(d))
      .attr("x", d=> -boxSize(d)/2).attr("y", d=> -boxSize(d)/2)
      .attr("rx", 6)
      .attr("stroke", d=> (TYPE_META[d.type]||TYPE_META.person).color)
      .style("color", d=> (TYPE_META[d.type]||TYPE_META.person).color);
    nodeG.append("foreignObject")
      .attr("class","node-icon")
      .attr("width", d=>boxSize(d)).attr("height", d=>boxSize(d))
      .attr("x", d=> -boxSize(d)/2).attr("y", d=> -boxSize(d)/2)
      .append("xhtml:div")
      .style("width","100%").style("height","100%").style("display","flex")
      .style("align-items","center").style("justify-content","center")
      .style("color", d=> (TYPE_META[d.type]||TYPE_META.person).color)
      .html(d=> ICONS[(TYPE_META[d.type]||TYPE_META.person).icon]);
    nodeG.append("text").attr("class","node-label").attr("y", d=> boxSize(d)/2+13).attr("text-anchor","middle")
      .text(d=> d.label.length>18? d.label.slice(0,17)+"\u2026" : d.label);
    nodeG.filter(d=>d.type==="person").append("text").attr("class","node-sublabel").attr("y", d=> boxSize(d)/2+23).attr("text-anchor","middle")
      .text(d=> d.risk_level ? riskLevelLabel(d.risk_level) : "");
    nodeG.on("click", (ev,d)=> { ev.stopPropagation(); selectNode(d.id); });
    nodeG.append("title").text(d=> `${d.label} \u2014 degree ${d.degree}, betweenness ${d.betweenness}`);

    simulation.on("tick", ()=>{
      link.attr("d", curvedPath);
      linkLabel.attr("x",d=>(d.source.x+d.target.x)/2).attr("y",d=>(d.source.y+d.target.y)/2 - 6);
      nodeG.attr("transform", d=> `translate(${d.x},${d.y})`);
    });
    window.addEventListener("resize", ()=>{ const s=sizeSvg(); w=s.w; h=s.h; svg.attr("viewBox", `0 0 ${w} ${h}`); simulation.force("center", d3.forceCenter(w/2,h/2)); simulation.alpha(0.3).restart(); });
    document.getElementById("btn-reset").addEventListener("click", ()=> svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity));
    window.__updateVisibility = function(){ nodeG.classed("dim", d=> !activeTypes.has(d.type)); link.classed("dim", d=> !activeTypes.has(d.source.type) || !activeTypes.has(d.target.type)); };

    function selectNode(id){
      CURRENT_SELECTED_NODE = id;
      nodeG.classed("selected", d=> d.id===id);
      document.getElementById("profile-panel").classList.add("open");
      const d = nodes.find(n=>n.id===id);
      const connected = links.filter(l => l.source.id===id || l.target.id===id).map(l=>{
        const otherId = l.source.id===id ? l.target.id : l.source.id;
        const other = nodes.find(n=>n.id===otherId);
        return {other, rel:l.type, susp: !!l.suspicious, label:l.display_label};
      });
      const meta = TYPE_META[d.type]||TYPE_META.person;
      const confidencePct = Math.round(d.degree*100);

      let attrsHtml = `<div class="attr-row"><div class="k">${t('connections')}</div><div class="v">${connected.length}</div></div>`;
      if(d.type==="person"){
        attrsHtml += `<div class="attr-row"><div class="k">${t('aliases')}</div><div class="v">${(d.aliases&&d.aliases.length)?d.aliases.join(", "):t('none_on_record')}</div></div>`;
        attrsHtml += `<div class="attr-row"><div class="k">${t('last_known_location')}</div><div class="v">${d.last_known ? d.last_known.location : t('unrecorded')}</div></div>`;
      }

      let explainHtml = "";
      if(d.risk){
        const reasons = getRiskReasons(d);
        explainHtml = `
          <div class="explain-mini">
            <div class="title">\u26a0 ${t('why_score')}? (${t('risk_indicator_label')}: ${d.risk.risk_indicator_score}/100)</div>
            ${reasons.map(r=>`<div class="reason">${r}</div>`).join("")}
            <div class="reason">${t('source_reliability_mult')}: \u00d7${d.risk.breakdown.source_reliability_multiplier}</div>
            <div class="verify">\u26a0 ${t('human_verify_short')}</div>
          </div>`;
      }
      document.getElementById("profile-panel").innerHTML = `
        <div class="profile-badge">\u2713 ${t('traced_entity')}</div>
        <div class="profile-head">
          <h2>${d.label}</h2>
          <div class="type">${t(meta.labelKey)} \u00b7 ${d.id}</div>
          <div style="margin-top:6px; display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
            ${d.type==="person" ? `<div class="risk-pill ${d.risk_level||'UNRATED'}">${riskLevelLabel(d.risk_level)}</div>` : ""}
            ${d.type==="person" ? getRoleBadge(d.role) : ""}
          </div>
        </div>
        <div class="profile-section">
          <div class="st">${t('network_centrality')}</div>
          <div class="confidence-bar-wrap"><div class="confidence-bar-track"><div class="confidence-bar-fill" style="width:${confidencePct}%; background:${meta.color}"></div></div>
          <div class="confidence-label"><span>${t('degree_centrality')}</span><span>${confidencePct}%</span></div></div>
        </div>
        <div class="profile-section"><div class="st">${t('key_attributes')}</div>${attrsHtml}</div>
        ${explainHtml}
        <div class="profile-section" style="border-bottom:none;">
          <div class="st">${t('traced_connections')} (${connected.length})</div>
          ${connected.map(c=>`<div class="trace-item" data-id="${c.other.id}">
              <div class="trace-icon" style="color:${(TYPE_META[c.other.type]||TYPE_META.person).color}">${ICONS[(TYPE_META[c.other.type]||TYPE_META.person).icon]}</div>
              <div class="trace-info"><div class="n">${c.other.label}</div><div class="r ${c.susp?'susp':''}">${c.susp?'\u26a0 ':''}${(c.label||c.rel).toLowerCase()}</div></div>
            </div>`).join("")}
        </div>
      `;
      document.querySelectorAll(".trace-item").forEach(el=> el.addEventListener("click", ()=> selectNode(el.dataset.id)));
    }
    window.__selectNode = selectNode;
    window.__reselectCurrentNode = function(){ if(CURRENT_SELECTED_NODE) selectNode(CURRENT_SELECTED_NODE); };
    svg.on("click", ()=>{ CURRENT_SELECTED_NODE=null; nodeG.classed("selected", false); document.getElementById("profile-panel").innerHTML = `<div class="profile-empty" data-i18n="empty_select_node">${t('empty_select_node')}</div>`; });
    document.getElementById("search-input").addEventListener("input",(e)=>{
      const q = e.target.value.trim().toLowerCase();
      if(!q){ nodeG.classed("dim", d=>!activeTypes.has(d.type)); return; }
      nodeG.classed("dim", d=> !d.label.toLowerCase().includes(q));
    });

    initPathFinder();
    initTimelinePlayer();
  } catch (err) {
    console.error("Graph init failed:", err);
    document.getElementById("graph-error").style.display = "flex";
  }
})();

/* ---------------- PATH FINDER INTERACTION ---------------- */
function initPathFinder(){
  const srcSelect = document.getElementById("pf-source");
  const tgtSelect = document.getElementById("pf-target");
  if(!srcSelect || !tgtSelect) return;

  const personNodes = DATA.nodes.filter(n=>n.type==="person");
  const opts = personNodes.map(p=>`<option value="${p.id}">${p.label}</option>`).join("");
  srcSelect.innerHTML = opts;
  tgtSelect.innerHTML = opts;
  if(personNodes.length > 1) tgtSelect.selectedIndex = 1;

  document.getElementById("btn-find-path").addEventListener("click", ()=>{
    const sId = srcSelect.value;
    const tId = tgtSelect.value;
    if(sId === tId){
      alert("Please select two different entities to trace a connection.");
      return;
    }
    const pathKey = `${sId}_${tId}`;
    const pathKeyRev = `${tId}_${sId}`;
    const pathData = (DATA.all_paths && (DATA.all_paths[pathKey] || DATA.all_paths[pathKeyRev]));

    const badge = document.getElementById("path-info-badge");
    if(pathData && pathData.path){
      const pathNodeIds = new Set(pathData.path);
      d3.selectAll("g.node").classed("dim", d => !pathNodeIds.has(d.id));
      d3.selectAll("path.link").classed("dim", l => !(pathNodeIds.has(l.source.id||l.source) && pathNodeIds.has(l.target.id||l.target)));
      
      badge.style.display = "block";
      badge.innerHTML = `<b>Traced Connection Path (${pathData.hops} hops):</b> ${pathData.labels.join(" \u2192 ")}`;
    } else {
      badge.style.display = "block";
      badge.innerHTML = `<b>No Direct Connection:</b> No direct record between ${DATA.id_to_label[sId]} and ${DATA.id_to_label[tId]} in current graph.`;
    }
  });

  document.getElementById("btn-clear-path").addEventListener("click", ()=>{
    d3.selectAll("g.node").classed("dim", false);
    d3.selectAll("path.link").classed("dim", false);
    document.getElementById("path-info-badge").style.display = "none";
  });
}

/* ---------------- TIMELINE SEQUENCE PLAYER ---------------- */
function initTimelinePlayer(){
  const events = DATA.timeline_events || [];
  if(!events.length) return;

  const slider = document.getElementById("tp-slider");
  const dateEl = document.getElementById("tp-event-date");
  const badgeEl = document.getElementById("tp-event-badge");
  const titleEl = document.getElementById("tp-event-title");
  const tickerEl = document.getElementById("tp-ticker");
  const playBtn = document.getElementById("btn-tp-play");

  slider.max = events.length - 1;
  let curStep = 0;
  let isPlaying = false;
  let playTimer = null;

  function applyStep(idx){
    curStep = idx;
    slider.value = idx;
    const evt = events[idx];
    if(!evt) return;

    dateEl.textContent = evt.date + " " + evt.time;
    badgeEl.textContent = evt.badge || evt.type;
    badgeEl.className = "tp-event-badge " + (evt.type || "");
    titleEl.textContent = evt.title + ": " + evt.description;
    tickerEl.textContent = `Step ${idx + 1} of ${events.length}`;

    const activeNodeIds = new Set(evt.nodes || []);
    d3.selectAll("g.node").classed("selected", d => activeNodeIds.has(d.id));
    d3.selectAll("path.link").classed("suspicious", l => activeNodeIds.has(l.source.id||l.source) && activeNodeIds.has(l.target.id||l.target));
  }

  slider.addEventListener("input", (e)=> applyStep(parseInt(e.target.value, 10)));
  document.getElementById("btn-tp-prev").addEventListener("click", ()=> {
    if(curStep > 0) applyStep(curStep - 1);
  });
  document.getElementById("btn-tp-next").addEventListener("click", ()=> {
    if(curStep < events.length - 1) applyStep(curStep + 1);
  });
  document.getElementById("btn-tp-reset").addEventListener("click", ()=> {
    pause();
    applyStep(0);
    d3.selectAll("g.node").classed("selected", false);
  });

  function play(){
    isPlaying = true;
    playBtn.textContent = "⏸";
    playTimer = setInterval(()=>{
      if(curStep < events.length - 1){
        applyStep(curStep + 1);
      } else {
        pause();
      }
    }, 1800);
  }

  function pause(){
    isPlaying = false;
    playBtn.textContent = "▶";
    if(playTimer) clearInterval(playTimer);
  }

  playBtn.addEventListener("click", ()=> {
    if(isPlaying) pause(); else play();
  });

  applyStep(0);
}

/* ---------------- ENTITY PROFILE DETAIL (full page) ---------------- */
let CURRENT_PROFILE_ID = null;
function riskColor(level){
  return {HIGH:"var(--red)", MEDIUM:"var(--amber)", LOW:"var(--green)"}[level] || "var(--ink-faint)";
}

function renderMiniConnectionMatrix(containerId, personId){
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  if(typeof d3 === "undefined"){ container.innerHTML = `<div class="pd-empty" style="padding:20px;">${t('pd_graph_unavailable')}</div>`; return; }
  const neighborEdges = DATA.edges.filter(e=>{
    const s = e.source.id || e.source, tt = e.target.id || e.target;
    return s===personId || tt===personId;
  });
  const neighborIds = new Set();
  neighborEdges.forEach(e=>{
    const s = e.source.id || e.source, tt = e.target.id || e.target;
    neighborIds.add(s); neighborIds.add(tt);
  });
  const localNodes = DATA.nodes.filter(n=> neighborIds.has(n.id)).map(n=>Object.assign({}, n));
  const localLinks = neighborEdges.map(e=> ({source: e.source.id||e.source, target: e.target.id||e.target, suspicious: e.suspicious}));

  const w = container.clientWidth || 300, h = 220;
  const svg = d3.select(container).append("svg").attr("viewBox", `0 0 ${w} ${h}`);
  const g = svg.append("g");
  const sim = d3.forceSimulation(localNodes)
    .force("link", d3.forceLink(localLinks).id(d=>d.id).distance(60))
    .force("charge", d3.forceManyBody().strength(-140))
    .force("center", d3.forceCenter(w/2, h/2))
    .force("collision", d3.forceCollide().radius(22));

  const link = g.selectAll("line").data(localLinks).join("line")
    .attr("stroke", d=> d.suspicious ? "var(--red)" : "var(--border)")
    .attr("stroke-dasharray", d=> d.suspicious ? "3,3" : null)
    .attr("stroke-width", 1.4);
  const node = g.selectAll("g").data(localNodes).join("g");
  node.append("circle").attr("r", d=> d.id===personId ? 14 : 9)
    .attr("fill", d=> d.id===personId ? "var(--blue)" : "#fff")
    .attr("stroke", d=> (TYPE_META[d.type]||TYPE_META.person).color).attr("stroke-width", 2);
  node.append("text").attr("y", d=> (d.id===personId?14:9)+13).attr("text-anchor","middle")
    .attr("font-family","var(--font-mono)").attr("font-size","8px").attr("fill","var(--ink-faint)")
    .text(d=> d.label.length>14 ? d.label.slice(0,13)+"\u2026" : d.label);
  sim.on("tick", ()=>{
    link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y).attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
    node.attr("transform", d=>`translate(${d.x},${d.y})`);
  });
}

function openProfileDetail(personId){
  const d = DATA.nodes.find(n=>n.id===personId);
  if(!d) return;
  CURRENT_PROFILE_ID = personId;
  document.getElementById("pd-breadcrumb-name").textContent = d.label;
  document.querySelector(".breadcrumb a#pd-back-link").textContent = t('breadcrumb_profiles');
  const riskLevel = d.risk_level || "UNRATED";
  const connected = DATA.edges.filter(e=>{
    const s = e.source.id||e.source, tt = e.target.id||e.target;
    return s===personId || tt===personId;
  });

  let briefingHtml = "";
  let assessmentHtml = "";
  let tagsHtml = "";
  if(d.risk){
    const reasons = getRiskReasons(d);
    const reasonsText = reasons.join(", ");
    briefingHtml = `<div class="pd-briefing-text">${t('pd_briefing_auto', d.label, reasonsText)}</div>`;
    const b = d.risk.breakdown;
    const aliasCorrob = (d.aliases && d.aliases.length) ? t('pd_alias_corrob', d.aliases.length) : t('pd_no_alias_corrob');
    assessmentHtml = `<div class="pd-assessment"><b>${t('pd_risk_score_label')}: ${d.risk.risk_indicator_score}/100.</b> ${t('pd_source_mult_label')}: \u00d7${b.source_reliability_multiplier}. ${t('pd_confidence_label')}: ${aliasCorrob}.</div>`;
    tagsHtml = `<div class="pd-tag-row">
        <span class="pd-tag">${t('pd_degree_centrality')}: ${Math.round(d.degree*100)}%</span>
        <span class="pd-tag">${t('pd_betweenness')}: ${Math.round(d.betweenness*100)}%</span>
        <span class="pd-tag">${t('pd_connections')}: ${connected.length}</span>
      </div>`;
  } else {
    briefingHtml = `<div class="pd-briefing-text">${t('pd_briefing_none', d.label)}</div>`;
    tagsHtml = `<div class="pd-tag-row"><span class="pd-tag">${t('pd_connections')}: ${connected.length}</span></div>`;
  }

  const timelineHtml = (d.timeline && d.timeline.length)
    ? d.timeline.map(tl=>`
        <div class="pd-timeline-item">
          <div class="pd-timeline-dot"></div>
          <div class="pd-timeline-info">
            <div class="t">${tl.location}</div>
            <div class="d">${tl.timestamp ? new Date(tl.timestamp).toLocaleString() : t('pd_date_unrecorded')}</div>
            ${tl.notes ? `<div class="n">${tl.notes}</div>` : ""}
          </div>
        </div>`).join("")
    : `<div class="pd-empty">${t('pd_no_timeline')}</div>`;

  document.getElementById("profile-detail-content").innerHTML = `
    <div class="pd-hero">
      <div class="pd-avatar">${ICONS.person.replace('width="13" height="13"','width="30" height="30"')}</div>
      <div class="pd-hero-info">
        <h1>${d.label}</h1>
        <div class="pd-hero-meta">
          <span>${t('pd_alias_label')} ${(d.aliases && d.aliases.length) ? d.aliases.join(", ") : t('none_on_record')}</span>
          <span>\u00b7</span>
          <span>${t('pd_last_known_label')} ${d.last_known ? d.last_known.location : t('unrecorded')}</span>
        </div>
        <div style="display:flex; gap:8px; align-items:center; margin-top:8px; flex-wrap:wrap;">
          <div class="risk-pill ${riskLevel}" style="background:rgba(255,255,255,0.2); border-color:rgba(255,255,255,0.5); color:#fff;">${riskLevelLabel(riskLevel)}</div>
          ${getRoleBadge(d.role)}
        </div>
      </div>
      <button class="btn-track" id="pd-flag-btn">${t('pd_flag_btn')}</button>
    </div>

    <div class="pd-grid">
      <div>
        <div class="pd-card">
          <div class="pd-card-head"><h3>${t('pd_briefing_title')}</h3><span class="pd-live-tag">${t('pd_computed_tag')}</span></div>
          ${briefingHtml}
          ${assessmentHtml}
          ${tagsHtml}
          <div class="pd-verify-note">${t('pd_verify_note')}</div>
        </div>
        <div class="pd-card">
          <div class="pd-card-head"><h3>${t('pd_connection_matrix_title')}</h3><a href="#" id="pd-expand-graph" style="font-family:var(--font-mono); font-size:10.5px; color:var(--blue); text-decoration:none;">${t('pd_open_explorer')}</a></div>
          <div class="pd-matrix-wrap" id="pd-matrix"></div>
        </div>
      </div>
      <div>
        <div class="pd-card">
          <div class="pd-card-head"><h3>${t('pd_identifiers_title')}</h3></div>
          <div class="pd-id-row"><div class="k">${t('pd_entity_id')}</div><div class="v">${d.id}</div></div>
          <div class="pd-id-row"><div class="k">${t('pd_primary_affiliation')}</div><div class="v">${d.affiliation || t('none_on_record')}</div></div>
          <div class="pd-id-row"><div class="k">${t('pd_known_aliases')}</div><div class="v">${(d.aliases && d.aliases.length) ? d.aliases.join(", ") : t('none_on_record')}</div></div>
          <div class="pd-id-row">
            <div class="k">${t('pd_risk_assessment')}</div>
            <div class="v">${riskLevelLabel(riskLevel)} ${d.risk? '('+d.risk.risk_indicator_score+'/100)' : ''}</div>
            <div class="pd-risk-bar-track"><div class="pd-risk-bar-fill" style="width:${d.risk? d.risk.risk_indicator_score : 5}%; background:${riskColor(riskLevel)};"></div></div>
          </div>
        </div>
        <div class="pd-card">
          <div class="pd-card-head"><h3>${t('pd_timeline_title')}</h3></div>
          ${timelineHtml}
        </div>
      </div>
    </div>
  `;
  renderMiniConnectionMatrix("pd-matrix", personId);
  document.getElementById("pd-flag-btn").addEventListener("click", ()=>{
    const btn = document.getElementById("pd-flag-btn");
    btn.textContent = t('pd_flag_btn_done'); btn.disabled = true; btn.style.opacity = "0.7";
  });
  document.getElementById("pd-expand-graph").addEventListener("click", (e)=>{
    e.preventDefault(); goToPage("graph"); setTimeout(()=>{ if(window.__selectNode) window.__selectNode(personId); }, 80);
  });
  goToPage("profile-detail");
}
document.getElementById("pd-back-link").addEventListener("click", (e)=>{ e.preventDefault(); CURRENT_PROFILE_ID=null; goToPage("profiles"); });

/* ---------------- DATA LAB ---------------- */
const dlActiveTypes = new Set(["PERSON","LOCATION","PHONE","VEHICLE","ORGANIZATION","MONEY","DATE"]);
const CHIP_TYPES = ["PERSON","LOCATION","PHONE","VEHICLE","ORGANIZATION","MONEY","DATE"];
const CHIP_LABEL_KEY = {PERSON:"type_persons", LOCATION:"type_locations", PHONE:"type_phones", VEHICLE:"type_vehicles", ORGANIZATION:"type_orgs", MONEY:"dl_chip_money", DATE:"dl_chip_date"};
function chipLabel(type){
  if(type==="MONEY") return CURRENT_LANG==="hi" ? "\u0930\u093e\u0936\u093f" : (CURRENT_LANG==="mr" ? "\u0930\u0915\u094d\u0915\u092e" : "MONEY");
  if(type==="DATE") return CURRENT_LANG==="hi" ? "\u0924\u093f\u0925\u093f" : (CURRENT_LANG==="mr" ? "\u0924\u093e\u0930\u0940\u0916" : "DATE");
  return t(CHIP_LABEL_KEY[type]).toUpperCase();
}
function renderChips(){
  document.getElementById("entity-chip-row").innerHTML = CHIP_TYPES.map(ty=>
    `<div class="dl-chip ${dlActiveTypes.has(ty)?'active':''}" data-t="${ty}">${chipLabel(ty)}</div>`).join("");
  document.querySelectorAll(".dl-chip").forEach(chip=>{
    chip.addEventListener("click", ()=>{
      const ty = chip.dataset.t;
      if(dlActiveTypes.has(ty)) dlActiveTypes.delete(ty); else dlActiveTypes.add(ty);
      renderChips(); renderSampleDocs();
      if(document.getElementById("live-output").innerHTML.trim()) renderLiveResult(document.getElementById("live-input").value);
    });
  });
  document.getElementById("dl-extraction-model-label").textContent = t('dl_extraction_model');
  document.getElementById("dl-model-option").textContent = t('dl_model_option');
  document.getElementById("dl-merge-threshold-label").innerHTML = t('dl_merge_threshold') + '<span class="dl-slider-val" id="thresh-val">' + document.getElementById("thresh-slider").value + '%</span>';
  document.getElementById("dl-active-classes-label").textContent = t('dl_active_classes');
}

const ENT_CSS = {PERSON:"person", LOCATION:"location", PHONE:"phone", VEHICLE:"vehicle", ORGANIZATION:"org", MONEY:"money", DATE:"date", TIME:"date"};

function filterDocHtml(html){
  const wrapper = document.createElement("div");
  wrapper.innerHTML = html;
  wrapper.querySelectorAll(".ent-tag").forEach(tag=>{
    const cls = [...tag.classList].find(c=>c!=="ent-tag");
    const typeKey = Object.keys(ENT_CSS).find(k=>ENT_CSS[k]===cls);
    if(typeKey && !dlActiveTypes.has(typeKey)){
      tag.replaceWith(document.createTextNode(tag.textContent.replace(/[A-Z]{3}$/,"")));
    }
  });
  return wrapper.innerHTML;
}

function renderSampleDocs(){
  document.getElementById("sample-doc-mode").innerHTML = DATA.fir_docs.map(doc=>`
    <div class="dl-doc-card" style="margin-bottom:20px;">
      <div class="doctitle">${doc.case_id} \u2014 ${doc.station}</div>
      <div style="font-family:var(--font-mono); font-size:9.5px; color:#8a5600; margin-bottom:14px;">${doc.date} \u00b7 ${t('source_reliability_label')}: ${doc.reliability.toUpperCase()}</div>
      <div class="doc-text">${filterDocHtml(doc.html)}</div>
    </div>`).join("");
}

function levenshteinRatio(a, b){
  a = a.toLowerCase(); b = b.toLowerCase();
  const m = a.length, n = b.length;
  if(m===0 || n===0) return 0;
  const dp = Array.from({length:m+1}, ()=> new Array(n+1).fill(0));
  for(let i=0;i<=m;i++) dp[i][0]=i;
  for(let j=0;j<=n;j++) dp[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++)
    dp[i][j] = a[i-1]===b[j-1] ? dp[i-1][j-1] : 1+Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
  return 1 - dp[m][n] / Math.max(m,n);
}
const REGEX_PATTERNS = [
  ["PHONE", /\+?\d{2}\s?\d{2}[\u2022\d]{2,}\d{4}|\+91[\s-]?\d{5}[\u2022\d]*\d{4}/g],
  ["VEHICLE", /\b[A-Z]{2}-\d{2}\s?[A-Z]{2}\s?\d{4}\b/g],
  ["MONEY", /\u20b9\s?[\d,]+(?:\.\d+)?|Rs\.?\s?[\d,]+(?:\.\d+)?|INR\s?[\d,]+/g],
  ["DATE", /\b\d{1,2}[\/-]\d{1,2}[\/-]\d{2,4}\b/g],
  ["TIME", /\b\d{3,4}\s?hrs\b/gi],
];
const NER_FUZZY_MATCH_THRESHOLD = 0.82;
function runLiveExtraction(text){
  const found = [];
  REGEX_PATTERNS.forEach(([type, re]) => {
    const r = new RegExp(re.source, re.flags);
    let m;
    while((m = r.exec(text)) !== null){ found.push({text:m[0], type, match:"pattern"}); if(m.index===r.lastIndex) r.lastIndex++; }
  });
  const gz = DATA.gazetteer;
  ["PERSON","LOCATION","ORGANIZATION"].forEach(type=>{
    gz[type].forEach(name=>{
      const idx = text.toUpperCase().indexOf(name.toUpperCase());
      if(idx !== -1){ found.push({text:text.substr(idx, name.length), type, matched_entity:name, match:"exact"}); return; }
      const words = text.match(/[A-Z][A-Za-z.]*(?:\s+[A-Z][A-Za-z.]*){0,2}/g) || [];
      words.forEach(w=>{
        const ratio = levenshteinRatio(w, name);
        if(ratio >= NER_FUZZY_MATCH_THRESHOLD) found.push({text:w, type, matched_entity:name, match:`fuzzy (${ratio.toFixed(2)})`});
      });
    });
  });
  const seen = new Set(); const unique = [];
  found.forEach(f=>{ const k=f.text+"|"+f.type; if(!seen.has(k)){ seen.add(k); unique.push(f); } });
  return unique.filter(f=> dlActiveTypes.has(f.type));
}
function escapeRegExp(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

function buildExtractionHtml(text, entities){
  let html = text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  const uniqueTexts = [...new Set(entities.map(e=>e.text))].sort((a,b)=>b.length-a.length);
  uniqueTexts.forEach(txt=>{
    const ent = entities.find(e=>e.text===txt);
    const cls = ENT_CSS[ent.type] || "org";
    const safe = txt.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    const re = new RegExp(escapeRegExp(safe));
    html = html.replace(re, `<span class="ent-tag ${cls}">${safe}<sup>${ent.type.slice(0,3)}</sup></span>`);
  });
  return html;
}
function buildChipHtml(entities){
  return entities.length
    ? entities.map(e=>`<span style="font-family:var(--font-mono); font-size:10px; padding:4px 9px; border-radius:12px; border:1px solid var(--border); color:var(--ink-faint); margin:3px 4px 0 0; display:inline-block;">${e.type} \u00b7 ${e.text}${e.matched_entity? ' \u2192 '+e.matched_entity:''}</span>`).join("")
    : `<span style="color:var(--ink-faint); font-family:var(--font-mono); font-size:11px;">${t('no_entities_detected')}</span>`;
}

function renderLiveResult(text){
  const entities = runLiveExtraction(text);
  const html = buildExtractionHtml(text, entities) || `<span style="color:var(--ink-faint)">${t('no_text_entered')}</span>`;
  document.getElementById("live-output").innerHTML = `
    <div class="conn-list-title" style="margin-top:4px;">${t('extraction_result_title')}</div>
    <div class="dl-doc-card"><div class="doc-text">${html}</div></div>
    <div class="live-summary" style="margin-top:12px;">${buildChipHtml(entities)}</div>`;
}

document.getElementById("btn-run-extraction").addEventListener("click", ()=> renderLiveResult(document.getElementById("live-input").value));
document.getElementById("btn-example-1").addEventListener("click", ()=>{ document.getElementById("live-input").value = DATA.example_texts[0]; renderLiveResult(DATA.example_texts[0]); });
document.getElementById("btn-example-2").addEventListener("click", ()=>{ document.getElementById("live-input").value = DATA.example_texts[1]; renderLiveResult(DATA.example_texts[1]); });

const MODE_BUTTONS = ["btn-mode-sample","btn-mode-custom","btn-mode-upload"];
const MODE_PANELS = {"btn-mode-sample":"sample-doc-mode", "btn-mode-custom":"custom-mode", "btn-mode-upload":"upload-mode"};
function switchMode(activeBtnId){
  MODE_BUTTONS.forEach(id=>{
    document.getElementById(id).classList.toggle("active", id===activeBtnId);
    const panelId = MODE_PANELS[id];
    const panel = document.getElementById(panelId);
    if(panelId === "sample-doc-mode"){ panel.style.display = (id===activeBtnId) ? "" : "none"; }
    else{ panel.classList.toggle("show", id===activeBtnId); }
  });
}
document.getElementById("btn-mode-sample").addEventListener("click", ()=> switchMode("btn-mode-sample"));
document.getElementById("btn-mode-custom").addEventListener("click", ()=> switchMode("btn-mode-custom"));
document.getElementById("btn-mode-upload").addEventListener("click", ()=> switchMode("btn-mode-upload"));

const uploadZone = document.getElementById("dl-upload-zone");
const fileInput = document.getElementById("dl-file-input");
function handleUploadedFile(file){
  if(!file) return;
  document.getElementById("upload-filename").textContent = t('upload_loaded', file.name, (file.size/1024).toFixed(1));
  if(!file.name.toLowerCase().endsWith(".txt")){
    document.getElementById("upload-output").innerHTML = `<div class="live-chip" style="border-color:var(--red); color:var(--red);">${t('upload_txt_only')}</div>`;
    return;
  }
  const reader = new FileReader();
  reader.onload = (e)=>{
    const text = e.target.result;
    const entities = runLiveExtraction(text);
    const html = buildExtractionHtml(text, entities);
    document.getElementById("upload-output").innerHTML = `
      <div class="dl-doc-card"><div class="doctitle">${file.name}</div><div class="doc-text">${html}</div></div>
      <div style="margin-top:12px;">${buildChipHtml(entities)}</div>`;
  };
  reader.onerror = ()=>{ document.getElementById("upload-output").innerHTML = `<div class="live-chip" style="border-color:var(--red); color:var(--red);">${t('upload_read_error')}</div>`; };
  reader.readAsText(file);
}
uploadZone.addEventListener("click", ()=> fileInput.click());
fileInput.addEventListener("change", (e)=> handleUploadedFile(e.target.files[0]));
uploadZone.addEventListener("dragover", (e)=>{ e.preventDefault(); uploadZone.classList.add("dragover"); });
uploadZone.addEventListener("dragleave", ()=> uploadZone.classList.remove("dragover"));
uploadZone.addEventListener("drop", (e)=>{
  e.preventDefault(); uploadZone.classList.remove("dragover");
  if(e.dataTransfer.files.length) handleUploadedFile(e.dataTransfer.files[0]);
});

function renderConflicts(threshold){
  const rows = DATA.resolution.map(r=>{
    const meetsThreshold = r.confidence >= threshold;
    const label = meetsThreshold ? t('dl_auto_merge') : t('dl_needs_review');
    return {r, meetsThreshold, label};
  });
  const unresolvedCount = rows.filter(x=>!x.meetsThreshold).length;
  document.getElementById("dl-conflicts-title").innerHTML = t('dl_conflicts_title') + ' (<span id="conflict-count">' + unresolvedCount + '</span>)';
  document.getElementById("conflict-list").innerHTML = rows.map(({r, meetsThreshold, label}, i)=>`
    <div class="conflict-card" id="conflict-${i}">
      <div class="head">"${r.mention}" \u2192 ${r.matched_person_name}</div>
      <div class="sub">${label} \u00b7 ${t('dl_source_prefix')} ${r.source_doc}</div>
      <div class="conflict-opt"><span>${r.matched_person_name}</span><span class="pct">${Math.round(r.confidence*100)}%</span></div>
      <div class="conflict-btns">
        <button class="btn-accept" data-i="${i}">${t('btn_accept')}</button>
        <button class="btn-edit" data-i="${i}">${t('btn_edit')}</button>
      </div>
    </div>`).join("");
  document.querySelectorAll(".btn-accept").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      btn.textContent = t('btn_accept_done'); btn.classList.add("done");
      document.getElementById("conflict-"+btn.dataset.i).classList.add("resolved");
    });
  });
  document.querySelectorAll(".btn-edit").forEach(btn=>{
    btn.addEventListener("click", ()=> alert(t('alert_edit_msg')));
  });
}

/* ---------------- REPORT ---------------- */
let CURRENT_REPORT_FILTER = "ALL";

function renderReportPage(){
  const reportH2 = document.querySelector('[data-page="report"] h2');
  if(reportH2) reportH2.textContent = t('tb_report');
  const badgeSec = document.querySelector('[data-page="report"] .badge-secure');
  if(badgeSec) badgeSec.textContent = t('badge_tagged');

  const blocks = DATA.report_i18n[CURRENT_LANG] || DATA.report_i18n.en;
  const sectionTitles = DATA.report_section_titles[CURRENT_LANG] || DATA.report_section_titles.en;

  // 1. Calculate statement counts
  const factCount = blocks.filter(b=>b.tag_key==="FACT").length;
  const infCount = blocks.filter(b=>b.tag_key==="AI_INFERENCE").length;
  const leadCount = blocks.filter(b=>b.tag_key==="LEAD").length;

  const statSummaryEl = document.getElementById("report-stat-summary");
  if(statSummaryEl){
    statSummaryEl.innerHTML = `
      <div class="rec-stat-box"><div class="k">Verified Facts</div><div class="v" style="color:var(--cyan);">${factCount}</div></div>
      <div class="rec-stat-box"><div class="k">AI Inferences</div><div class="v" style="color:var(--amber);">${infCount}</div></div>
      <div class="rec-stat-box"><div class="k">Investigative Leads</div><div class="v" style="color:var(--red);">${leadCount}</div></div>
      <div class="rec-stat-box"><div class="k">Evidentiary Standard</div><div class="v" style="font-size:16px; margin-top:5px; color:var(--blue);">Court-Support</div></div>
    `;
  }

  // 2. Group statements by section
  const sectionsMap = {};
  blocks.forEach(b=>{
    if(!sectionsMap[b.section]) sectionsMap[b.section] = [];
    sectionsMap[b.section].push(b);
  });

  const esc = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  let sectionsHtml = "";

  Object.keys(sectionsMap).sort().forEach(secKey=>{
    const stmts = sectionsMap[secKey];
    const filteredStmts = (CURRENT_REPORT_FILTER === "ALL") 
      ? stmts 
      : stmts.filter(s => s.tag_key === CURRENT_REPORT_FILTER);

    if(!filteredStmts.length && CURRENT_REPORT_FILTER !== "ALL") return;

    sectionsHtml += `
      <div class="report-section-card">
        <div class="report-section-head">
          <span>${sectionTitles["s"+secKey] || "Section " + secKey}</span>
          <span style="font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); font-weight:normal;">${filteredStmts.length} statement(s)</span>
        </div>
        <div class="report-statement-list">
          ${filteredStmts.map(s=>`
            <div class="statement-card ${s.tag_key}">
              <span class="stmt-tag ${s.tag_key}">[${esc(s.tag_label)}]</span>
              <div class="stmt-text">${esc(s.text)}</div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  });

  const container = document.getElementById("report-sections-container");
  if(container){
    container.innerHTML = sectionsHtml || `<div style="padding:40px; text-align:center; color:var(--ink-faint); font-family:var(--font-mono);">No statements match the selected filter.</div>`;
  }
}

// Wire filter buttons
document.querySelectorAll(".rf-btn").forEach(btn=>{
  btn.addEventListener("click", ()=>{
    document.querySelectorAll(".rf-btn").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    CURRENT_REPORT_FILTER = btn.dataset.filter;
    renderReportPage();
  });
});

/* ---------------- INITIAL RENDER (page load) ---------------- */
applyStaticI18n();
renderLegend();
renderCommandCenter();
renderEpGrid();
renderChips();
renderSampleDocs();
renderConflicts(parseInt(document.getElementById("thresh-slider").value,10)/100);
renderReportPage();

/* ============================================================
   AI INVESTIGATION ASSISTANT
   Real, working query engine — no external LLM/backend involved.
   Every answer is derived directly from DATA (the same computed
   graph/risk/resolution output used everywhere else in the app),
   and every answer states its source and, where relevant, a note
   that human verification is required. Nothing is invented.
   ============================================================ */

/* ---- entity matching: find known entities mentioned in free text ---- */
function asstFindEntities(query){
  const qUpper = query.toUpperCase();
  const found = [];
  DATA.nodes.forEach(n=>{
    const idx = qUpper.indexOf(n.label.toUpperCase());
    if(idx !== -1) found.push({node:n, idx});
  });
  // de-dup: if one label is a substring of another matched label, keep only the longer/more specific one
  const filtered = found.filter(f => !found.some(g => g!==f && g.node.label.length>f.node.label.length && g.node.label.toUpperCase().includes(f.node.label.toUpperCase())));
  filtered.sort((a,b)=> a.idx - b.idx);
  const seen = new Set(); const result = [];
  filtered.forEach(f=>{ if(!seen.has(f.node.id)){ seen.add(f.node.id); result.push(f.node); } });
  return result;
}

/* ---- shortest path via BFS over DATA.edges ---- */
function asstShortestPath(startId, endId){
  if(startId === endId) return {path:[startId], edges:[]};
  const adj = {};
  DATA.edges.forEach(e=>{
    const s = e.source, tt = e.target;
    (adj[s] = adj[s] || []).push({to:tt, edge:e});
    (adj[tt] = adj[tt] || []).push({to:s, edge:e});
  });
  const visited = new Set([startId]);
  const queue = [{node:startId, path:[startId], edges:[]}];
  while(queue.length){
    const cur = queue.shift();
    if(cur.node === endId) return {path:cur.path, edges:cur.edges};
    (adj[cur.node] || []).forEach(nb=>{
      if(!visited.has(nb.to)){
        visited.add(nb.to);
        queue.push({node:nb.to, path:[...cur.path, nb.to], edges:[...cur.edges, nb.edge]});
      }
    });
  }
  return null;
}

/* ---- response builder: every answer follows Claim -> Evidence -> Source -> Confidence -> Verify ---- */
function asstBuildResponse(html, evidenceRows, opts){
  opts = opts || {};
  let out = `<div>${html}</div>`;
  if(evidenceRows && evidenceRows.length){
    out += `<div class="asst-evidence">`;
    evidenceRows.forEach(r=> out += `<div class="asst-evidence-row"><span class="k">${r.k}</span><span class="v">${r.v}</span></div>`);
    out += `</div>`;
  }
  if(opts.confidence){
    out += `<div class="asst-confidence-pill">${t('asst_confidence_label')}: ${opts.confidence}</div>`;
  }
  if(opts.verify){
    out += `<div class="asst-verify">${t('asst_verify_note')}</div>`;
  } else if(opts.graphVerified){
    out += `<div class="asst-confidence-pill" style="background:rgba(22,163,74,0.1); color:var(--green);">${t('asst_graph_verified')}</div>`;
  }
  return out;
}

function asstEntityTypeLabel(node){
  return t((TYPE_META[node.type]||TYPE_META.person).labelKey);
}

/* ---- intent handlers ---- */
function asstHandleWhoConnects(entities){
  if(entities.length < 2) return asstBuildResponse(t('asst_need_two_entities'));
  const [a,b] = entities;
  const result = asstShortestPath(a.id, b.id);
  if(!result) return asstBuildResponse(t('asst_path_none', a.label, b.label));
  const pathLabels = result.path.map(id => DATA.id_to_label[id] || id).join(' \u2192 ');
  const evidence = result.edges.map((e,i)=>({
    k: t('asst_relationship_label').toUpperCase(),
    v: `${DATA.id_to_label[e.source]||e.source} \u2192 ${DATA.id_to_label[e.target]||e.target} (${(e.display_label || e.type || '').toLowerCase()})`
  }));
  const html = `${t('asst_path_intro', a.label, b.label)}<br><b>${pathLabels}</b> <span style="color:var(--ink-faint);">(${t('asst_path_hops', result.edges.length)})</span>`;
  return asstBuildResponse(html, evidence, {graphVerified:true});
}

function asstHandleWhyFlagged(entities){
  if(entities.length === 0) return asstBuildResponse(t('asst_no_entity_found'));
  const d = entities[0];
  if(!d.risk) return asstBuildResponse(t('asst_why_none', d.label));
  const reasons = getRiskReasons(d);
  const html = t('asst_why_intro', d.label, d.risk.risk_indicator_score);
  const evidence = reasons.map(r=>({k:'\u2022', v:r}));
  evidence.push({k: t('asst_source_label').toUpperCase(), v: t('source_reliability_mult') + `: \u00d7${d.risk.breakdown.source_reliability_multiplier}`});
  return asstBuildResponse(html, evidence, {verify:true});
}

function asstHandleConnections(entities){
  if(entities.length === 0) return asstBuildResponse(t('asst_no_entity_found'));
  const d = entities[0];
  const connected = DATA.edges.filter(e => e.source===d.id || e.target===d.id).map(e=>{
    const otherId = e.source===d.id ? e.target : e.source;
    const other = DATA.nodes.find(n=>n.id===otherId);
    return {other, label: e.display_label || e.type, susp: !!e.suspicious};
  }).filter(c=>c.other);
  if(connected.length === 0) return asstBuildResponse(t('asst_connections_none', d.label));
  const html = t('asst_connections_intro', d.label, connected.length);
  const evidence = connected.slice(0,8).map(c=>({
    k: c.susp ? '\u26a0' : '\u2022',
    v: `${c.other.label} \u2014 ${(c.label||'').toString().toLowerCase()}`
  }));
  return asstBuildResponse(html, evidence, {graphVerified: !connected.some(c=>c.susp), verify: connected.some(c=>c.susp)});
}

function asstHandleTopPriority(){
  const evidence = DATA.priority_ranking.slice(0,5).map((id,i)=>{
    const n = DATA.nodes.find(x=>x.id===id);
    if(!n) return null;
    const score = n.risk ? n.risk.risk_indicator_score : Math.round(n.degree*100);
    return {k: `#${i+1}`, v: `${n.label} (${asstEntityTypeLabel(n)}) \u2014 ${score}`};
  }).filter(Boolean);
  return asstBuildResponse(t('asst_top_priority_intro'), evidence, {verify:true});
}

function asstHandleSummary(){
  const highRisk = (DATA.risk||[]).filter(r=>r.risk_indicator_score>=45).length;
  const suspicious = DATA.edges.filter(e=>e.suspicious).length;
  const evidence = [
    {k:'\u2022', v:t('asst_summary_entities', DATA.nodes.length)},
    {k:'\u2022', v:t('asst_summary_edges', DATA.edges.length)},
    {k:'\u2022', v:t('asst_summary_communities', DATA.communities.length)},
    {k:'\u2022', v:t('asst_summary_highrisk', highRisk)},
    {k:'\u2022', v:t('asst_summary_suspicious', suspicious)},
  ];
  return asstBuildResponse(t('asst_summary_intro'), evidence, {graphVerified:true});
}

function asstHandleFinancial(){
  const txns = DATA.edges.filter(e=>e.type==="TRANSFERRED_MONEY");
  if(txns.length===0) return asstBuildResponse(t('asst_financial_none'));
  const evidence = txns.map(e=>({
    k: e.suspicious ? '\u26a0' : t('asst_amount_label').toUpperCase(),
    v: `${DATA.id_to_label[e.source]||e.source} \u2192 ${DATA.id_to_label[e.target]||e.target}: ${e.display_label||''}`
  }));
  return asstBuildResponse(t('asst_financial_intro'), evidence, {verify: txns.some(e=>e.suspicious), graphVerified: !txns.some(e=>e.suspicious)});
}

function asstHandleSuspicious(){
  const susp = DATA.edges.filter(e=>e.suspicious);
  if(susp.length===0) return asstBuildResponse(t('asst_suspicious_none'));
  const evidence = susp.map(e=>({
    k: '\u26a0',
    v: `${DATA.id_to_label[e.source]||e.source} \u2194 ${DATA.id_to_label[e.target]||e.target} (${e.display_label||e.type})`
  }));
  return asstBuildResponse(t('asst_suspicious_intro'), evidence, {verify:true});
}

function asstHandleGenericEntity(entities){
  const d = entities[0];
  const connected = DATA.edges.filter(e => e.source===d.id || e.target===d.id).length;
  const html = t('asst_entity_profile_intro', d.label, asstEntityTypeLabel(d));
  const evidence = [{k: t('asst_relationship_label').toUpperCase(), v: connected}];
  if(d.type==="person"){
    evidence.push({k: t('aliases').toUpperCase(), v: (d.aliases&&d.aliases.length)?d.aliases.join(", "):t('none_on_record')});
    if(d.risk) evidence.push({k: t('risk_indicator_label').toUpperCase(), v: `${d.risk.risk_indicator_score}/100`});
  }
  return asstBuildResponse(html, evidence, {graphVerified:true});
}

/* ---- main dispatcher ---- */
function asstAnswer(query){
  const q = query.toLowerCase();
  const entities = asstFindEntities(query);

  if(/who connects|connection between|path between|link between|connects .* and|\u0915\u094c\u0928 \u091c\u094b\u0921\u093c|\u0915\u094b\u0923 \u091c\u094b\u0921\u0924\u0947|\u0915\u0947 \u092c\u0940\u091a/.test(q)){
    return asstHandleWhoConnects(entities);
  }
  if(/why (is|was)|why.*flag|why.*priorit|why.*risk|\u0915\u094d\u092f\u094b\u0902 \u091a\u093f\u0928\u094d\u0939\u093f\u0924|\u0915\u093e \u091a\u093f\u0928\u094d\u0939\u093e\u0902\u0915\u093f\u0924/.test(q)){
    return asstHandleWhyFlagged(entities);
  }
  if(/connection[s]? of|connected to|who.*connected|show.*connection|\u0938\u0902\u092c\u0902\u0927 \u0926\u093f\u0916\u093e\u090f\u0902|\u0938\u0902\u092c\u0902\u0927 \u0926\u093e\u0916\u0935\u093e|\u091c\u0941\u0921\u093c\u093e/.test(q)){
    return asstHandleConnections(entities);
  }
  if(/top priorit|high risk|most important|key entit|priority entit|\u0936\u0940\u0930\u094d\u0937 \u092a\u094d\u0930\u093e\u0925\u092e\u093f\u0915\u0924\u093e|\u0936\u0940\u0930\u094d\u0937 \u092a\u094d\u0930\u093e\u0927\u093e\u0928\u094d\u092f|\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u093f\u092e|\u0909\u091a\u094d\u091a \u091c\u094b\u0916\u0940\u092e/.test(q)){
    return asstHandleTopPriority();
  }
  if(/summar|case overview|overview of the case|\u0938\u093e\u0930\u093e\u0902\u0936/.test(q)){
    return asstHandleSummary();
  }
  if(/financ|transaction|money transfer|fund transfer|\u0935\u093f\u0924\u094d\u0924\u0940\u092f|\u0906\u0930\u094d\u0925\u093f\u0915|\u0932\u0947\u0928\u0926\u0947\u0928|\u0939\u0938\u094d\u0924\u093e\u0902\u0924\u0930\u0923/.test(q)){
    return asstHandleFinancial();
  }
  if(/suspicious|anomal|flagged pattern|\u0938\u0902\u0926\u093f\u0917\u094d\u0927|\u0938\u0902\u0936\u092f\u093f\u0924/.test(q)){
    return asstHandleSuspicious();
  }
  if(entities.length >= 2){
    return asstHandleWhoConnects(entities);
  }
  if(entities.length === 1){
    return asstHandleGenericEntity(entities);
  }
  const evidence = [
    {k:'\u2022', v: t('chip_who_connects')},
    {k:'\u2022', v: t('chip_why_flagged')},
    {k:'\u2022', v: t('chip_top_priority')},
    {k:'\u2022', v: t('chip_summarize')},
  ];
  return asstBuildResponse(t('asst_fallback'), evidence);
}

/* ---- Assistant UI wiring ---- */
let ASST_HISTORY = [];
function asstRenderMessages(){
  const container = document.getElementById("asst-messages");
  if(!container) return;
  container.innerHTML = ASST_HISTORY.map(m=>{
    if(m.role === "user"){
      return `<div class="asst-msg user">
        <div class="asst-msg-avatar">${ICONS.person}</div>
        <div class="asst-bubble">${m.text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}</div>
      </div>`;
    }
    return `<div class="asst-msg assistant">
      <div class="asst-msg-avatar">\u2726</div>
      <div class="asst-bubble">${m.html}</div>
    </div>`;
  }).join("");
  container.scrollTop = container.scrollHeight;
}

const ASST_CHIPS = [
  {key:"chip_who_connects", intent:"who_connects", args:["Rajeev Malhotra","Anita Rao"]},
  {key:"chip_why_flagged", intent:"why_flagged", args:["Vikram Solanki"]},
  {key:"chip_top_priority", intent:"top_priority", args:[]},
  {key:"chip_summarize", intent:"summary", args:[]},
  {key:"chip_suspicious", intent:"suspicious", args:[]},
  {key:"chip_financial", intent:"financial", args:[]},
];
function asstResolveEntities(names){
  return names.map(name => DATA.nodes.find(n => n.label === name)).filter(Boolean);
}
function asstAnswerByIntent(intent, args){
  switch(intent){
    case "who_connects": return asstHandleWhoConnects(asstResolveEntities(args));
    case "why_flagged": return asstHandleWhyFlagged(asstResolveEntities(args));
    case "top_priority": return asstHandleTopPriority();
    case "summary": return asstHandleSummary();
    case "suspicious": return asstHandleSuspicious();
    case "financial": return asstHandleFinancial();
    default: return asstBuildResponse(t('asst_fallback'));
  }
}
function asstRenderSuggestions(){
  const el = document.getElementById("asst-suggestions");
  if(!el) return;
  el.innerHTML = ASST_CHIPS.map((c,i)=>`<div class="asst-chip" data-idx="${i}">${t(c.key)}</div>`).join("");
  el.querySelectorAll(".asst-chip").forEach(chip=>{
    chip.addEventListener("click", ()=>{
      const cfg = ASST_CHIPS[parseInt(chip.dataset.idx,10)];
      asstSubmitDirect(t(cfg.key), asstAnswerByIntent(cfg.intent, cfg.args));
    });
  });
}

function asstShowTypingThen(displayText, resolveHtml){
  ASST_HISTORY.push({role:"user", text:displayText});
  asstRenderMessages();
  const container = document.getElementById("asst-messages");
  const typingId = "asst-typing-" + Date.now();
  container.insertAdjacentHTML("beforeend", `<div class="asst-msg assistant" id="${typingId}">
    <div class="asst-msg-avatar">\u2726</div>
    <div class="asst-bubble"><div class="asst-typing"><span></span><span></span><span></span></div></div>
  </div>`);
  container.scrollTop = container.scrollHeight;
  setTimeout(()=>{
    const el = document.getElementById(typingId);
    if(el) el.remove();
    const html = (typeof resolveHtml === "function") ? resolveHtml() : resolveHtml;
    ASST_HISTORY.push({role:"assistant", html});
    asstRenderMessages();
  }, 450);
}

/* Used by suggestion chips: bypasses free-text keyword parsing entirely,
   so chip answers are always correct regardless of the active UI language. */
function asstSubmitDirect(displayText, html){
  asstShowTypingThen(displayText, html);
}

/* Used by the free-text input box: parses typed text via keyword matching. */
function asstSubmit(queryText){
  const query = (queryText !== undefined) ? queryText : document.getElementById("asst-input").value;
  if(!query || !query.trim()) return;
  document.getElementById("asst-input").value = "";
  asstShowTypingThen(query, ()=> asstAnswer(query));
}

function initAssistant(){
  if(ASST_HISTORY.length === 0){
    ASST_HISTORY.push({role:"assistant", html: `<div>${t('asst_welcome')}</div>`});
  }
  asstRenderMessages();
  asstRenderSuggestions();
}

const asstSendBtn = document.getElementById("asst-send");
const asstInputEl = document.getElementById("asst-input");
if(asstSendBtn){ asstSendBtn.addEventListener("click", ()=> asstSubmit()); }
if(asstInputEl){ asstInputEl.addEventListener("keydown", (e)=>{ if(e.key === "Enter") asstSubmit(); }); }

document.querySelector('.sb-item[data-page="assistant"]').addEventListener("click", ()=> initAssistant());
