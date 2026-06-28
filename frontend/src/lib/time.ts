import { CONFIG, getSaudiTime, getSaudiDate } from './config';

export type RegistrationStatus =
  | 'closed'      // completely closed
  | 'friday'      // Friday - always closed
  | 'saturday'    // Saturday - depends on flag
  | 'before'      // before 13:00
  | 'open'        // 13:00-15:00
  | 'after';      // after 15:00

export async function getRegistrationStatus(saturdayEnabled: boolean): Promise<{
  status: RegistrationStatus;
  nextOpenTime?: string;
}> {
  const { hour, minute, day } = getSaudiTime();

  // Friday check
  if (day === CONFIG.FRIDAY_INDEX) {
    return { status: 'friday' };
  }

  // Saturday check
  if (day === CONFIG.SATURDAY_INDEX && !saturdayEnabled) {
    return { status: 'saturday' };
  }

  // Time check
  if (hour < CONFIG.OPEN_HOUR) {
    return { status: 'before' };
  }

  if (hour >= CONFIG.CLOSE_HOUR) {
    return { status: 'after' };
  }

  return { status: 'open' };
}

export function getTimeUntilOpen(): number {
  const now = getSaudiDate();
  const open = new Date(now);
  open.setHours(CONFIG.OPEN_HOUR, 0, 0, 0);
  return Math.max(0, open.getTime() - now.getTime());
}

export function getTimeUntilClose(): number {
  const now = getSaudiDate();
  const close = new Date(now);
  close.setHours(CONFIG.CLOSE_HOUR, 0, 0, 0);
  return Math.max(0, close.getTime() - now.getTime());
}

export function formatCountdown(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const parts: string[] = [];
  if (hours > 0) parts.push(`${hours} ساعة`);
  if (minutes > 0) parts.push(`${minutes} دقيقة`);
  parts.push(`${seconds} ثانية`);

  return parts.join(' و ');
}
