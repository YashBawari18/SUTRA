/**
 * SUTRA API Client
 * Connects the frontend to the live FastAPI backend.
 * Overwrites the local mock DATA object if the backend is reachable.
 */

const API_BASE = "http://localhost:8000/api";

async function fetchLiveCaseData(caseId) {
    try {
        console.log(`[SUTRA API] Attempting to connect to live backend for case ${caseId}...`);
        
        // Example endpoints configured in Phase 1
        // Fetch all data in parallel to save time
        const [
            graphResponse, caseResponse, timelineResponse, 
            anomaliesResponse, auditResponse, evidenceResponse, correlationResponse
        ] = await Promise.all([
            fetch(`${API_BASE}/graph/${caseId}`),
            fetch(`${API_BASE}/cases/${caseId}`),
            fetch(`${API_BASE}/timeline?case_id=${caseId}`),
            fetch(`${API_BASE}/anomalies?case_id=${caseId}`),
            fetch(`${API_BASE}/audit-logs?case_id=${caseId}`),
            fetch(`${API_BASE}/evidence/${caseId}`),
            fetch(`${API_BASE}/correlation?case_id=${caseId}`)
        ]);
        
        if (graphResponse.ok) {
            const graphData = await graphResponse.json();
            const caseInfo = caseResponse.ok ? await caseResponse.json() : null;
            const timelineData = timelineResponse.ok ? await timelineResponse.json() : null;
            const anomaliesData = anomaliesResponse.ok ? await anomaliesResponse.json() : null;
            const auditData = auditResponse.ok ? await auditResponse.json() : null;
            const evidenceData = evidenceResponse.ok ? await evidenceResponse.json() : null;
            const correlationData = correlationResponse.ok ? await correlationResponse.json() : null;
            
            console.log("[SUTRA API] Successfully connected to live backend.");
            
            // If the live graph has data, we overwrite the local DATA
            if (graphData.nodes && graphData.nodes.length > 0) {
                if (typeof DATA !== 'undefined') {
                    // Map backend Neo4j format to frontend expected format
                    DATA.nodes = graphData.nodes.map(n => ({
                        id: n.id,
                        type: n.labels.length > 0 ? n.labels[0].toLowerCase() : 'unknown',
                        name: n.properties.name || n.id,
                        risk: n.properties.risk_score || n.properties.risk || 0,
                        community: n.properties.community || 1,
                        affiliation: n.properties.affiliation || '',
                        aliases: n.properties.aliases ? n.properties.aliases.split(',') : [],
                        last_known: { location: n.properties.location || 'Unknown' },
                        // copy all other properties
                        ...n.properties
                    }));
                    
                    DATA.edges = graphData.edges.map(e => ({
                        source: e.source,
                        target: e.target,
                        type: e.type.toLowerCase(),
                        weight: e.properties.weight || 1,
                        suspicious: e.properties.suspicious || e.type === 'FLAGGED' || false,
                        amount: e.properties.amount || null,
                        ...e.properties
                    }));
                    
                    console.log("[SUTRA API] Live graph data injected and transformed.");
                    
                    if (timelineData && timelineData.events) {
                        DATA.timeline = timelineData.events.map(e => ({
                            date: e.timestamp,
                            event: e.event_type,
                            entities: [e.description],
                            evidence_ref: e.evidence_id
                        }));
                    }
                    if (anomaliesData && anomaliesData.anomalies) {
                        DATA.risk_signals = anomaliesData.anomalies.map(a => ({
                            entity: a.entity_name,
                            signal: "Automated multi-source anomaly detection",
                            score: a.risk_profile.hybrid_risk_score,
                            details: JSON.stringify(a.risk_profile)
                        }));
                    }
                    if (evidenceData && evidenceData.evidence_vault) {
                        DATA.evidence = evidenceData.evidence_vault.map(ev => ({
                            id: ev.id,
                            filename: ev.filename,
                            type: ev.mime_type,
                            date: ev.upload_date,
                            hash: ev.sha256_hash
                        }));
                    }
                    if (correlationData && correlationData.correlations) {
                        DATA.correlations = correlationData.correlations.map(c => ({
                            entities: [c.entity],
                            description: `Overlap detected across multiple distinct evidence documents`,
                            confidence: "High",
                            sources: c.sources
                        }));
                    }
                }
            } else {
                console.warn("[SUTRA API] Live graph is currently empty. Falling back to default demo synthetic data.");
            }
        }
    } catch (error) {
        console.error("[SUTRA API] Backend is unreachable. Running in offline/demo mode.", error);
    }
}

// In the SUTRA architecture, window load happens synchronously
// We kick off the fetch and if successful, we can re-render specific components.
document.addEventListener("DOMContentLoaded", () => {
    // Connect to the actual "Operation Phantom" case seeded in PostgreSQL/Neo4j
    fetchLiveCaseData("C-0992").then(() => {
        // If a render function exists globally, call it here to refresh view
        if (typeof window.renderNetwork === "function" && document.getElementById("app").classList.contains("show")) {
            // Optional: re-trigger render
        }
    });
});
