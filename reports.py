import pandas as pd
import logging
import os
from datetime import datetime
from database import get_db
from api_integration import get_currency_api

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate business reports in CSV and Excel formats"""
    
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logger.info(f"Report output directory: {output_dir}")
    
    def generate_task_summary_report(self) -> str:
        """Generate a summary report of all tasks"""
        try:
            db = get_db()
            
            # Fetch tasks with employee details
            response = db.table('tasks').select(
                'id, title, status, priority, due_date, assigned_to, created_at'
            ).execute()
            
            tasks = response.data
            
            if not tasks:
                logger.warning("No tasks found for report")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(tasks)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'task_summary_{timestamp}.xlsx'
            filepath = os.path.join(self.output_dir, filename)
            
            # Create Excel writer
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='All Tasks', index=False)
                
                # Add summary statistics sheet
                summary_stats = {
                    'Status': df['status'].value_counts().to_dict(),
                    'Priority': df['priority'].value_counts().to_dict()
                }
                stats_df = pd.DataFrame(summary_stats)
                stats_df.to_excel(writer, sheet_name='Statistics')
            
            logger.info(f"✓ Task summary report generated: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"✗ Failed to generate task summary report: {str(e)}")
            return None
    
    def generate_employee_performance_report(self) -> str:
        """Generate employee performance report based on task completion"""
        try:
            db = get_db()
            
            # Fetch tasks grouped by employee
            response = db.table('tasks').select(
                'assigned_to, status'
            ).execute()
            
            tasks = response.data
            
            if not tasks:
                logger.warning("No tasks found for employee performance report")
                return None
            
            df = pd.DataFrame(tasks)
            
            # Calculate performance metrics
            performance = df.groupby('assigned_to').agg({
                'status': [
                    ('total_tasks', 'count'),
                    ('completed', lambda x: (x == 'done').sum()),
                    ('in_progress', lambda x: (x == 'in_progress').sum()),
                    ('pending', lambda x: (x == 'pending').sum())
                ]
            }).reset_index()
            
            performance.columns = ['employee_id', 'total_tasks', 'completed', 
                                   'in_progress', 'pending']
            performance['completion_rate'] = (
                performance['completed'] / performance['total_tasks'] * 100
            ).round(2)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'employee_performance_{timestamp}.xlsx'
            filepath = os.path.join(self.output_dir, filename)
            
            # Write to Excel
            performance.to_excel(filepath, sheet_name='Performance', index=False)
            
            logger.info(f"✓ Employee performance report generated: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"✗ Failed to generate employee performance report: {str(e)}")
            return None
    
    def generate_currency_rates_report(self, base_currency: str = 'USD') -> str:
        """Generate current exchange rates report"""
        try:
            currency_api = get_currency_api()
            rates = currency_api.get_exchange_rates(base_currency)
            
            if not rates:
                logger.warning("No currency rates fetched")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(list(rates.items()), columns=['Currency', 'Rate'])
            df = df.sort_values('Currency').reset_index(drop=True)
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'currency_rates_{base_currency}_{timestamp}.csv'
            filepath = os.path.join(self.output_dir, filename)
            
            # Write to CSV
            df.to_csv(filepath, index=False)
            
            logger.info(f"✓ Currency rates report generated: {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"✗ Failed to generate currency rates report: {str(e)}")
            return None
    
    def list_reports(self) -> list:
        """List all generated reports"""
        try:
            reports = os.listdir(self.output_dir)
            return sorted(reports)
        except Exception as e:
            logger.error(f"Failed to list reports: {str(e)}")
            return []

report_generator = ReportGenerator()

def get_report_generator():
    """Get report generator instance"""
    return report_generator
