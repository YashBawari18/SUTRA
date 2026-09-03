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
        const graphResponse = await fetch(`${API_BASE}/graph/${caseId}`);
        const caseResponse = await fetch(`${API_BASE}/cases/${caseId}`);
        
        if (graphResponse.ok && caseResponse.ok) {
            const graphData = await graphResponse.json();
            const caseInfo = await caseResponse.json();
            
            console.log("[SUTRA API] Successfully connected to live backend.");
            
            // If the live graph has data, we overwrite the local DATA
            // For now, if the graph is completely empty (no nodes), we preserve the demo data
            // to avoid breaking the demonstration flow before Phase 8 (Data Generation) is done.
            if (graphData.nodes && graphData.nodes.length > 0) {
                // Ensure global DATA exists before overriding
                if (typeof DATA !== 'undefined') {
                    // Update nodes and edges from live Neo4j data
                    DATA.nodes = graphData.nodes;
                    DATA.edges = graphData.edges;
                    console.log("[SUTRA API] Live graph data injected.");
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
    // Assuming CASE-0001 or similar is active for demo
    fetchLiveCaseData("C-0417").then(() => {
        // If a render function exists globally, call it here to refresh view
        if (typeof window.renderNetwork === "function" && document.getElementById("app").classList.contains("show")) {
            // Optional: re-trigger render
        }
    });
});
