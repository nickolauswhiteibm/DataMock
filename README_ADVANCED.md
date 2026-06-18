# Object-Centric Process Mining Data Generator - Advanced Edition

**Celonis-Inspired Process Intelligence Data Generator with BPMN Support**

A comprehensive web application for generating realistic process mining data with advanced features including BPMN diagram upload, custom process creation, and event sequence management.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
cd C:\Users\NickolausWhite\Desktop\datamock
python -m streamlit run app_advanced.py
```

The application will open at `http://localhost:8501`

## ✨ New Advanced Features

### 1. 📤 BPMN Diagram Upload
- **Upload BPMN 2.0 XML files** directly into the application
- **Automatic activity extraction** from BPMN tasks
- **Instant process creation** from uploaded diagrams
- **Supports multiple BPMN task types**: Task, UserTask, ServiceTask, ManualTask, ScriptTask

### 2. 🔧 Custom Process Builder
- **Manual process creation** with text input
- **Edit existing processes** in real-time
- **Add/remove activities** dynamically
- **Custom case and activity attributes**

### 3. 📚 Process Library
- **Unified view** of all standard and custom processes
- **Detailed process information** including activity sequences
- **Quick access** to process configurations
- **Visual distinction** between standard and custom processes

### 4. 💾 Import/Export Functionality
- **Export custom processes** as JSON
- **Import process libraries** from JSON files
- **Share configurations** across teams
- **Backup and restore** custom processes

### 5. 🎯 Enhanced UI/UX
- **Three-tab interface**: Generate Data, Custom Processes, Process Library
- **Real-time editing** of process activities
- **Persistent session state** for custom processes
- **Intuitive process management** with expandable cards

## 📋 Application Structure

### Tab 1: 🚀 Generate Data
The main data generation interface with:
- Process selection (standard + custom)
- Data size configuration
- Data quality issue selection
- Real-time data preview
- Excel download functionality

### Tab 2: 🔧 Custom Processes
Process creation and management:
- **BPMN Upload Section**: Drag and drop BPMN files
- **Manual Creation Form**: Text-based process builder
- **Process Editor**: Edit activities for existing processes
- **Import/Export**: JSON-based configuration management

### Tab 3: 📚 Process Library
Complete process catalog:
- All available processes in one view
- Detailed process specifications
- Activity sequences and attributes
- Standard vs. custom process indicators

## 🎯 Use Cases

### 1. BPMN-Based Data Generation
**Scenario**: You have a BPMN diagram from a process modeling tool

**Steps**:
1. Go to "Custom Processes" tab
2. Upload your BPMN XML file
3. Review extracted activities
4. Click "Create Process from BPMN"
5. Switch to "Generate Data" tab
6. Select your new process
7. Generate data

**Supported BPMN Tools**:
- Camunda Modeler
- Signavio
- Bizagi Modeler
- ARIS
- Any BPMN 2.0 compliant tool

### 2. Custom Process Creation
**Scenario**: You want to create a unique process not in the standard library

**Steps**:
1. Go to "Custom Processes" tab
2. Fill in the manual creation form:
   - Process Name: "Customer Onboarding"
   - Case Table: "Onboarding Cases"
   - Case ID Prefix: "ONB"
   - Activities (one per line):
     ```
     Application Received
     Document Verification
     Background Check
     Manager Approval
     Account Setup
     Welcome Email Sent
     Onboarding Complete
     ```
3. Click "Create Process"
4. Process is now available for data generation

### 3. Process Editing
**Scenario**: You need to modify an existing custom process

**Steps**:
1. Go to "Custom Processes" tab
2. Find your process in "Your Custom Processes"
3. Click to expand the process card
4. Edit activities in the text area
5. Click "Save Changes"
6. Changes are immediately available

### 4. Process Library Management
**Scenario**: Share processes with your team

**Steps**:
1. Create multiple custom processes
2. Go to "Custom Processes" tab
3. Click "Export All Custom Processes (JSON)"
4. Share the JSON file with team members
5. Team members import using "Import Custom Processes"

## 📤 BPMN Upload Guide

### Supported BPMN Elements

The parser extracts activities from these BPMN elements:
- `<bpmn:task>` - Generic tasks
- `<bpmn:userTask>` - User tasks
- `<bpmn:serviceTask>` - Service tasks
- `<bpmn:manualTask>` - Manual tasks
- `<bpmn:scriptTask>` - Script tasks

### BPMN File Requirements

