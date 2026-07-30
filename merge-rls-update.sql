-- ============================================================
-- Tighten RLS on the 3D-print tables now that order/gallery/review
-- management lives behind K&D's real admin login (profiles.is_admin)
-- instead of the old hardcoded admin.html password.
-- Run this AFTER supabase-setup.sql, gallery-posts-setup.sql, and
-- reviews-setup.sql have already created the tables.
-- ============================================================

-- ---------- ORDERS ----------
-- Previously: "Allow anon reads" using (true) — anyone could read
-- every customer's name/email/phone/notes. Restrict reads to admins;
-- keep public insert so the order form still works for anyone.
drop policy if exists "Allow anon reads" on public.orders;

create policy "Admins can read orders"
  on public.orders for select
  using (exists (select 1 from public.profiles where id = auth.uid() and is_admin = true));

create policy "Admins can update orders"
  on public.orders for update
  using (exists (select 1 from public.profiles where id = auth.uid() and is_admin = true));

-- (the existing "Allow anon inserts" policy is kept as-is so the
--  order form keeps working for anonymous visitors)

-- ---------- GALLERY POSTS ----------
-- Previously: public insert AND public delete. Public read/insert stays
-- (admin adds posts through the app using the anon key, same as before),
-- but delete should require admin.
drop policy if exists "Allow delete" on public.gallery_posts;

create policy "Admins can delete gallery posts"
  on public.gallery_posts for delete
  using (exists (select 1 from public.profiles where id = auth.uid() and is_admin = true));

-- ---------- REVIEWS ----------
-- Previously: public delete. Keep public read/insert (anyone can leave
-- a review), but only admins can remove one.
drop policy if exists "Allow delete reviews" on reviews;

create policy "Admins can delete reviews"
  on reviews for delete
  using (exists (select 1 from public.profiles where id = auth.uid() and is_admin = true));

-- ============================================================
-- NOTE: the drop/insert/update policies above all check
-- public.profiles.is_admin, the same table K&D's admin system
-- already uses. If you're an admin on K&D, you're an admin here
-- too — no separate login needed.
-- ============================================================
