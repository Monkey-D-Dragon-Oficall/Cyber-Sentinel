class AIRiskScorer:
    """
    نظام تقييم المخاطر بالذكاء الاصطناعي (AI-Risk Scoring)
    ترتيب الثغرات بناءً على خطورتها وتأثيرها.
    """
    def __init__(self):
        self.severity_map = {
            "Critical": 10,
            "High": 7,
            "Medium": 4,
            "Low": 2,
            "Info": 0
        }

    def calculate_score(self, vulnerability_type: str, evidence_quality: float) -> dict:
        """
        حساب درجة الخطورة بناءً على نوع الثغرة وجودة الدليل
        """
        base_scores = {
            "SQL Injection": "Critical",
            "SSRF": "High",
            "IDOR": "High",
            "Sensitive File": "Medium",
            "API Key Leak": "High",
            "Information Disclosure": "Low"
        }
        
        severity = base_scores.get(vulnerability_type, "Info")
        score = self.severity_map[severity] * evidence_quality
        
        return {
            "severity": severity,
            "score": round(score, 2),
            "priority": "Immediate Action Required" if score > 7 else "Monitor"
        }
