export const CONFIG = {
  TIMEZONE: 'Asia/Riyadh',
  OPEN_HOUR: 13,
  CLOSE_HOUR: 15,
  FRIDAY_INDEX: 5,
  SATURDAY_INDEX: 6,
  MANAGER_COUNT: 5,
};

export function getSaudiDate(): Date {
  const now = new Date();
  const saudi = new Date(now.toLocaleString('en-US', { timeZone: CONFIG.TIMEZONE }));
  return saudi;
}

export function getSaudiTime(): { hour: number; minute: number; day: number } {
  const d = getSaudiDate();
  return { hour: d.getHours(), minute: d.getMinutes(), day: d.getDay() };
}
