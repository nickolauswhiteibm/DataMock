"""
Object-Centric Process Mining Data Generator - Complete Advanced UI
Celonis-Inspired Process Intelligence Data Generator
With BPMN Upload, Event Editing, and Industry KPIs
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import io
import json
import xml.etree.ElementTree as ET

# Session State
if 'custom_processes' not in st.session_state:
    st.session_state.custom_processes = {}
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None

# Industry KPIs
INDUSTRY_KPIS = {
    "Order to Cash (O2C)": {
        "common_issues": [
            "Long credit check delays (avg 3-5 days)",
            "Manual order confirmation bottleneck",
            "Shipping delays due to picking inefficiencies",
            "Late payment collection (30+ days overdue)",
            "High order cancellation rate (15-20%)"
        ],
        "kpis": {
            "Avg Order Processing Time": "5.2 days",
            "On-Time Delivery Rate": "78%",
            "Order Accuracy": "92%",
            "Days Sales Outstanding (DSO)": "45 days",
            "Order Cancellation Rate": "18%",
            "Perfect Order Rate": "71%",
            "Cash Conversion Cycle": "52 days",
            "Order Fill Rate": "89%"
        }
    },
    "Purchase to Pay (P2P)": {
        "common_issues": [
            "Purchase requisition approval delays (avg 7 days)",
            "Invoice matching errors (3-way match failures)",
            "Maverick spending (30% off-contract)",
            "Duplicate invoice payments",
            "Vendor payment delays causing relationship issues"
        ],
        "kpis": {
            "Avg P2P Cycle Time": "28 days",
            "Invoice Processing Cost": "$15.50",
            "3-Way Match Success Rate": "73%",
            "On-Time Payment Rate": "65%",
            "Maverick Spend": "32%",
            "PO Compliance Rate": "68%",
            "Early Payment Discount Capture": "41%",
            "Supplier Satisfaction Score": "3.2/5"
        }
    },
    "Procurement": {
        "common_issues": [
            "Budget approval bottlenecks (multiple approval layers)",
            "Vendor selection delays (avg 14 days)",
            "Contract negotiation taking too long",
            "Emergency purchases bypassing process (25%)",
            "Poor vendor performance tracking"
        ],
        "kpis": {
            "Avg Procurement Cycle Time": "35 days",
            "Cost Savings Achieved": "8.5%",
            "Vendor On-Time Delivery": "82%",
            "Emergency Purchase Rate": "24%",
            "Contract Compliance": "71%",
            "Sourcing Efficiency": "76%",
            "Supplier Quality Rating": "3.8/5",
            "Procurement ROI": "4.2x"
        }
    },
    "Finance Operations": {
        "common_issues": [
            "Manual data entry errors (12% error rate)",
            "Multi-level approval delays",
            "Payment scheduling inefficiencies",
            "Reconciliation discrepancies",
            "Late invoice processing penalties"
        ],
        "kpis": {
            "Avg Invoice Processing Time": "12 days",
            "Invoice Error Rate": "11%",
            "Straight-Through Processing": "45%",
            "Early Payment Discount Capture": "23%",
            "Reconciliation Time": "8 days",
            "Payment Accuracy": "94%",
            "Cost per Invoice": "$12.80",
            "Automation Rate": "38%"
        }
    },
    "BPO Operations": {
        "common_issues": [
            "Long first response time (avg 4 hours)",
            "Multiple agent handoffs (avg 2.3 per ticket)",
            "SLA breaches (35% of tickets)",
            "Customer escalations due to delays",
            "Inconsistent resolution quality"
        ],
        "kpis": {
            "Avg Resolution Time": "18 hours",
            "First Contact Resolution": "58%",
            "SLA Compliance": "67%",
            "Customer Satisfaction": "3.4/5",
            "Agent Utilization": "73%",
            "Escalation Rate": "22%",
            "Avg Handle Time": "12 min",
            "Net Promoter Score": "32"
        }
    }
}

BUSINESS_PROCESSES = {
    "Order to Cash (O2C)": {
        "case_table": "Sales Orders",
        "case_id_prefix": "SO",
        "activities": [
            "Order Created", "Credit Check", "Order Confirmed", 
            "Picking Started", "Goods Packed", "Goods Shipped",
            "Invoice Created", "Payment Received", "Order Closed"
        ],
        "case_attributes": ["customer_id", "order_value", "currency", "sales_rep", "region", "priority"],
        "activity_attributes": ["resource", "department", "system", "cost"]
    },
    "Purchase to Pay (P2P)": {
        "case_table": "Purchase Orders",
        "case_id_prefix": "PO",
        "activities": [
            "PR Created", "PR Approved", "PO Created", "PO Sent to Vendor",
            "Goods Received", "GR Posted", "Invoice Received", 
            "Invoice Matched", "Payment Released", "PO Closed"
        ],
        "case_attributes": ["vendor_id", "po_value", "currency", "buyer", "category", "urgency"],
        "activity_attributes": ["resource", "department", "approval_level", "cost"]
    },
    "Procurement": {
        "case_table": "Requisitions",
        "case_id_prefix": "REQ",
        "activities": [
            "Requisition Created", "Budget Check", "Manager Approval",
            "Procurement Review", "Vendor Selection", "Contract Negotiation",
            "PO Generation", "Delivery Scheduled", "Goods Received", "Requisition Closed"
        ],
        "case_attributes": ["requester_id", "department", "budget_code", "item_category", "total_value"],
        "activity_attributes": ["resource", "approval_tier", "vendor_id", "lead_time"]
    },
    "Finance Operations": {
        "case_table": "Invoices",
        "case_id_prefix": "INV",
        "activities": [
            "Invoice Received", "Data Entry", "Validation Check",
            "Approval Level 1", "Approval Level 2", "Payment Scheduled",
            "Payment Executed", "Reconciliation", "Invoice Archived"
        ],
        "case_attributes": ["vendor_id", "invoice_amount", "currency", "payment_terms", "gl_account"],
        "activity_attributes": ["resource", "approval_status", "payment_method", "processing_time"]
    },
    "BPO Operations": {
        "case_table": "Service Tickets",
        "case_id_prefix": "TKT",
        "activities": [
            "Ticket Created", "Initial Assessment", "Assigned to Agent",
            "Investigation Started", "Customer Contacted", "Solution Proposed",
            "Solution Implemented", "Quality Check", "Customer Confirmation", "Ticket Closed"
        ],
        "case_attributes": ["customer_id", "service_type", "priority", "channel", "sla_hours"],
        "activity_attributes": ["agent_id", "team", "resolution_category", "customer_satisfaction"]
    }
}

DATA_QUALITY_ISSUES = {
    "Missing Activities": {"description": "Some cases skip critical activities", "severity": "🔴 High", "code": "1"},
    "Duplicate Activities": {"description": "Activities recorded multiple times", "severity": "🟡 Medium", "code": "2"},
    "Out of Sequence": {"description": "Activities occur in wrong order", "severity": "🔴 High", "code": "3"},
    "Long Waiting Times": {"description": "Unusual delays between activities", "severity": "🟡 Medium", "code": "4"},
    "Rework Loops": {"description": "Activities repeated due to errors", "severity": "🔴 High", "code": "5"},
    "Missing Case Attributes": {"description": "Incomplete case information", "severity": "🟢 Low", "code": "6"},
    "Inconsistent Timestamps": {"description": "Timestamp anomalies", "severity": "🟡 Medium", "code": "7"},
    "Orphaned Events": {"description": "Events without corresponding cases", "severity": "🔴 High", "code": "8"}
}

class BPMNParser:
    @staticmethod
    def parse_bpmn(file_content: bytes) -> Dict:
        try:
            root = ET.fromstring(file_content)
            namespaces = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
            
            activities = []
            process_name = "Imported Process"
            
            process_elem = root.find('.//bpmn:process', namespaces)
            if process_elem is not None and 'name' in process_elem.attrib:
                process_name = process_elem.attrib['name']
            
            for task_type in ['task', 'userTask', 'serviceTask', 'manualTask', 'scriptTask']:
                for task in root.findall(f'.//bpmn:{task_type}', namespaces):
                    if 'name' in task.attrib:
                        activities.append(task.attrib['name'])
            
            if not activities:
                for task in root.findall('.//task'):
                    if 'name' in task.attrib:
                        activities.append(task.attrib['name'])
            
            return {'name': process_name, 'activities': activities, 'success': len(activities) > 0}
        except Exception as e:
            return {'name': 'Error', 'activities': [], 'success': False, 'error': str(e)}

class OCPMDataGenerator:
    def __init__(self, num_cases: int, process_config: Dict, issues: List[str]):
        self.num_cases = num_cases
        self.process_config = process_config
        self.issues = issues
        self.case_df = None
        self.event_df = None
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2024, 12, 31)
        
    def generate_case_id(self, index: int) -> str:
        return f"{self.process_config['case_id_prefix']}-{str(index + 1).zfill(6)}"
    
    def generate_timestamp(self, base_date: datetime, add_hours: int = 0) -> datetime:
        timestamp = base_date + timedelta(hours=add_hours)
        timestamp += timedelta(hours=random.randint(0, 8), minutes=random.randint(0, 59))
        return timestamp
    
    def generate_case_table(self) -> pd.DataFrame:
        cases = []
        for i in range(self.num_cases):
            case_id = self.generate_case_id(i)
            case_start = self.start_date + timedelta(days=random.randint(0, (self.end_date - self.start_date).days))
            
            case = {
                "case_id": case_id,
                "case_start_date": case_start,
                "case_status": random.choice(["Completed", "In Progress", "Completed", "Completed", "Cancelled"])
            }
            
            for attr in self.process_config.get("case_attributes", []):
                if "customer_id" in attr:
                    case[attr] = f"CUST-{random.randint(1000, 9999)}"
                elif "vendor_id" in attr:
                    case[attr] = f"VEND-{random.randint(100, 999)}"
                elif "value" in attr or "amount" in attr:
                    case[attr] = round(random.uniform(100, 50000), 2)
                elif "currency" in attr:
                    case[attr] = random.choice(["USD", "EUR", "GBP", "USD", "USD"])
                elif "region" in attr:
                    case[attr] = random.choice(["North America", "Europe", "Asia Pacific", "Latin America"])
                elif "priority" in attr:
                    case[attr] = random.choice(["Low", "Medium", "High", "Medium", "Low"])
                else:
                    case[attr] = f"{attr.upper()}-{random.randint(100, 999)}"
            
            cases.append(case)
        
        self.case_df = pd.DataFrame(cases)
        if "6" in self.issues:
            self._inject_missing_attributes()
        return self.case_df
    
    def generate_event_log(self) -> pd.DataFrame:
        events = []
        event_id = 1
        
        for _, case in self.case_df.iterrows():
            case_id = case["case_id"]
            current_time = case["case_start_date"]
            activities = self.process_config["activities"].copy()
            
            if "1" in self.issues and random.random() < 0.15:
                skip_count = random.randint(1, 2)
                for _ in range(skip_count):
                    if len(activities) > 3:
                        activities.pop(random.randint(1, len(activities) - 2))
            
            for idx, activity in enumerate(activities):
                hours_gap = random.randint(48, 240) if "4" in self.issues and random.random() < 0.1 else random.randint(1, 48)
                current_time = self.generate_timestamp(current_time, hours_gap)
                
                event = {
                    "event_id": f"EVT-{str(event_id).zfill(8)}",
                    "case_id": case_id,
                    "activity": activity,
                    "timestamp": current_time,
                    "resource": random.choice(["System", "John Doe", "Jane Smith", "Bob Johnson", "Alice Williams"])
                }
                
                for attr in self.process_config.get("activity_attributes", []):
                    if "department" in attr:
                        event[attr] = random.choice(["Finance", "Operations", "Procurement", "Sales", "IT"])
                    elif "cost" in attr:
                        event[attr] = round(random.uniform(10, 500), 2)
                    else:
                        event[attr] = f"{attr.upper()}-{random.randint(1, 99)}"
                
                events.append(event)
                event_id += 1
                
                if "2" in self.issues and random.random() < 0.08:
                    duplicate_event = event.copy()
                    duplicate_event["event_id"] = f"EVT-{str(event_id).zfill(8)}"
                    duplicate_event["timestamp"] = current_time + timedelta(minutes=random.randint(1, 30))
                    events.append(duplicate_event)
                    event_id += 1
                
                if "5" in self.issues and random.random() < 0.12 and idx > 0:
                    rework_event = events[-2].copy() if len(events) > 1 else event.copy()
                    rework_event["event_id"] = f"EVT-{str(event_id).zfill(8)}"
                    rework_event["timestamp"] = current_time + timedelta(hours=random.randint(1, 24))
                    rework_event["activity"] = f"{rework_event['activity']} (Rework)"
                    events.append(rework_event)
                    event_id += 1
        
        self.event_df = pd.DataFrame(events)
        
        if "3" in self.issues:
            self._inject_out_of_sequence()
        if "7" in self.issues:
            self._inject_timestamp_anomalies()
        if "8" in self.issues:
            self._inject_orphaned_events()
        
        return self.event_df
    
    def _inject_missing_attributes(self):
        num_nulls = int(self.num_cases * 0.05)
        for col in self.case_df.columns:
            if col not in ["case_id", "case_start_date"]:
                null_indices = random.sample(range(len(self.case_df)), min(num_nulls, len(self.case_df)))
                self.case_df.loc[null_indices, col] = np.nan
    
    def _inject_out_of_sequence(self):
        case_groups = self.event_df.groupby("case_id")
        affected_cases = random.sample(list(case_groups.groups.keys()), int(len(case_groups) * 0.1))
        for case_id in affected_cases:
            case_events = self.event_df[self.event_df["case_id"] == case_id].index.tolist()
            if len(case_events) > 2:
                idx1, idx2 = random.sample(case_events, 2)
                temp = self.event_df.loc[idx1, "timestamp"]
                self.event_df.loc[idx1, "timestamp"] = self.event_df.loc[idx2, "timestamp"]
                self.event_df.loc[idx2, "timestamp"] = temp
    
    def _inject_timestamp_anomalies(self):
        num_anomalies = int(len(self.event_df) * 0.03)
        anomaly_indices = random.sample(range(len(self.event_df)), num_anomalies)
        for idx in anomaly_indices:
            if random.choice(["future", "weekend"]) == "future":
                self.event_df.loc[idx, "timestamp"] = datetime.now() + timedelta(days=random.randint(1, 30))
    
    def _inject_orphaned_events(self):
        num_orphans = int(len(self.event_df) * 0.02)
        for _ in range(num_orphans):
            orphan_event = {
                "event_id": f"EVT-{str(len(self.event_df) + 1).zfill(8)}",
                "case_id": f"{self.process_config['case_id_prefix']}-999999",
                "activity": random.choice(self.process_config["activities"]),
                "timestamp": self.start_date + timedelta(days=random.randint(0, 365)),
                "resource": "Unknown"
            }
            self.event_df = pd.concat([self.event_df, pd.DataFrame([orphan_event])], ignore_index=True)
    
    def validate_and_clean(self) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
        stats = {
            "initial_cases": len(self.case_df),
            "initial_events": len(self.event_df),
            "duplicate_cases": 0,
            "duplicate_events": 0,
            "orphaned_events": 0,
            "cases_without_events": 0
        }
        
        self.case_df = self.case_df.drop_duplicates(subset=["case_id"], keep="first")
        self.event_df = self.event_df.drop_duplicates(subset=["event_id"], keep="first")
        
        valid_case_ids = set(self.case_df["case_id"])
        orphaned = self.event_df[~self.event_df["case_id"].isin(valid_case_ids)]
        stats["orphaned_events"] = len(orphaned)
        
        if len(orphaned) > 0 and "8" not in self.issues:
            self.event_df = self.event_df[self.event_df["case_id"].isin(valid_case_ids)]
        
        cases_with_events = set(self.event_df["case_id"])
        self.case_df = self.case_df[self.case_df["case_id"].isin(cases_with_events)]
        
        self.event_df = self.event_df.sort_values(["case_id", "timestamp"]).reset_index(drop=True)
        
        stats["final_cases"] = len(self.case_df)
        stats["final_events"] = len(self.event_df)
        
        return self.case_df, self.event_df, stats

def create_enhanced_visualizations(event_df: pd.DataFrame, case_df: pd.DataFrame, process_name: str):
    """Create comprehensive visualizations with matplotlib"""
    
    # Calculate comprehensive metrics
    case_times = event_df.groupby('case_id').agg({'timestamp': ['min', 'max']})
    case_times.columns = ['start', 'end']
    case_times['throughput_hours'] = (case_times['end'] - case_times['start']).dt.total_seconds() / 3600
    case_times['throughput_days'] = (case_times['throughput_hours'] / 24).round(0).astype(int)
    
    activity_counts = event_df['activity'].value_counts()
    rework_cases = event_df[event_df['activity'].str.contains('Rework', na=False)]['case_id'].nunique()
    
    # Resource analysis
    resource_counts = event_df['resource'].value_counts()
    resource_workload = event_df.groupby('resource').size()
    
    # Time-based analysis
    event_df['hour'] = pd.to_datetime(event_df['timestamp']).dt.hour
    event_df['day_of_week'] = pd.to_datetime(event_df['timestamp']).dt.day_name()
    event_df['month'] = pd.to_datetime(event_df['timestamp']).dt.to_period('M').astype(str)
    
    # Bottleneck detection
    event_df_sorted = event_df.sort_values(['case_id', 'timestamp'])
    event_df_sorted['time_since_last'] = event_df_sorted.groupby('case_id')['timestamp'].diff().dt.total_seconds() / 3600
    bottlenecks = event_df_sorted.groupby('activity')['time_since_last'].mean().sort_values(ascending=False).head(5)
    
    industry_info = INDUSTRY_KPIS.get(process_name, {})
    
    # Layout: KPI cards
    st.subheader("📊 Comprehensive Process Intelligence Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        avg_throughput = case_times['throughput_days'].mean()
        st.metric("Avg Throughput", f"{avg_throughput:.1f} days", 
                 delta=f"{case_times['throughput_days'].std():.1f}d std")
    
    with col2:
        rework_rate = (rework_cases / len(case_df)) * 100 if len(case_df) > 0 else 0
        st.metric("Rework Rate", f"{rework_rate:.1f}%", 
                 delta=f"{rework_cases} cases", delta_color="inverse")
    
    with col3:
        completed_cases = len(case_df[case_df['case_status'] == 'Completed'])
        completion_rate = (completed_cases / len(case_df)) * 100 if len(case_df) > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%", 
                 delta=f"{completed_cases}/{len(case_df)}")
    
    with col4:
        avg_events_per_case = len(event_df) / len(case_df) if len(case_df) > 0 else 0
        st.metric("Avg Events/Case", f"{avg_events_per_case:.1f}",
                 delta=f"{len(event_df)} total")
    
    with col5:
        unique_resources = event_df['resource'].nunique()
        avg_load = len(event_df) / unique_resources if unique_resources > 0 else 0
        st.metric("Resource Utilization", f"{unique_resources} resources",
                 delta=f"{avg_load:.0f} events/resource")
    
    st.markdown("---")
    
    # Row 1: Activity Analysis and Bottlenecks
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Activity Frequency Analysis")
        top_activities = activity_counts.head(10)
        st.write("**Top 10 Most Frequent Activities:**")
        for idx, (activity, count) in enumerate(top_activities.items(), 1):
            st.write(f"{idx}. {activity}: {count} occurrences")
    
    with col2:
        st.subheader("⚠️ Bottleneck Detection")
        st.write("**Top 5 Bottleneck Activities (Avg Wait Time):**")
        for idx, (activity, hours) in enumerate(bottlenecks.items(), 1):
            st.write(f"{idx}. {activity}: {hours:.1f} hours")
    
    # Row 2: Throughput and Resource Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Throughput Time Distribution")
        median_val = case_times['throughput_days'].median()
        mean_val = case_times['throughput_days'].mean()
        min_val = case_times['throughput_days'].min()
        max_val = case_times['throughput_days'].max()
        st.write(f"**Statistics:**")
        st.write(f"- Median: {median_val:.1f} days")
        st.write(f"- Mean: {mean_val:.1f} days")
        st.write(f"- Min: {min_val:.1f} days")
        st.write(f"- Max: {max_val:.1f} days")
        st.bar_chart(case_times['throughput_days'].value_counts().sort_index().head(20))
    
    with col2:
        st.subheader("👥 Resource Workload Analysis")
        st.write("**Event Distribution by Resource:**")
        for resource, count in resource_workload.items():
            percentage = (count / resource_workload.sum()) * 100
            st.write(f"- {resource}: {count} events ({percentage:.1f}%)")
    
    # Row 3: Time-based Trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Activity by Day of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = event_df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
        st.bar_chart(day_counts)
    
    with col2:
        st.subheader("🕐 Hourly Activity Pattern")
        hour_counts = event_df['hour'].value_counts().sort_index()
        st.line_chart(hour_counts)
    
    # Row 4: Monthly Trends and Industry KPIs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📈 Monthly Activity Trends")
        month_counts = event_df['month'].value_counts().sort_index()
        st.area_chart(month_counts)
    
    with col2:
        st.subheader("🎯 Industry Benchmarks")
        if industry_info.get('kpis'):
            kpi_df = pd.DataFrame(list(industry_info['kpis'].items()), columns=['KPI', 'Benchmark'])
            st.dataframe(kpi_df, hide_index=True, use_container_width=True, height=350)
        else:
            st.info("No industry benchmarks available for this process")
    
    # Row 5: Common Issues
    if industry_info.get('common_issues'):
        st.subheader("🔴 Common Process Issues & Recommendations")
        issue_cols = st.columns(2)
        for idx, issue in enumerate(industry_info['common_issues']):
            with issue_cols[idx % 2]:
                st.warning(f"**Issue {idx+1}:** {issue}")

def main():
    st.set_page_config(page_title="OCPM Data Generator", page_icon="📊", layout="wide")
    
    st.title("📊 Object-Centric Process Mining Data Generator")
    st.markdown("*Celonis-Inspired Process Intelligence Data Generator with Advanced Analytics*")
    st.markdown("---")
    
    tabs = st.tabs(["🚀 Generate Data", "✏️ Edit Events & Processes", "📚 Process Library"])
    
    # TAB 1: GENERATE DATA
    with tabs[0]:
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.header("⚙️ Configuration")
            
            st.subheader("1️⃣ Select Process")
            all_processes = {**BUSINESS_PROCESSES, **st.session_state.custom_processes}
            process_name = st.selectbox("Process Type", options=list(all_processes.keys()))
            
            if process_name in all_processes:
                process_info = all_processes[process_name]
                with st.expander("📋 Process Details"):
                    st.write(f"**Case Table:** {process_info.get('case_table', 'N/A')}")
                    st.write(f"**Case ID Prefix:** {process_info.get('case_id_prefix', 'N/A')}")
                    st.write(f"**Activities ({len(process_info.get('activities', []))}):**")
                    for i, act in enumerate(process_info.get('activities', []), 1):
                        st.write(f"{i}. {act}")
            
            st.subheader("2️⃣ Data Size")
            size_option = st.radio("Select Size", ["Small (100)", "Medium (500)", "Large (1,000)", "Extra Large (5,000)", "Custom"])
            
            if size_option == "Custom":
                num_cases = st.number_input("Number of Cases", min_value=10, max_value=10000, value=250, step=50)
            else:
                size_map = {"Small (100)": 100, "Medium (500)": 500, "Large (1,000)": 1000, "Extra Large (5,000)": 5000}
                num_cases = size_map[size_option]
            
            st.subheader("3️⃣ Data Quality Issues")
            selected_issues = []
            for issue_name, issue_info in DATA_QUALITY_ISSUES.items():
                if st.checkbox(f"{issue_info['severity']} {issue_name}", help=issue_info['description'], key=f"issue_{issue_info['code']}"):
                    selected_issues.append(issue_info['code'])
            
            st.markdown("---")
            generate_button = st.button("🚀 Generate Data", type="primary", use_container_width=True)
        
        with col_right:
            if generate_button:
                with st.spinner("🔄 Generating data..."):
                    process_config = all_processes[process_name]
                    generator = OCPMDataGenerator(num_cases, process_config, selected_issues)
                    case_df = generator.generate_case_table()
                    event_df = generator.generate_event_log()
                    case_df, event_df, stats = generator.validate_and_clean()
                    
                    st.session_state.generated_data = {
                        'case_df': case_df, 'event_df': event_df, 'stats': stats,
                        'process_config': process_config, 'process_name': process_name
                    }
                st.success("✅ Data generation complete!")
            
            if st.session_state.generated_data is not None:
                data = st.session_state.generated_data
                case_df, event_df = data['case_df'], data['event_df']
                stats, process_config = data['stats'], data['process_config']
                process_name = data['process_name']
                
                st.subheader("📊 Generation Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Cases", stats["final_cases"])
                with col2:
                    st.metric("Total Events", stats["final_events"])
                with col3:
                    st.metric("Avg Events/Case", f"{stats['final_events'] / stats['final_cases']:.1f}")
                with col4:
                    st.metric("Issues Injected", len(selected_issues))
                
                st.markdown("---")
                create_enhanced_visualizations(event_df, case_df, process_name)
                st.markdown("---")
                
                # CASE TABLE WITH FILTERING
                st.subheader("📋 Case Table Preview")
                
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    case_search = st.text_input("🔍 Search Cases", placeholder="Search by Case ID, Customer, etc.", key="case_search")
                with col2:
                    if 'case_status' in case_df.columns:
                        status_filter = st.multiselect("Filter by Status", options=case_df['case_status'].unique(), key="status_filter")
                    else:
                        status_filter = []
                with col3:
                    case_limit = st.number_input("Rows to show", min_value=5, max_value=100, value=10, step=5, key="case_limit")
                
                # Apply filters
                filtered_case_df = case_df.copy()
                if case_search:
                    mask = filtered_case_df.astype(str).apply(lambda x: x.str.contains(case_search, case=False, na=False)).any(axis=1)
                    filtered_case_df = filtered_case_df[mask]
                if status_filter:
                    filtered_case_df = filtered_case_df[filtered_case_df['case_status'].isin(status_filter)]
                
                st.caption(f"Showing {min(case_limit, len(filtered_case_df))} of {len(filtered_case_df)} cases (filtered from {len(case_df)} total)")
                st.dataframe(filtered_case_df.head(case_limit), use_container_width=True)
                
                # EVENT LOG WITH FILTERING
                st.subheader("📋 Event Log Preview")
                
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    event_search = st.text_input("🔍 Search Events", placeholder="Search by Activity, Resource, etc.", key="event_search")
                with col2:
                    if 'activity' in event_df.columns:
                        activity_filter = st.multiselect("Filter by Activity", options=sorted(event_df['activity'].unique()), key="activity_filter")
                    else:
                        activity_filter = []
                with col3:
                    if 'resource' in event_df.columns:
                        resource_filter = st.multiselect("Filter by Resource", options=sorted(event_df['resource'].unique()), key="resource_filter")
                    else:
                        resource_filter = []
                with col4:
                    event_limit = st.number_input("Rows to show", min_value=5, max_value=200, value=20, step=10, key="event_limit")
                
                # Apply filters
                filtered_event_df = event_df.copy()
                if event_search:
                    mask = filtered_event_df.astype(str).apply(lambda x: x.str.contains(event_search, case=False, na=False)).any(axis=1)
                    filtered_event_df = filtered_event_df[mask]
                if activity_filter:
                    filtered_event_df = filtered_event_df[filtered_event_df['activity'].isin(activity_filter)]
                if resource_filter:
                    filtered_event_df = filtered_event_df[filtered_event_df['resource'].isin(resource_filter)]
                
                st.caption(f"Showing {min(event_limit, len(filtered_event_df))} of {len(filtered_event_df)} events (filtered from {len(event_df)} total)")
                st.dataframe(filtered_event_df.head(event_limit), use_container_width=True)
                
                st.subheader("💾 Download Data")
                col1, col2 = st.columns(2)
                
                with col1:
                    case_buffer = io.BytesIO()
                    with pd.ExcelWriter(case_buffer, engine='openpyxl') as writer:
                        case_df.to_excel(writer, sheet_name='Cases', index=False)
                    case_buffer.seek(0)
                    st.download_button("📥 Download Case Table (Excel)", data=case_buffer,
                                     file_name=f"ocpm_cases_{process_config['case_id_prefix'].lower()}.xlsx",
                                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                     use_container_width=True)
                
                with col2:
                    event_buffer = io.BytesIO()
                    with pd.ExcelWriter(event_buffer, engine='openpyxl') as writer:
                        event_df.to_excel(writer, sheet_name='Events', index=False)
                    event_buffer.seek(0)
                    st.download_button("📥 Download Event Log (Excel)", data=event_buffer,
                                     file_name=f"ocpm_events_{process_config['case_id_prefix'].lower()}.xlsx",
                                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                     use_container_width=True)
            else:
                st.info("👈 Configure settings and click 'Generate Data' to begin!")
    
    # TAB 2: EDIT EVENTS & PROCESSES
    with tabs[1]:
        st.header("✏️ Event & Process Management")
        st.markdown("*Create custom processes, upload BPMN diagrams, and edit event sequences*")
        
        st.subheader("📤 Quick Process Creation")
        
        creation_tabs = st.tabs(["📝 Manual Entry", "📄 BPMN Upload"])
        
        with creation_tabs[0]:
            st.markdown("### Create a New Process Manually")
            
            with st.form("create_process_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_process_name = st.text_input("Process Name*", placeholder="e.g., Customer Onboarding")
                    new_case_table = st.text_input("Case Table Name*", placeholder="e.g., Onboarding Cases")
                
                with col2:
                    new_case_prefix = st.text_input("Case ID Prefix* (max 5 chars)", placeholder="e.g., ONB", max_chars=5)
                    num_activities = st.number_input("Number of Activities", min_value=3, max_value=20, value=5)
                
                st.markdown("**Define Your Event Sequence:**")
                st.info("💡 Tip: Enter activities in the order they should occur in your process")
                
                activities_input = []
                cols = st.columns(2)
                for i in range(num_activities):
                    with cols[i % 2]:
                        activity = st.text_input(f"Activity {i+1}*", key=f"new_act_{i}", 
                                               placeholder=f"e.g., Step {i+1}")
                        activities_input.append(activity)
                
                submit_button = st.form_submit_button("✅ Create Process", type="primary", use_container_width=True)
                
                if submit_button:
                    activities = [act.strip() for act in activities_input if act.strip()]
                    
                    if new_process_name and new_case_table and new_case_prefix and len(activities) >= 3:
                        process_config = {
                            'case_table': new_case_table,
                            'case_id_prefix': new_case_prefix.upper(),
                            'activities': activities,
                            'case_attributes': ['customer_id', 'value', 'status', 'priority'],
                            'activity_attributes': ['resource', 'department', 'duration']
                        }
                        st.session_state.custom_processes[new_process_name] = process_config
                        st.success(f"✅ Process '{new_process_name}' created with {len(activities)} activities!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields and provide at least 3 activities")
        
        with creation_tabs[1]:
            st.markdown("### Upload BPMN Diagram")
            uploaded_file = st.file_uploader("Upload BPMN XML file", type=['bpmn', 'xml'], 
                                            help="Upload a BPMN 2.0 XML file to automatically extract activities")
            
            if uploaded_file is not None:
                file_content = uploaded_file.read()
                result = BPMNParser.parse_bpmn(file_content)
                
                if result['success']:
                    st.success(f"✅ Successfully parsed: **{result['name']}**")
                    st.write(f"**Found {len(result['activities'])} activities:**")
                    
                    for i, activity in enumerate(result['activities'], 1):
                        st.write(f"{i}. {activity}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        custom_name = st.text_input("Customize Process Name", value=result['name'])
                    with col2:
                        custom_prefix = st.text_input("Customize Case ID Prefix", value=result['name'][:3].upper(), max_chars=5)
                    
                    if st.button("➕ Create Process from BPMN", type="primary", use_container_width=True):
                        process_config = {
                            'case_table': f"{custom_name} Cases"
,
                            'case_id_prefix': custom_prefix.upper(),
                            'activities': result['activities'],
                            'case_attributes': ['customer_id', 'value', 'status'],
                            'activity_attributes': ['resource', 'department']
                        }
                        st.session_state.custom_processes[custom_name] = process_config
                        st.success(f"✅ Process '{custom_name}' created from BPMN!")
                        st.rerun()
                else:
                    st.error(f"❌ Failed to parse BPMN: {result.get('error', 'Unknown error')}")
        
        st.markdown("---")
        st.subheader("📚 Manage Your Custom Processes")
        
        if len(st.session_state.custom_processes) == 0:
            st.info("🎯 No custom processes yet. Create one above to get started!")
        else:
            for proc_name, proc_config in st.session_state.custom_processes.items():
                with st.expander(f"✏️ **{proc_name}** ({len(proc_config.get('activities', []))} activities)", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("#### 📝 Edit Event Sequence")
                        st.info("💡 Modify the activities below. Each line represents one event in your process flow.")
                        
                        activities_str = '\n'.join(proc_config.get('activities', []))
                        edited_activities = st.text_area(
                            "Event Sequence (one per line)",
                            value=activities_str,
                            height=250,
                            key=f"edit_{proc_name}",
                            help="Add, remove, or reorder activities. Each line is one step in the process.",
                            label_visibility="collapsed"
                        )
                        
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            if st.button("💾 Save Changes", key=f"save_{proc_name}", type="primary", use_container_width=True):
                                new_activities = [act.strip() for act in edited_activities.split('\n') if act.strip()]
                                if len(new_activities) > 0:
                                    proc_config['activities'] = new_activities
                                    st.session_state.custom_processes[proc_name] = proc_config
                                    st.success(f"✅ Saved {len(new_activities)} activities!")
                                    st.rerun()
                                else:
                                    st.error("❌ Must have at least one activity")
                        
                        with col_b:
                            if st.button("↩️ Reset", key=f"reset_{proc_name}", use_container_width=True):
                                st.rerun()
                        
                        with col_c:
                            if st.button("🗑️ Delete Process", key=f"delete_{proc_name}", use_container_width=True):
                                del st.session_state.custom_processes[proc_name]
                                st.success("✅ Process deleted!")
                                st.rerun()
                    
                    with col2:
                        st.markdown("#### ℹ️ Process Info")
                        st.write(f"**Case Table:** {proc_config.get('case_table', 'N/A')}")
                        st.write(f"**Case ID Prefix:** {proc_config.get('case_id_prefix', 'N/A')}")
                        st.write(f"**Total Activities:** {len(proc_config.get('activities', []))}")
                        
                        st.markdown("**Case Attributes:**")
                        for attr in proc_config.get('case_attributes', []):
                            st.write(f"• {attr}")
                        
                        st.markdown("**Activity Attributes:**")
                        for attr in proc_config.get('activity_attributes', []):
                            st.write(f"• {attr}")
            
            st.markdown("---")
            st.subheader("💾 Import/Export")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if len(st.session_state.custom_processes) > 0:
                    export_json = json.dumps(st.session_state.custom_processes, indent=2)
                    st.download_button("📥 Export All Custom Processes (JSON)", data=export_json,
                                     file_name="custom_processes.json", mime="application/json",
                                     use_container_width=True)
            
            with col2:
                import_file = st.file_uploader("Import Custom Processes (JSON)", type=['json'])
                if import_file is not None:
                    try:
                        json_content = import_file.read().decode('utf-8')
                        processes = json.loads(json_content)
                        st.session_state.custom_processes.update(processes)
                        st.success("✅ Custom processes imported successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error importing: {str(e)}")
    
    # TAB 3: PROCESS LIBRARY
    with tabs[2]:
        st.header("📚 Process Library")
        st.markdown("*All available processes - both standard and custom*")
        
        all_processes = {**BUSINESS_PROCESSES, **st.session_state.custom_processes}
        
        for proc_name, proc_config in all_processes.items():
            is_custom = proc_name in st.session_state.custom_processes
            icon = "🔧" if is_custom else "📦"
            
            with st.expander(f"{icon} {proc_name}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Type:** {'Custom Process' if is_custom else 'Standard Process'}")
                    st.write(f"**Case Table:** {proc_config.get('case_table', 'N/A')}")
                    st.write(f"**Case ID Prefix:** {proc_config.get('case_id_prefix', 'N/A')}")
                    st.write(f"**Number of Activities:** {len(proc_config.get('activities', []))}")
                    
                    st.write("**Activity Sequence:**")
                    for i, activity in enumerate(proc_config.get('activities', []), 1):
                        st.write(f"{i}. {activity}")
                
                with col2:
                    st.write("**Case Attributes:**")
                    for attr in proc_config.get('case_attributes', []):
                        st.write(f"• {attr}")
                    
                    st.write("**Activity Attributes:**")
                    for attr in proc_config.get('activity_attributes', []):
                        st.write(f"• {attr}")

if __name__ == "__main__":
    main()
