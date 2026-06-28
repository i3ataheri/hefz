"""
Daily cleanup: deletes all registration records at midnight (Saudi time).
"""
from supabase_client import delete_all_registrations


def run_cleanup() -> int:
    """
    Delete all registration records from the database.
    Returns the number of deleted records.
    """
    count = delete_all_registrations()
    print(f"Cleanup completed. Deleted {count} registration records.")
    return count
