# Object-Centric Process Mining Data Generator - Streamlit UI

A user-friendly web interface for generating realistic process mining data following the **Celonis Object-Centric Methodology**.

## 🚀 Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📋 Features

### Interactive Web Interface
- **Dropdown Menus**: Easy selection of business processes
- **Radio Buttons**: Quick data size selection
- **Checkboxes**: Multi-select data quality issues
- **Real-time Preview**: View generated data before downloading
- **One-Click Download**: Export to Excel with a single click

### Supported Business Processes
1. **Order to Cash (O2C)** - Sales order processing
2. **Purchase to Pay (P2P)** - Procurement and payment
3. **Procurement** - Requisition to delivery
4. **Finance Operations** - Invoice processing
5. **BPO Operations** - Service ticket management

### Data Size Options
- **Small**: 100 cases
- **Medium**: 500 cases
- **Large**: 1,000 cases
- **Extra Large**: 5,000 cases
- **Custom**: 10-10,000 cases (user-defined)

### Data Quality Issues (8 Types)
Each issue can be toggled on/off with checkboxes:

1. 🔴 **Missing Activities** (High Severity)
2. 🟡 **Duplicate Activities** (Medium Severity)
3. 🔴 **Out of Sequence** (High Severity)
4. 🟡 **Long Waiting Times** (Medium Severity)
5. 🔴 **Rework Loops** (High Severity)
6. 🟢 **Missing Case Attributes** (Low Severity)
7. 🟡 **Inconsistent Timestamps** (Medium Severity)
8. 🔴 **Orphaned Events** (High Severity)

## 🎯 How to Use

### Step 1: Configure Settings (Sidebar)

1. **Select Business Process**
   - Use dropdown to choose your process type
   - Each process has unique activities and attributes

2. **Choose Data Size**
   - Select from preset sizes or enter custom value
   - Recommended: Start with "Small" for testing

3. **Select Data Quality Issues**
   - Check boxes for issues you want to inject
   - Hover over each option to see description
   - Can select multiple issues simultaneously

### Step 2: Generate Data

1. Click the **"🚀 Generate Data"** button
2. Wait for generation (typically 1-5 seconds)
3. Review the summary statistics

### Step 3: Review & Download

1. **View Summary Metrics**
   - Total cases and events
   - Average events per case
   - Number of issues injected

2. **Preview Data Tables**
   - Case table preview (first 10 rows)
   - Event log preview (first 20 rows)

3. **Download Files**
   - Click "📥 Download Case Table (Excel)"
   - Click "📥 Download Event Log (Excel)"
   - Files are ready to use in process mining tools

### Step 4: Analyze Insights (Optional)

Expand the **"📈 Data Insights"** section to view:
- Case status distribution chart
- Top 10 activities chart

## 📊 Output Files

### Case Table
- **Filename**: `ocpm_cases_[prefix].xlsx`
- **Contains**: Business objects (orders, invoices, tickets, etc.)
- **Structure**: One row per case with attributes

### Event Log
- **Filename**: `ocpm_events_[prefix].xlsx`
- **Contains**: All activities/events
- **Structure**: One row per event with timestamps

## 🔧 Advanced Usage

### Combining Multiple Issues

You can select multiple data quality issues to create complex scenarios:

**Example 1: Process Inefficiency Analysis**
- ✓ Long Waiting Times
- ✓ Rework Loops
- ✓ Missing Activities

**Example 2: Data Quality Assessment**
- ✓ Missing Case Attributes
- ✓ Duplicate Activities
- ✓ Inconsistent Timestamps

**Example 3: Comprehensive Testing**
- ✓ Select ALL issues for maximum complexity

### Custom Data Sizes

For specific testing needs:
1. Select "Custom" in data size
2. Enter exact number of cases (10-10,000)
3. Larger datasets take longer to generate

## 💡 Tips & Best Practices

### For Learning
- Start with **Small (100 cases)** and **1-2 issues**
- Gradually increase complexity
- Compare clean vs. problematic data

### For Demonstrations
- Use **Medium (500 cases)** for balanced demos
- Select **3-4 relevant issues** for your story
- Download and prepare files before presentation

### For Testing Tools
- Use **Large (1,000+ cases)** for performance testing
- Select **ALL issues** for comprehensive validation
- Test with different business processes

### For Training
- Generate multiple datasets with different issues
- Use **Custom sizes** to match training scenarios
- Create before/after improvement examples

## 🎨 UI Features

### Sidebar Configuration
- Persistent settings during session
- Clear visual hierarchy
- Helpful tooltips on hover

### Main Content Area
- Welcome screen with process overview
- Real-time generation progress
- Comprehensive data preview
- Interactive charts and metrics

### Download Section
- Separate buttons for each file
- Automatic filename generation
- Excel format for compatibility

## 🔍 Validation & Cleanup

The generator automatically:
- ✓ Removes duplicate case IDs
- ✓ Removes duplicate event IDs
- ✓ Validates case-event relationships
- ✓ Sorts events chronologically
- ✓ Reports all changes made

Validation results are displayed after generation.

## 📈 Data Insights

### Case Status Distribution
- Visual bar chart
- Shows completed, in-progress, cancelled cases
- Helps understand process completion rates

### Top Activities
- Bar chart of most frequent activities
- Identifies bottlenecks and common steps
- Useful for process analysis

## 🛠️ Troubleshooting

### Application Won't Start
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Try running with verbose output
streamlit run app.py --logger.level=debug
```

### Slow Generation
- Reduce data size
- Deselect some data quality issues
- Close other applications

### Download Issues
- Check browser download settings
- Ensure sufficient disk space
- Try different browser if needed

### Display Problems
- Refresh the page (F5)
- Clear browser cache
- Update Streamlit: `pip install --upgrade streamlit`

## 🔐 Data Privacy

- All data is generated locally
- No data is sent to external servers
- Files are created in-memory
- Downloads are direct to your computer

## 🚀 Performance

### Generation Times (Approximate)
- 100 cases: ~1 second
- 500 cases: ~2-3 seconds
- 1,000 cases: ~4-5 seconds
- 5,000 cases: ~15-20 seconds

### Browser Requirements
- Modern browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled
- Minimum 4GB RAM recommended

## 📝 Example Workflow

1. **Open Application**
   ```bash
   streamlit run app.py
   ```

2. **Configure**
   - Process: Order to Cash
   - Size: Medium (500)
   - Issues: Missing Activities, Long Waiting Times

3. **Generate**
   - Click "Generate Data"
   - Wait 2-3 seconds

4. **Review**
   - Check metrics: 500 cases, ~4,500 events
   - Preview tables
   - View insights charts

5. **Download**
   - Download both Excel files
   - Import into Celonis/process mining tool

6. **Analyze**
   - Identify missing approval steps
   - Find bottlenecks with long wait times
   - Create process improvement recommendations

## 🎓 Learning Resources

### Understanding Object-Centric Process Mining
- Each case represents a business object
- Events are activities performed on objects
- Relationships show process flow
- Timestamps enable temporal analysis

### Common Analysis Patterns
- **Conformance Checking**: Compare actual vs. expected flow
- **Bottleneck Analysis**: Find long waiting times
- **Rework Detection**: Identify repeated activities
- **Variant Analysis**: Compare different process paths

## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Checking Version
```bash
streamlit --version
```

## 📞 Support

For issues or questions:
1. Check this README
2. Review code comments in `app.py`
3. Test with smaller datasets first
4. Verify all dependencies are installed

---

**Happy Process Mining! 📊🚀**
