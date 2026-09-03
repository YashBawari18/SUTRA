from sklearn.ensemble import IsolationForest
import numpy as np

def detect_financial_anomalies(transactions):
    """
    Uses Isolation Forest to detect anomalous financial transactions.
    transactions: list of dicts {"id": str, "amount": float, "frequency": int}
    """
    if not transactions or len(transactions) < 5:
        # Not enough data for ML
        return {t["id"]: {"is_anomaly": False, "score": 0} for t in transactions}

    # Extract features for ML model
    features = np.array([[t["amount"], t["frequency"]] for t in transactions])
    
    # Initialize Isolation Forest
    clf = IsolationForest(contamination=0.1, random_state=42)
    predictions = clf.fit_predict(features)
    scores = clf.decision_function(features)
    
    results = {}
    for i, t in enumerate(transactions):
        results[t["id"]] = {
            "is_anomaly": bool(predictions[i] == -1),
            "anomaly_score": round(float(scores[i]), 4),
            "reason": "Unusual amount/frequency detected by ML model" if predictions[i] == -1 else ""
        }
        
    return results

def compute_hybrid_risk(entity_data, graph_metrics, ml_anomalies):
    """
    Computes a hybrid risk score (0-100) combining rule-based, graph, and ML signals.
    """
    base_risk = 10
    
    # 1. Graph Risk (Highly central nodes are riskier in a criminal network)
    graph_score = 0
    if graph_metrics:
        graph_score += graph_metrics.get("degree_centrality", 0) * 40
        graph_score += graph_metrics.get("betweenness_centrality", 0) * 30
        
    # 2. ML Risk
    ml_score = 0
    if ml_anomalies and ml_anomalies.get("is_anomaly"):
        ml_score += 40

    # 3. Rule-based Risk (e.g. Communication bursts, specific watchlists)
    rule_score = 0
    if entity_data.get("communication_bursts", 0) > 3:
        rule_score += 25
        
    total_risk = min(100, base_risk + graph_score + ml_score + rule_score)
    
    reasons = []
    if graph_score > 20: reasons.append("High network centrality")
    if ml_score > 0: reasons.append("Financial ML Anomaly")
    if rule_score > 0: reasons.append("Communication pattern matches rule")
    
    return {
        "hybrid_risk_score": round(total_risk, 2),
        "risk_level": "CRITICAL" if total_risk > 75 else "HIGH" if total_risk > 50 else "MODERATE",
        "signals": reasons
    }
