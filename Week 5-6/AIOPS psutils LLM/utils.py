from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from fpdf import FPDF
import os
import subprocess

# Utility function to save a report as a PDF
def save_report_as_pdf(report_content, folder="reports"):
    """
    Save the given report content as a PDF file in the specified folder.

    Args:
        report_content (str): The content of the report to save.
        folder (str): The folder where the PDF will be saved. Defaults to "reports".

    Returns:
        str: The file path of the saved PDF.
    """
    try:
        # Ensure the folder exists
        os.makedirs(folder, exist_ok=True)

        # Generate a timestamped file name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(folder, f"system_report_{timestamp}.pdf")

        # Create and save the PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, report_content)
        pdf.output(file_path)

        return file_path
    except Exception as e:
        print(f"Error saving report as PDF: {str(e)}")
        raise

# Utility function to archive old reports
def archive_old_reports(folder="reports", max_files=10):
    """
    Archive old reports by keeping only the latest `max_files` files in the folder.

    Args:
        folder (str): The folder containing the reports. Defaults to "reports".
        max_files (int): The maximum number of files to keep. Defaults to 10.
    """
    try:
        # List all files in the folder, sorted by creation time
        files = sorted(
            [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))],
            key=os.path.getctime
        )

        # Remove older files if the limit is exceeded
        while len(files) > max_files:
            old_file = files.pop(0)
            os.remove(old_file)
    except Exception as e:
        print(f"Error archiving old reports: {str(e)}")
        raise

# Utility function to schedule a task
def schedule_task(scheduler, func, interval_seconds, job_id):
    """
    Schedule a task to run at a fixed interval.

    Args:
        scheduler (BackgroundScheduler): The scheduler instance.
        func (callable): The function to schedule.
        interval_seconds (int): The interval in seconds between executions.
        job_id (str): The unique ID for the scheduled job.
    """
    try:
        scheduler.add_job(func, 'interval', seconds=interval_seconds, id=job_id, replace_existing=True)
    except Exception as e:
        print(f"Error scheduling task: {str(e)}")
        raise

# Utility function to delete a scheduled task
def delete_scheduled_task(scheduler, job_id):
    """
    Delete a scheduled task by its job ID.

    Args:
        scheduler (BackgroundScheduler): The scheduler instance.
        job_id (str): The unique ID of the job to delete.
    """
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        print(f"Job with ID {job_id} not found.")
    except Exception as e:
        print(f"Error deleting scheduled task: {str(e)}")
        raise

# Utility function to execute a runbook
def run_runbook():
    """
    Execute a predefined runbook. This can be a script to perform automated tasks.
    """
    try:
        os.system("taskkill /f /im notepad.exe")  # Example: Close notepad.exe
    except Exception as e:
        print(f"Error executing runbook: {str(e)}")
        raise

# Utility function to retrieve all scheduled jobs
def get_scheduled_jobs(scheduler):
    """
    Retrieve all scheduled jobs from the scheduler.

    Args:
        scheduler (BackgroundScheduler): The scheduler instance.

    Returns:
        list: A list of scheduled jobs.
    """
    try:
        return scheduler.get_jobs()
    except JobLookupError as e:
        print(f"Error retrieving scheduled jobs: {str(e)}")
        return []