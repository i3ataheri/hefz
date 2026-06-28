import os
from datetime import date, datetime
from typing import Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

_url = os.environ["VITE_SUPABASE_URL"]
_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

_supabase: Client = create_client(_url, _key)


def get_supabase() -> Client:
    return _supabase


def get_setting(key: str) -> Any:
    result = _supabase.table("settings").select("value").eq("key", key).execute()
    if result.data:
        return result.data[0]["value"]
    return None


def get_is_saturday_enabled() -> bool:
    val = get_setting("is_saturday_enabled")
    return bool(val)


def get_managers() -> list[dict]:
    result = (
        _supabase.table("managers")
        .select("*")
        .order("sort_order")
        .execute()
    )
    return result.data or []


def get_today_registrations(today: date | None = None) -> list[dict]:
    if today is None:
        today = date.today()
    result = (
        _supabase.table("registrations")
        .select("*")
        .eq("registered_date", today.isoformat())
        .order("created_at")
        .execute()
    )
    return result.data or []


def delete_all_registrations() -> int:
    result = _supabase.table("registrations").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    return len(result.data or [])
