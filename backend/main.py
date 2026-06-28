"""
Main scheduler for the Quran circle registration system.
Runs:
  - Every day at 15:00 AST: Send WhatsApp report
  - Every day at 00:00 AST: Cleanup registrations
"""
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from dotenv import load_dotenv

from report import build_html_report
from whatsapp import send_whatsapp
from cleanup import run_cleanup

load_dotenv()

TIMEZONE = os.environ.get("TIMEZONE", "Asia/Riyadh")
TZ = pytz.timezone(TIMEZONE)


def job_send_report():
    """Generate and send the daily registration report."""
    print(f"[{datetime.now()}] Generating daily report...")
    report = build_html_report()
    print(report)
    success = send_whatsapp(report)
    if success:
        print(f"[{datetime.now()}] Report sent successfully.")
    else:
        print(f"[{datetime.now()}] Failed to send report.")


def job_cleanup():
    """Clean up all registration records."""
    print(f"[{datetime.now()}] Running daily cleanup...")
    count = run_cleanup()
    print(f"[{datetime.now()}] Cleanup finished. Deleted {count} records.")


def main():
    scheduler = BlockingScheduler(timezone=TZ)

    # Schedule report at 15:00 AST daily
    scheduler.add_job(
        job_send_report,
        CronTrigger(hour=15, minute=0, timezone=TZ),
        id="send_report",
        name="Send daily WhatsApp report",
    )

    # Schedule cleanup at 00:00 AST daily
    scheduler.add_job(
        job_cleanup,
        CronTrigger(hour=0, minute=0, timezone=TZ),
        id="cleanup",
        name="Cleanup registrations",
    )

    print(f"🚀 Scheduler started. Timezone: {TIMEZONE}")
    print("   📊 Report: 15:00 daily")
    print("   🧹 Cleanup: 00:00 daily")
    print("   Press Ctrl+C to stop.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()