**Valid BPMN 2.0 XML structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
  <process id="Process_1" name="Order Processing">
    <task id="Task_1" name="Receive Order"/>
    <userTask id="Task_2" name="Validate Order"/>
    <serviceTask id="Task_3" name="Check Inventory"/>
    <task id="Task_4" name="Ship Order"/>
  </process>
</definitions>
```

### Example BPMN Upload

1. **Export from Camunda Modeler**:
   - File → Save File As → `process.bpmn`

2. **Upload to Application**:
   - Drag and drop or click to browse
   - Application extracts: "Receive Order", "Validate Order", "Check Inventory", "Ship Order"

3. **Create Process**:
   - Click "Create Process from BPMN"
   - Process "Order Processing" is now available

## 🔧 Custom Process Configuration

### Process Structure

Each process contains:

```json
{
  "Process Name": {
    "case_table": "Case Table Name",
    "case_id_prefix": "PREFIX",
    "activities": [
      "Activity 1",
      "Activity 2",
      "Activity 3"
    ],
    "case_attributes": [
      "customer_id",
      "value",
      "status"
    ],
    "activity_attributes": [
      "resource",
      "department"
    ]
  }
}
```

### Example Custom Process

**Customer Onboarding Process:**
```json
{
  "Customer Onboarding": {
    "case_table": "Onboarding Cases",
    "case_id_prefix": "ONB",
    "activities": [
      "Application Received",
      "Document Verification",
      "Background Check",
      "Credit Check",
      "Manager Approval",
      "Account Setup",
      "Welcome Email Sent",
      "Training Scheduled",
      "Onboarding Complete"
    ],
    "case_attributes": [
      "customer_id",
      "application_value",
      "risk_level",
      "priority"
    ],
    "activity_attributes": [
      "resource",
      "department",
      "duration"
    ]
  }
}
```

## 💡 Advanced Tips

### 1. Creating Industry-Specific Processes

**Healthcare - Patient Admission:**
```
Patient Registration
Insurance Verification
Medical History Review
Doctor Assignment
Initial Assessment
Treatment Plan Created
Admission Complete
```

**Manufacturing - Production Order:**
```
Order Received
Material Planning
Production Scheduled
Manufacturing Started
Quality Check
Packaging
Shipping Prepared
Order Completed
```

**Banking - Loan Application:**
```
Application Submitted
Document Collection
Credit Score Check
Risk Assessment
Underwriter Review
Approval Decision
Contract Generation
Funds Disbursed
```

### 2. Combining BPMN with Manual Editing

1. Upload BPMN to get base structure
2. Edit activities to add detail
3. Add industry-specific steps
4. Save customized version

### 3. Creating Process Variants

**Base Process**: Standard Order to Cash
**Variant 1**: Express Order to Cash (fewer steps)
**Variant 2**: International Order to Cash (additional customs steps)

Create each as a separate custom process.

### 4. Testing Process Improvements

**Before State**: Create process with current activities
**After State**: Create process with improved activities
Generate data for both and compare metrics

## 📊 Data Generation with Custom Processes

### Standard Workflow

1. **Select Custom Process** from dropdown
2. **Configure Data Size** (100-10,000 cases)
3. **Select Data Quality Issues** to inject
4. **Generate Data**
5. **Review Preview**
6. **Download Excel Files**

### Custom Process Benefits

- **Exact Activity Match**: Activities match your real process
- **Realistic Sequences**: Events follow your defined order
- **Industry Alignment**: Process reflects your domain
- **Stakeholder Buy-in**: Uses familiar terminology

## 🔄 Import/Export Workflows

### Export Workflow

1. Create multiple custom processes
2. Go to "Custom Processes" tab
3. Click "Export All Custom Processes (JSON)"
4. Save file: `my_processes.json`
5. Share with team or backup

### Import Workflow

1. Receive JSON file from colleague
2. Go to "Custom Processes" tab
3. Click "Import Custom Processes (JSON)"
4. Select file
5. Processes are added to your library

### Merge Strategy

- **Import adds** to existing processes
- **Duplicate names** are overwritten
- **Standard processes** are never affected
- **Session state** persists until browser close

## 🎨 UI Components

### Process Cards

Each custom process displays as an expandable card:
- **Header**: Process name with icon (🔧 for custom)
- **Details**: Case table, prefix, activity count
- **Editor**: Text area for activity editing
- **Actions**: Save Changes, Delete buttons

### Activity Editor

- **Multi-line text area** for easy editing
- **One activity per line** format
- **Real-time updates** on save
- **Validation**: Ensures at least one activity

### Process Library View

- **Expandable sections** for each process
- **Two-column layout**: Details and attributes
- **Visual indicators**: Icons for standard vs. custom
- **Complete specifications**: All process information

## 🔍 Troubleshooting

### BPMN Upload Issues

**Problem**: "Failed to parse BPMN"
**Solutions**:
- Ensure file is valid BPMN 2.0 XML
- Check that tasks have `name` attributes
- Verify XML structure is well-formed
- Try exporting from BPMN tool again

**Problem**: "No activities found"
**Solutions**:
- Ensure BPMN contains task elements
- Check that tasks are named
- Verify namespace declarations
- Add activities manually after upload

### Custom Process Issues

**Problem**: Process not appearing in dropdown
**Solutions**:
- Refresh the page
- Check that process was saved
- Verify process name is unique
- Re-create the process

**Problem**: Activities not saving
**Solutions**:
- Ensure at least one activity exists
- Check for empty lines
- Click "Save Changes" button
- Refresh and try again

### Import/Export Issues

**Problem**: Import fails
**Solutions**:
- Verify JSON file format
- Check for syntax errors
- Ensure file is not corrupted
- Try exporting and re-importing

## 📈 Best Practices

### 1. Process Naming
- Use descriptive names: "Customer Onboarding" not "Process1"
- Include domain: "Healthcare - Patient Admission"
- Be consistent: Use same naming convention

### 2. Activity Naming
- Use action verbs: "Verify Documents" not "Documents"
- Be specific: "Manager Approval" not "Approval"
- Maintain sequence: Order activities logically

### 3. Process Organization
- Group related processes
- Export by domain or department
- Version control: Include dates in exports
- Document purpose in process name

### 4. Data Generation
- Start small: Test with 100 cases
- Validate output: Check activity sequences
- Iterate: Refine process based on results
- Document issues: Note data quality patterns

## 🚀 Advanced Scenarios

### Scenario 1: Multi-Department Process

**Requirement**: Create a process spanning multiple departments

**Solution**:
```
Request Submitted (Sales)
Budget Approval (Finance)
Resource Allocation (Operations)
Technical Review (IT)
Legal Review (Legal)
Final Approval (Management)
Implementation (Operations)
Completion (Sales)
```

### Scenario 2: Exception Handling

**Requirement**: Include exception paths in process

**Solution**:
```
Order Received
Validation Check
Validation Failed - Rework
Validation Passed
Processing
Quality Check
Quality Failed - Rework
Quality Passed
Shipment
```

### Scenario 3: Parallel Activities

**Requirement**: Model concurrent activities

**Solution**:
```
Application Received
Credit Check (Parallel)
Background Check (Parallel)
Reference Check (Parallel)
All Checks Complete
Decision Made
```

## 📚 Integration Examples

### With Celonis

1. Generate data using custom process
2. Export Excel files
3. Import into Celonis Data Integration
4. Create data model
5. Build process analysis

### With Process Mining Tools

**Compatible with**:
- Celonis
- UiPath Process Mining
- Signavio Process Intelligence
- Disco
- ProM
- PM4Py

**Export Format**: Standard event log structure
- Case ID
- Activity
- Timestamp
- Resource
- Additional attributes

## 🎓 Learning Path

### Beginner
1. Use standard processes
2. Generate small datasets (100 cases)
3. Explore data quality issues
4. Download and examine Excel files

### Intermediate
1. Create simple custom processes manually
2. Edit existing processes
3. Export and import configurations
4. Generate medium datasets (500 cases)

### Advanced
1. Upload BPMN diagrams
2. Create complex multi-step processes
3. Manage process libraries
4. Generate large datasets (5,000+ cases)
5. Integrate with process mining tools

## 🔐 Data Privacy & Security

- **Local Processing**: All data generated locally
- **No External Calls**: No data sent to servers
- **Session-Based**: Custom processes stored in browser session
- **Export Control**: You control all exports
- **No Tracking**: No analytics or tracking

## 📞 Support & Resources

### Getting Help
1. Check this README
2. Review code comments in `app_advanced.py`
3. Test with standard processes first
4. Start with small datasets

### Common Questions

**Q: Can I use this for production data?**
A: This generates synthetic data for testing and training only.

**Q: How many custom processes can I create?**
A: No hard limit, but recommend keeping under 50 for performance.

**Q: Can I share processes with others?**
A: Yes, use the Export/Import JSON functionality.

**Q: Does it support BPMN 1.0?**
A: No, only BPMN 2.0 is supported.

**Q: Can I edit standard processes?**
A: No, but you can create a custom copy and edit that.

---

**Version**: 2.0.0 (Advanced Edition)
**Last Updated**: 2026-06-17
**Celonis-Inspired Process Intelligence Data Generator**

🚀 **Happy Process Mining!**
