import os
from fpdf import FPDF
import pandas as pd

# # 1. incidents.pdf
# incident_data = [
#     {
#         "Incident ID": "INC001",
#         "Team": "Network",
#         "Problem": "High latency in API calls",
#         "Root Cause": "Misconfigured load balancer rule",
#         "Resolution": "Updated the load balancer configuration"
#     },
#     {
#         "Incident ID": "INC002",
#         "Team": "Database",
#         "Problem": "Unable to connect to DB cluster",
#         "Root Cause": "Expired SSL certificate",
#         "Resolution": "Renewed the certificate and restarted services"
#     },
#     {
#         "Incident ID": "INC003",
#         "Team": "Storage",
#         "Problem": "Frequent disk IO errors",
#         "Root Cause": "Faulty SSD on node 4",
#         "Resolution": "Replaced the faulty SSD"
#     },
#     {
#         "Incident ID": "INC004",
#         "Team": "Application",
#         "Problem": "Web app timeout errors during peak hours",
#         "Root Cause": "Inefficient database queries under load",
#         "Resolution": "Optimized queries and added caching layer"
#     },
#     {
#         "Incident ID": "INC005",
#         "Team": "Security",
#         "Problem": "Unauthorized login attempts detected",
#         "Root Cause": "Exposed SSH port with weak password policy",
#         "Resolution": "Implemented IP filtering and updated SSH policy"
#     },
#     {
#         "Incident ID": "INC006",
#         "Team": "DevOps",
#         "Problem": "CI/CD pipeline failing during deployment",
#         "Root Cause": "Corrupt Docker image in registry",
#         "Resolution": "Rebuilt image and purged cache in registry"
#     },
#     {
#         "Incident ID": "INC007",
#         "Team": "Monitoring",
#         "Problem": "Missing alerts for CPU spikes",
#         "Root Cause": "Incorrect threshold set in alert rule",
#         "Resolution": "Adjusted alert thresholds and tested rules"
#     },
#     {
#         "Incident ID": "INC008",
#         "Team": "Network",
#         "Problem": "Intermittent packet loss in VPN",
#         "Root Cause": "Flaky link between data centers",
#         "Resolution": "Rerouted VPN over redundant link"
#     },
#     {
#         "Incident ID": "INC009",
#         "Team": "Database",
#         "Problem": "Slow replication between master and slave",
#         "Root Cause": "Heavy write load and insufficient bandwidth",
#         "Resolution": "Scheduled heavy writes during off-peak hours"
#     },
#     {
#         "Incident ID": "INC010",
#         "Team": "Storage",
#         "Problem": "Backup process failing nightly",
#         "Root Cause": "Quota exceeded on backup volume",
#         "Resolution": "Increased volume size and enabled cleanup job"
#     },
#     {
#         "Incident ID": "INC011",
#         "Team": "Support",
#         "Problem": "Users unable to reset password",
#         "Root Cause": "SMTP server misconfiguration",
#         "Resolution": "Updated SMTP credentials and restarted service"
#     },
#     {
#         "Incident ID": "INC012",
#         "Team": "Analytics",
#         "Problem": "Missing data in dashboards",
#         "Root Cause": "Kafka topic retention too short",
#         "Resolution": "Extended retention policy to 7 days"
#     },
#     {
#         "Incident ID": "INC013",
#         "Team": "DevOps",
#         "Problem": "Automated deployment failed on staging",
#         "Root Cause": "Version mismatch in config templates",
#         "Resolution": "Synced config files and added version check"
#     },
#     {
#         "Incident ID": "INC014",
#         "Team": "Application",
#         "Problem": "Service returns 500 error intermittently",
#         "Root Cause": "Memory leak in new service version",
#         "Resolution": "Rolled back release and fixed memory issue"
#     },
#     {
#         "Incident ID": "INC015",
#         "Team": "Monitoring",
#         "Problem": "Too many false positive alerts",
#         "Root Cause": "Test environment accidentally monitored",
#         "Resolution": "Excluded non-prod environments from alert config"
#     }
# ]

# knowledge_article="""
# INC001:
# The Network team investigated high latency in API calls, which was affecting application performance. The root cause was identified as a misconfigured load balancer rule that routed traffic inefficiently. The issue was resolved by updating the load balancer configuration to optimize routing.

# INC002:
# The Database team faced a major issue where the system could not connect to the database cluster. Upon analysis, the root cause was found to be an expired SSL certificate on the database node. The team renewed the certificate and restarted the necessary services to restore connectivity.

# INC003:
# The Storage team observed frequent disk I/O errors that impacted read/write operations. Diagnosis revealed a faulty SSD on node 4. The problem was resolved by replacing the defective SSD with a healthy one.

# INC004:
# Users experienced web application timeouts during peak usage hours. The Application team traced the issue to inefficient database queries that could not handle high concurrency. To resolve this, queries were optimized and a caching layer was introduced to reduce database load.

# INC005:
# Security logs showed multiple unauthorized login attempts. Investigation revealed an exposed SSH port combined with a weak password policy. The Security team mitigated this by enabling IP filtering and updating the SSH configuration to enforce stronger access controls.

