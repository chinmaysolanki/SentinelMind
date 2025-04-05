import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

class CVEFetcher:
    def __init__(self):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.logger = logging.getLogger(__name__)

    def fetch_recent_cves(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Fetch recent CVEs from NVD API
        
        Args:
            days_back: Number of days to look back for CVEs
            
        Returns:
            List of CVE entries with relevant information
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for API
            start_date_str = start_date.strftime("%Y-%m-%dT00:00:00:000 UTC-00:00")
            end_date_str = end_date.strftime("%Y-%m-%dT23:59:59:999 UTC-00:00")
            
            # Prepare API request
            params = {
                "pubStartDate": start_date_str,
                "pubEndDate": end_date_str,
                "resultsPerPage": 50,
                "startIndex": 0
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            cves = []
            
            for cve in data.get("vulnerabilities", []):
                cve_data = cve.get("cve", {})
                cves.append({
                    "id": cve_data.get("id"),
                    "published": cve_data.get("published"),
                    "lastModified": cve_data.get("lastModified"),
                    "description": cve_data.get("descriptions", [{}])[0].get("value", ""),
                    "severity": self._get_severity(cve_data),
                    "source": "NVD"
                })
            
            return cves
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching CVEs: {str(e)}")
            return []
            
    def _get_severity(self, cve_data: Dict[str, Any]) -> str:
        """Extract severity from CVE data"""
        metrics = cve_data.get("metrics", {})
        cvss_v3 = metrics.get("cvssMetricV31", [{}])[0]
        if cvss_v3:
            return cvss_v3.get("cvssData", {}).get("baseSeverity", "UNKNOWN")
        return "UNKNOWN" 