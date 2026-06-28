import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';
import fs from 'fs';

function loadDotEnv(path) {
  const raw = {};
  try {
    const text = fs.readFileSync(path, 'utf-8');
    for (const line of text.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eq = trimmed.indexOf('=');
      if (eq === -1) continue;
      const key = trimmed.slice(0, eq).trim();
      let val = trimmed.slice(eq + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      if (key.startsWith('VITE_')) raw[key] = val;
    }
  } catch {}
  return raw;
}

const env = { ...loadDotEnv('.env') };
// Fallback to process.env (used on Vercel where .env is not present)
if (!env.VITE_SUPABASE_URL) env.VITE_SUPABASE_URL = process.env.VITE_SUPABASE_URL;
if (!env.VITE_SUPABASE_ANON_KEY) env.VITE_SUPABASE_ANON_KEY = process.env.VITE_SUPABASE_ANON_KEY;

export default defineConfig({
  output: 'static',
  adapter: vercel({
    webAnalytics: {
      enabled: true,
    },
  }),
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler',
        },
      },
    },
    define: {
      'import.meta.env.VITE_SUPABASE_URL': JSON.stringify(env.VITE_SUPABASE_URL || ''),
      'import.meta.env.VITE_SUPABASE_ANON_KEY': JSON.stringify(env.VITE_SUPABASE_ANON_KEY || ''),
    },
  },
});
