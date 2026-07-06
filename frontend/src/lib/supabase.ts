const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_ANON_KEY;
const hdrs = { 'apikey': key, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' };

function fetch_(method: string, path: string, body?: unknown) {
  return fetch(url + path, { method, headers: hdrs, body: body ? JSON.stringify(body) : void 0 });
}

class Q {
  private t: string; private c = '*'; private fs: string[] = []; private o = ''; private s = false;
  constructor(t: string) { this.t = t; }
  select(col: string) { this.c = col; return this; }
  eq(col: string, val: unknown) { this.fs.push(col + '=eq.' + val); return this; }
  order(col: string) { this.o = '&order=' + col; return this; }
  single() { this.s = true; return this; }
  then(resolve: (r: { data: unknown; error: unknown }) => void) {
    const qs = '/rest/v1/' + this.t + '?select=' + this.c + (this.fs.length ? '&' + this.fs.join('&') : '') + this.o;
    fetch_('GET', qs).then(r => { if (!r.ok) throw new Error(r.status + ''); return r.json(); }).then(d => resolve({ data: this.s ? (d?.[0] || null) : (d || []), error: null })).catch(e => resolve({ data: null, error: e }));
    return { catch: () => {} };
  }
}

function thenable<T>(exec: (resolve: (r: T) => void) => void): Promise<T> {
  return { then: (res: (r: T) => void) => { exec(res); return { catch: () => {} }; } } as any;
}

export const supabase = {
  from: (table: string) => ({
    select: (cols: string) => new Q(table).select(cols),
    insert: (row: Record<string, unknown>) => thenable<{ error: unknown }>(resolve =>
      fetch_('POST', '/rest/v1/' + table, row).then(r => {
        if (!r.ok && r.status === 409) return resolve({ error: { code: '23505', message: 'duplicate' } });
        if (!r.ok) throw new Error(r.status + '');
        resolve({ error: null });
      }).catch(e => resolve({ error: e }))
    ),
  }),
  rpc: (fn: string, params: Record<string, unknown>) => thenable<{ data: unknown; error: unknown }>(resolve =>
    fetch_('POST', '/rest/v1/rpc/' + fn, params).then(r => { if (!r.ok) throw new Error(r.status + ''); return r.json().catch(() => null); }).then(d => resolve({ data: d, error: null })).catch(e => resolve({ data: null, error: e }))
  ),
};
