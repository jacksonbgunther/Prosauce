-- "Next drop" notify-me signups. Written only by the /api/signup serverless
-- function using the service role key; RLS with no policies blocks the public
-- anon key from reading or writing this table.
create table if not exists public.signups (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  name text not null check (char_length(name) between 1 and 100),
  contact text not null check (char_length(contact) between 3 and 254),
  contact_type text not null check (contact_type in ('email', 'phone')),
  source text not null,
  sms_consent boolean not null default false
);

create index if not exists signups_created_at_idx on public.signups (created_at desc);

alter table public.signups enable row level security;
