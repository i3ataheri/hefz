"""
Generate the daily registration report.
- Only those who registered today appear in the list
- Managers who registered are placed first (rotating order)
- Priority member 'هدى الغماس' always appears right after managers
- Regular members appear after priority member, ordered by timestamp
"""
from datetime import date, datetime
from supabase_client import get_managers, get_today_registrations

PRIORITY_MEMBER = "هدى الغماس"


def _get_day_offset(today: date, total_managers: int) -> int:
    epoch = date(2025, 1, 1)
    delta = (today - epoch).days
    return delta % max(total_managers, 1)


def _partition_members(all_registrations: list, manager_names: set) -> tuple:
    """Returns (rotated_managers, priority_member, other_members)."""
    # Managers
    manager_regs = [r for r in all_registrations if r["name"] in manager_names]
    other_regs = [r for r in all_registrations if r["name"] not in manager_names]
    return manager_regs, other_regs


def _build_rotated_managers(all_managers: list, all_registrations: list, today: date) -> list:
    if not all_managers:
        return []
    offset = _get_day_offset(today, len(all_managers))
    rotated = all_managers[offset:] + all_managers[:offset]
    names = [m["name"] for m in rotated if m["name"] in {r["name"] for r in all_registrations}]
    result = [r for r in all_registrations if r["name"] in names]
    result.sort(key=lambda r: names.index(r["name"]))
    return result


def _sort_members(member_regs: list) -> list:
    """Priority member first, then sorted by created_at."""
    priority = [r for r in member_regs if r["name"] == PRIORITY_MEMBER]
    others = [r for r in member_regs if r["name"] != PRIORITY_MEMBER]
    return priority + others


def build_report(today: date | None = None) -> str:
    if today is None:
        today = date.today()

    all_managers = get_managers()
    manager_names = {m["name"] for m in all_managers}
    all_registrations = get_today_registrations(today)

    rotated = _build_rotated_managers(all_managers, all_registrations, today)
    member_regs = _sort_members([r for r in all_registrations if r["name"] not in manager_names])

    weekdays = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    weekday_name = weekdays[today.weekday()]

    report_lines = [
        "=" * 40,
        f"           تقرير حلقة القرآن",
        f"        {today.strftime('%Y/%m/%d')} - {weekday_name}",
        "=" * 40,
        "",
    ]

    idx = 1
    if rotated:
        report_lines.append("👤 المدراء:")
        report_lines.append("-" * 40)
        for r in rotated:
            time_str = datetime.fromisoformat(r["created_at"]).strftime("%H:%M")
            report_lines.append(f"  {idx}. {r['name']}  ⏰ {time_str}")
            idx += 1
        report_lines.append("")

    if member_regs:
        report_lines.append("📋 الأعضاء:")
        report_lines.append("-" * 40)
        for r in member_regs:
            time_str = datetime.fromisoformat(r["created_at"]).strftime("%H:%M")
            report_lines.append(f"  {idx}. {r['name']}  ⏰ {time_str}")
            idx += 1

    if not all_registrations:
        report_lines.append("لا يوجد حضور حتى الآن.")

    report_lines.extend([
        "",
        "=" * 40,
        f"إجمالي الحضور: {idx - 1}",
        f"المدراء: {len(rotated)}",
        f"الأعضاء: {len(member_regs)}",
        "=" * 40,
        f"تم إنشاء التقرير: {datetime.now().strftime('%H:%M:%S')}",
    ])

    return "\n".join(report_lines)


def build_html_report(today: date | None = None) -> str:
    """WhatsApp-friendly report (supports Markdown-style bold)."""
    if today is None:
        today = date.today()

    all_managers = get_managers()
    manager_names = {m["name"] for m in all_managers}
    all_registrations = get_today_registrations(today)

    rotated = _build_rotated_managers(all_managers, all_registrations, today)
    member_regs = _sort_members([r for r in all_registrations if r["name"] not in manager_names])

    weekdays = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    weekday_name = weekdays[today.weekday()]

    lines = [
        f"📖 تقرير حلقة القرآن",
        f"📅 {today.strftime('%Y/%m/%d')} - {weekday_name}",
        "",
    ]

    idx = 1
    if rotated:
        lines.append("👤 *المدراء:*")
        for r in rotated:
            time_str = datetime.fromisoformat(r["created_at"]).strftime("%H:%M")
            lines.append(f"  {idx}. {r['name']} ({time_str})")
            idx += 1
        lines.append("")

    if member_regs:
        lines.append("📋 *الأعضاء:*")
        for r in member_regs:
            time_str = datetime.fromisoformat(r["created_at"]).strftime("%H:%M")
            lines.append(f"  {idx}. {r['name']} ({time_str})")
            idx += 1

    if not all_registrations:
        lines.append("لا يوجد حضور حتى الآن.")

    total = idx - 1
    lines.extend([
        "",
        f"📊 الإجمالي: {total}",
        f"✅ المدراء: {len(rotated)} | الأعضاء: {len(member_regs)}",
    ])

    return "\n".join(lines)