# INC006:
# The DevOps team encountered failures in the CI/CD deployment pipeline. A corrupt Docker image in the registry was identified as the root cause. The issue was fixed by rebuilding the image and purging the Docker cache to prevent reuse of broken layers.

# INC007:
# CPU spikes were not being reported as alerts, leading to delayed response to performance issues. It was discovered that the alert thresholds were incorrectly configured. The Monitoring team corrected the thresholds and thoroughly tested the alert rules to ensure reliability.

# INC008:
# Users connected via VPN reported intermittent packet loss. The Network team traced this to an unreliable link between two data centers. As a solution, VPN traffic was rerouted through a redundant and more stable link.

# INC009:
# Database replication lag was increasing consistently. Analysis showed that heavy write operations during peak hours were overwhelming the replication process, compounded by limited bandwidth. The solution involved deferring non-critical writes to off-peak hours.

# INC010:
# Nightly backup jobs were failing consistently. Investigation revealed that the backup volume had exceeded its storage quota. The team increased the volume size and also implemented a scheduled job to clean up older backup files.

# INC011:
# Several users reported they were unable to reset their passwords. The issue was traced to a misconfigured SMTP server that was failing to send verification emails. The Support team updated the SMTP credentials and restarted the mail service to resolve the issue.

# INC012:
# Analytics dashboards were missing recent data. The root cause was found to be a Kafka topic with a retention period too short to preserve the necessary messages. The Analytics team extended the topic retention period to 7 days to ensure data availability.

# INC013:
# The staging environment encountered deployment failures during automated releases. The DevOps team identified a version mismatch in the configuration templates as the root cause. Synchronizing the templates and introducing version checks resolved the issue.

# INC014:
# A service was intermittently returning HTTP 500 errors. Memory profiling indicated a leak introduced in the latest deployment. The Application team rolled back to the previous stable version and fixed the memory issue before redeploying.

# INC015:
# The Monitoring team received a flood of false-positive alerts. It was discovered that alert rules were incorrectly applied to test environments. The configuration was updated to scope alert rules strictly to production environments.
# """

# # create PDF for this article
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)
# for line in knowledge_article.strip().split("\n"):
#     pdf.multi_cell(0, 10, txt=line.strip())
# pdf_path = "knowledge_article.pdf"
# pdf.output(pdf_path)

# # create PDF for incident data
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)
# for incident in incident_data:
#     for key, value in incident.items():
#         pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
#     pdf.ln(5)
# pdf_path = "incidents_2.pdf"
# pdf.output(pdf_path)


# 2. automations.csv
automation_data = pd.DataFrame([
    {
        "Automation ID": "AUTO001",
        "Automation Name": "LB Rule Checker",
        "Description": "Checks and validates load balancer rules across environments"
    },
    {
        "Automation ID": "AUTO002",
        "Automation Name": "SSL Cert Monitor",
        "Description": "Monitors SSL certificate expiry and renews them automatically"
    },
    {
        "Automation ID": "AUTO003",
        "Automation Name": "Disk Health Scanner",
        "Description": "Scans and reports health of SSDs in all storage nodes"
    },
    {
        "Automation ID": "AUTO004",
        "Automation Name": "DB Query Optimizer",
        "Description": "Analyzes and optimizes inefficient database queries"
    },
    {
        "Automation ID": "AUTO005",
        "Automation Name": "SSH Port Hardener",
        "Description": "Scans exposed SSH ports and enforces secure policies"
    },
    {
        "Automation ID": "AUTO006",
        "Automation Name": "Docker Cache Purger",
        "Description": "Identifies and clears corrupted Docker layers in registry"
    },
    {
        "Automation ID": "AUTO007",
        "Automation Name": "Alert Rule Validator",
        "Description": "Validates alert rules against metrics and suggests thresholds"
    },
    {
        "Automation ID": "AUTO008",
        "Automation Name": "VPN Path Switcher",
        "Description": "Detects flaky VPN links and reroutes traffic automatically"
    },
    {
        "Automation ID": "AUTO009",
        "Automation Name": "Write Load Balancer",
        "Description": "Defers high-volume DB writes to off-peak schedules"
    },
    {
        "Automation ID": "AUTO010",
        "Automation Name": "Backup Volume Manager",
        "Description": "Monitors backup volume usage and auto-expands or cleans old data"
    },
    {
        "Automation ID": "AUTO011",
        "Automation Name": "SMTP Config Validator",
        "Description": "Validates SMTP credentials and checks service connectivity"
    },
    {
        "Automation ID": "AUTO012",
        "Automation Name": "Kafka Retention Manager",
        "Description": "Monitors Kafka topic retention and extends policies automatically"
    },
    {
        "Automation ID": "AUTO013",
        "Automation Name": "Config Sync Enforcer",
        "Description": "Detects version mismatches in configs across environments"
    },
    {
        "Automation ID": "AUTO014",
        "Automation Name": "Memory Leak Detector",
        "Description": "Scans deployed services for abnormal memory growth and rolls back if needed"
    },
    {
        "Automation ID": "AUTO015",
        "Automation Name": "Env Scope Filter",
        "Description": "Ensures alert rules are only applied to production environments"
    }
])
automation_data.to_csv("automations_2.csv", index=False)
