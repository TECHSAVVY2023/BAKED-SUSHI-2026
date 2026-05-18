<template>
  <div
    class="min-h-screen text-slate-900"
    style="background: radial-gradient(1200px 700px at 16% -8%, rgba(242, 124, 134, 0.34), rgba(255, 255, 255, 0) 58%), radial-gradient(1100px 680px at 86% 0%, rgba(242, 161, 170, 0.22), rgba(255, 255, 255, 0) 60%), linear-gradient(180deg, rgba(255, 238, 241, 1), rgba(255, 247, 248, 1) 38%, rgba(255, 255, 255, 1) 100%);"
  >
    <AppTopbar>
      <template #left>
        <a
          href="#top"
          @click.prevent="scrollTo('top')"
          class="flex min-w-[220px] items-center gap-3 text-slate-900 no-underline"
        >
          <img class="h-11 w-11 rounded-xl border border-slate-200 bg-white/70 object-cover" :src="logo" alt="Baked Sushi logo" />
          <div class="flex items-center gap-3 whitespace-nowrap">
            <div class="font-black tracking-tight">Baked Sushi</div>
          </div>
        </a>
      </template>

      <template #center>
        <nav class="hidden items-center justify-center gap-2 sm:flex">
          <div class="group/menu relative">
            <button
              class="inline-flex items-center gap-2 rounded-xl px-4 py-2 text-[#f27c86] font-semibold transition hover:bg-[#f7c4ca]/50 hover:text-slate-900 group-hover/menu:bg-[#f7c4ca]/50 group-hover/menu:text-slate-900"
              type="button"
            >
              Menu
              <svg class="h-4 w-4 transition-transform group-hover/menu:rotate-180" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 11.168l3.71-3.938a.75.75 0 1 1 1.08 1.04l-4.25 4.51a.75.75 0 0 1-1.08 0L5.21 8.27a.75.75 0 0 1 .02-1.06Z" clip-rule="evenodd" />
              </svg>
            </button>

            <div class="pointer-events-none absolute left-0 top-full z-50 pt-2 opacity-0 transition duration-150 group-hover/menu:pointer-events-auto group-hover/menu:opacity-100 group-focus-within/menu:pointer-events-auto group-focus-within/menu:opacity-100">
              <div class="w-[280px] rounded-[1.25rem] border border-[#f2c0c7] bg-white/95 p-3 shadow-[0_20px_60px_rgba(15,23,42,0.14)] backdrop-blur">
                <div class="mb-2 px-3 pt-1 text-[11px] font-black uppercase tracking-[0.18em] text-[#c96b76]">
                  Browse Menu
                </div>

                <button
                  class="flex w-full items-center justify-between rounded-xl px-3 py-3 text-left text-base font-semibold text-slate-700 transition hover:bg-[#fff1f3] hover:text-slate-900"
                  type="button"
                  @click="scrollTo('menu')"
                >
                  <span>All Products</span>
                  <span class="text-xs text-slate-400">{{ menu.length }}</span>
                </button>

                <button
                  v-for="cat in categoryOrder"
                  :key="cat"
                  class="flex w-full items-center justify-between rounded-xl px-3 py-3 text-left text-base font-semibold text-slate-700 transition hover:bg-[#fff1f3] hover:text-slate-900"
                  type="button"
                  @click="scrollTo(`cat-${slug(cat)}`)"
                >
                  <span>{{ cat }}</span>
                  <span class="text-xs text-slate-400">{{ (menuByCategory[cat] || []).length }}</span>
                </button>

                <button
                  v-if="bestSeller"
                  class="mt-1 flex w-full items-center justify-between rounded-xl bg-[#fff6f7] px-3 py-3 text-left text-base font-semibold text-slate-800 transition hover:bg-[#ffe8eb]"
                  type="button"
                  @click="scrollTo(`cat-${slug(bestSeller.category)}`)"
                >
                  <span>Best Seller</span>
                  <span class="rounded-full bg-[#f27c86]/12 px-2 py-1 text-[11px] font-black uppercase tracking-[0.12em] text-[#d45d6d]">
                    {{ bestSeller.name }}
                  </span>
                </button>

                <button
                  class="mt-1 flex w-full items-center justify-between rounded-xl px-3 py-3 text-left text-base font-semibold text-slate-700 transition hover:bg-[#fff1f3] hover:text-slate-900"
                  type="button"
                  @click="scrollTo('menu')"
                >
                  <span>Promos & Events</span>
                  <span class="text-xs text-[#f27c86]">See offers</span>
                </button>
              </div>
            </div>
          </div>

          <a
            href="#how"
            @click.prevent="scrollTo('how')"
            class="inline-flex items-center rounded-xl px-4 py-2 text-[#f27c86] font-semibold transition hover:bg-[#f7c4ca]/50 hover:text-slate-900"
          >
            How to Order
          </a>
          <a
            href="#about"
            @click.prevent="scrollTo('about')"
            class="inline-flex items-center rounded-xl px-4 py-2 text-[#f27c86] font-semibold transition hover:bg-[#f7c4ca]/50 hover:text-slate-900"
          >
            About
          </a>
          <a
            href="#contact"
            @click.prevent="scrollTo('contact')"
            class="inline-flex items-center rounded-xl px-4 py-2 text-[#f27c86] font-semibold transition hover:bg-[#f7c4ca]/50 hover:text-slate-900"
          >
            Contact
          </a>
        </nav>
      </template>

      <template #right>
        <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#f2a1aa]/45 bg-white/90 px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-[#f27c86] hover:bg-[#fff1f3] shadow-sm" type="button" @click="loginOpen = true">Login</button>

        <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#f2a1aa]/45 bg-white/90 px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-[#f27c86] hover:bg-[#fff1f3] shadow-sm" type="button" @click="cartOpen = true">
          <span class="h-2.5 w-2.5 rounded-xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] shadow-[0_0_0_4px_rgba(242,124,134,0.16)]"></span>
          Cart
          <span
            v-if="cartCount"
            class="inline-flex min-w-[26px] items-center justify-center rounded-xl bg-slate-200/70 px-2 text-sm font-semibold"
            aria-label="Items in cart"
          >
            {{ cartCount }}
          </span>
        </button>
      </template>
    </AppTopbar>

    <main id="top">
      <section class="relative grid min-h-[92vh] items-center overflow-hidden">
        <video
          class="absolute inset-0 h-full w-full object-cover scale-[1.03] saturate-[1.1] contrast-[1.08]"
          autoplay
          muted
          loop
          playsinline
          preload="metadata"
        >
          <source :src="heroVideo" type="video/mp4" />
        </video>

        <div class="absolute inset-0 bg-[radial-gradient(circle_at_20%_24%,rgba(255,255,255,0.12),rgba(242,124,134,0.42))] bg-[linear-gradient(180deg,rgba(255,225,230,0.18),rgba(242,124,134,0.44),rgba(255,233,236,0.82))]"></div>

        <div class="relative z-10 mx-auto flex w-full max-w-7xl justify-start px-4 py-10 sm:px-6">
          <div class="w-full max-w-3xl rounded-[2rem] border border-[#f2b3bb]/55 bg-[rgba(255,244,246,0.58)] p-5 shadow-[0_24px_80px_rgba(20,12,10,0.16)] backdrop-blur-md sm:p-7">
            <div class="font-semibold tracking-tight text-[#9d4b56]">Welcome to</div>

            <h1 class="mt-4 max-w-4xl text-5xl font-black tracking-tight leading-[0.95] sm:text-6xl">
              Baked Sushi
              <span class="block text-[#f27c86] italic font-black">Ozamiz</span>
            </h1>

            <p class="mt-6 max-w-2xl text-base leading-7 text-slate-800/90">
              Scoop | Wrap | Munch | Repeat
            </p>

            <div class="mt-8 flex flex-wrap gap-3">
              <a
                href="#menu"
                @click.prevent="scrollTo('menu')"
                class="inline-flex items-center rounded-xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-6 py-3 text-sm font-semibold text-slate-950 shadow-xl transition hover:brightness-105"
              >
                View Menu
              </a>
              <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-[#f2a1aa]/45 bg-[#fff4f5] px-6 py-3 text-sm font-semibold text-slate-900 transition hover:border-[#f27c86] hover:bg-white shadow-sm" type="button" @click="quickOrder()">Order Now</button>
            </div>
          </div>
        </div>
      </section>

      <section class="py-10">
        <div class="mx-auto max-w-7xl px-4 sm:px-6">
          <div class="rounded-[1.5rem] border border-[#f2c0c7] bg-white/72 p-6 shadow-[0_20px_60px_rgba(242,124,134,0.12)] backdrop-blur">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <div class="text-sm font-black uppercase tracking-[0.18em] text-[#c96b76]">Fresh Favorites</div>
                <h2 class="mt-2 text-3xl font-black tracking-tight text-slate-900">Why people keep ordering</h2>
              </div>
              <div class="text-sm text-slate-600">Freshly baked trays, fast replies, and crowd-ready servings.</div>
            </div>

            <div class="mt-6 grid gap-3 md:grid-cols-3">
              <article class="rounded-[1.125rem] border border-[#f2c0c7] bg-[rgba(255,244,246,0.92)] p-5 shadow-[0_18px_40px_rgba(242,124,134,0.12)]">
                <div class="flex items-start gap-3">
                  <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-white">
                    <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M4 7h16M7 3v4m10-4v4M6 11h12l-1 7H7l-1-7Z" />
                    </svg>
                  </span>
                  <div>
                    <div class="font-black text-slate-900">Large portions</div>
                    <div class="mt-1 text-sm text-slate-600">Party-ready trays for sharing, events, and cravings that need more than one bite.</div>
                  </div>
                </div>
              </article>

              <article class="rounded-[1.125rem] border border-[#f2c0c7] bg-[rgba(255,244,246,0.92)] p-5 shadow-[0_18px_40px_rgba(242,124,134,0.12)]">
                <div class="flex items-start gap-3">
                  <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-white">
                    <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 3v6l4 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                  </span>
                  <div>
                    <div class="font-black text-slate-900">Fast ordering</div>
                    <div class="mt-1 text-sm text-slate-600">Browse, add to cart, and send your order quickly without extra steps.</div>
                  </div>
                </div>
              </article>

              <article class="rounded-[1.125rem] border border-[#f2c0c7] bg-[rgba(255,244,246,0.92)] p-5 shadow-[0_18px_40px_rgba(242,124,134,0.12)]">
                <div class="flex items-start gap-3">
                  <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-white">
                    <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="m12 21-1.45-1.32C5.4 15.04 2 11.97 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09A6 6 0 0 1 16.5 3C19.58 3 22 5.42 22 8.5c0 3.47-3.4 6.54-8.55 11.18Z" />
                    </svg>
                  </span>
                  <div>
                    <div class="font-black text-slate-900">Made with care</div>
                    <div class="mt-1 text-sm text-slate-600">Comfort food energy with rich flavor, soft textures, and a signature salmon-pink style.</div>
                  </div>
                </div>
              </article>
            </div>

            <div class="mt-8 overflow-hidden rounded-[1.25rem] border border-[#f2c0c7] bg-[rgba(255,248,249,0.88)] p-4">
              <div class="mb-3 flex items-center justify-between gap-3">
                <div class="font-black text-slate-900">Product Preview</div>
                <div class="text-xs uppercase tracking-[0.18em] text-[#c96b76]">Slides left</div>
              </div>

              <div class="product-marquee">
                <div class="product-track">
                  <article v-for="item in productShowcase" :key="`${item.id}-${item.trackKey}`" class="product-slide-card">
                    <div class="product-slide-image">
                      <img :src="item.image || logo" :alt="item.name" loading="lazy" />
                    </div>
                    <div class="mt-3">
                      <div class="truncate font-black text-slate-900">{{ item.name }}</div>
                      <div class="mt-1 text-sm text-slate-600">{{ item.category }}</div>
                    </div>
                  </article>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="menu" class="py-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-6">
          <div class="mb-8 flex flex-col gap-4 rounded-[1.25rem] bg-white/80 p-6 shadow-[0_18px_50px_rgba(15,23,42,0.08)] sm:flex-row sm:items-end sm:justify-between">
            <div>
              <div class="flex flex-wrap items-center gap-3 text-3xl font-black tracking-tight sm:text-4xl">
                <span>Our Menu</span>
                <span class="text-[#f27c86]">♥</span>
              </div>
              <p class="mt-3 max-w-2xl text-sm text-slate-600">
                Tap “Add” to build your order. You can edit prices/items later.
              </p>
            </div>
            <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="cartOpen = true">Review Cart</button>
          </div>

          <div class="mb-6 flex flex-wrap gap-3 overflow-x-auto pb-2">
            <button
              v-for="option in menuFilterOptions"
              :key="option.key"
              class="inline-flex items-center gap-3 rounded-xl border px-4 py-2 text-sm font-semibold transition"
              :class="selectedMenuFilter === option.key
                ? 'border-[#f2a1aa] bg-[#fff1f3] text-slate-900 shadow-sm'
                : 'border-slate-200 bg-white/80 text-slate-700 hover:bg-slate-50'"
              type="button"
              @click="selectedMenuFilter = option.key"
            >
              {{ option.label }}
              <span
                class="inline-flex min-w-[22px] items-center justify-center rounded-xl px-2 text-xs font-semibold"
                :class="selectedMenuFilter === option.key ? 'bg-[#f7c4ca]/50 text-[#9d4b56]' : 'bg-slate-200/70 text-slate-700'"
              >
                {{ option.count }}
              </span>
            </button>
          </div>

          <div class="space-y-4">
            <div class="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h3 class="text-lg font-black tracking-tight">{{ selectedMenuLabel }}</h3>
                <div class="text-sm text-slate-600">{{ filteredMenu.length }} item(s)</div>
              </div>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <article
                v-for="item in filteredMenu"
                :key="item.id"
                class="flex h-full flex-col overflow-hidden rounded-[1.125rem] border border-slate-200 bg-white/80 shadow-[0_18px_50px_rgba(15,23,42,0.08)]"
              >
                <div class="relative aspect-[16/10] bg-slate-100/80">
                  <div
                    v-if="item.isBestSeller"
                    class="absolute left-3 top-3 rounded-xl bg-slate-950 px-3 py-1 text-xs font-black text-white"
                  >
                    Best Seller
                  </div>
                  <img
                    class="absolute inset-0 h-full w-full object-cover"
                    :src="item.image || logo"
                    :alt="item.name"
                    loading="lazy"
                  />
                </div>
                <div class="flex flex-1 flex-col p-5">
                  <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <h4 class="text-lg font-black">{{ item.name }}</h4>
                      <p class="mt-2 min-h-[72px] text-sm leading-6 text-slate-600">{{ item.description }}</p>
                    </div>
                    <div class="min-w-[120px] text-right">
                      <div class="font-black">{{ formatPeso(item.price) }}</div>
                      <div class="mt-1 text-xs text-slate-600">{{ item.sizeLabel }}</div>
                    </div>
                  </div>

                  <div class="mt-auto pt-4 flex flex-wrap gap-3">
                    <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-5 py-2 text-sm font-semibold text-slate-950 transition hover:brightness-105 shadow-sm" type="button" @click="addToCart(item)">Add</button>
                    <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-5 py-2 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="orderSingle(item)">Order this</button>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section id="how" class="py-20 bg-slate-50">
        <div class="mx-auto max-w-7xl px-4 sm:px-6">
          <h2 class="text-3xl font-black tracking-tight">How to order</h2>
          <div class="mt-8 grid gap-4 sm:grid-cols-3">
            <div class="card">
              <div class="card-inner flex items-start gap-4">
                <div class="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-sm font-black text-white">1</div>
                <div>
                  <div class="font-black">Choose your tray</div>
                  <div class="mt-2 text-sm text-slate-700/80">Add items to your cart from the menu.</div>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-inner flex items-start gap-4">
                <div class="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-sm font-black text-white">2</div>
                <div>
                  <div class="font-black">Send your order</div>
                  <div class="mt-2 text-sm text-slate-700/80">Checkout opens a message you can send to us.</div>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-inner flex items-start gap-4">
                <div class="inline-flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] text-sm font-black text-white">3</div>
                <div>
                  <div class="font-black">Wait for confirmation</div>
                  <div class="mt-2 text-sm text-slate-700/80">We’ll confirm availability, schedule, and total.</div>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 rounded-[1.125rem] border border-slate-200 bg-white/80 shadow-[0_18px_50px_rgba(15,23,42,0.08)]">
            <div class="card-inner">
              <div class="font-black">Tip</div>
              <div class="mt-2 text-sm leading-6 text-slate-700/80">
                For faster processing, include your name, delivery/pickup time, and address in the
                message.
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="about" class="py-20 bg-[linear-gradient(180deg,rgba(255,247,248,0.95),rgba(255,255,255,1))]">
        <div class="mx-auto grid max-w-7xl gap-8 px-4 sm:px-6 lg:grid-cols-[1.02fr_0.98fr] lg:items-center">
          <div class="relative">
            <div class="absolute -left-2 top-3 h-16 w-16 border-l-2 border-t-2 border-[#d45d6d]"></div>
            <div class="absolute -bottom-2 right-3 h-16 w-16 border-b-2 border-r-2 border-[#d45d6d]"></div>
            <div class="rounded-[1.75rem] border border-[#f2b3bb] bg-white/92 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.08)]">
              <div class="rounded-[1.35rem] bg-[linear-gradient(145deg,rgba(255,246,247,1),rgba(255,236,239,0.9))] p-6 shadow-[inset_0_0_0_1px_rgba(242,179,187,0.28)]">
                <img class="mx-auto h-[320px] w-full max-w-[460px] rounded-[1.1rem] object-cover" :src="bestSeller?.image || logo" alt="Baked Sushi story image" />
                <div class="mt-5 text-center text-sm font-black uppercase tracking-[0.35em] text-[#e98995]">Est. 2026</div>
              </div>
            </div>
          </div>

          <div class="max-w-2xl">
            <div class="text-sm font-black uppercase tracking-[0.28em] text-[#c96b76]">Our Story</div>
            <h2 class="mt-4 text-4xl font-black tracking-tight text-slate-900 sm:text-5xl">About</h2>
            <div class="mt-4 h-1 w-20 rounded-full bg-[#f27c86]"></div>

            <p class="mt-8 text-lg leading-8 text-slate-600">
              Baked Sushi Ozamiz serves warm, creamy, flavor-packed trays made for families, barkadas, office sharing, and
              special celebrations. We focus on comforting food that feels generous, memorable, and easy to enjoy.
            </p>
            <p class="mt-6 text-lg leading-8 text-slate-600">
              Every order is prepared with a homemade feel, from crowd-favorite baked sushi trays to rolls and rice bowls.
              Our goal is simple: make every box feel satisfying, shareable, and worthy of coming back for.
            </p>
            <p class="mt-6 text-lg leading-8 text-slate-600">
              Built for the local Ozamiz community, Baked Sushi is all about dependable flavor, generous servings, and a
              menu that brings people together around food they actually get excited about.
            </p>

            <div class="mt-8 flex flex-wrap items-center gap-3">
              <span class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 bg-white/90 text-slate-500">
                <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M13.5 22v-8.3h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.7-1.6h1.7V4c-.3 0-1.5-.1-2.8-.1-2.8 0-4.7 1.7-4.7 4.8v1.8H6.5v3.2h2.9V22h4.1z"/></svg>
              </span>
              <span class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 bg-white/90 text-slate-500">
                <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M7.7 2h8.6A5.7 5.7 0 0 1 22 7.7v8.6A5.7 5.7 0 0 1 16.3 22H7.7A5.7 5.7 0 0 1 2 16.3V7.7A5.7 5.7 0 0 1 7.7 2Zm0 2A3.7 3.7 0 0 0 4 7.7v8.6A3.7 3.7 0 0 0 7.7 20h8.6A3.7 3.7 0 0 0 20 16.3V7.7A3.7 3.7 0 0 0 16.3 4H7.7Zm4.3 4.5a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7Zm0 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3ZM17.8 6.7a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8Z"/></svg>
              </span>
              <span class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 bg-white/90 text-slate-500">
                <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M22 5.8c-.7.3-1.4.5-2.1.6a3.7 3.7 0 0 0 1.6-2c-.7.4-1.6.8-2.4 1A3.7 3.7 0 0 0 12.8 8c0 .3 0 .6.1.8A10.5 10.5 0 0 1 5 4.8a3.7 3.7 0 0 0 1.1 4.9c-.6 0-1.2-.2-1.7-.5 0 1.8 1.3 3.3 3 3.6-.3.1-.7.1-1 .1-.2 0-.5 0-.7-.1.5 1.5 1.9 2.6 3.5 2.6A7.5 7.5 0 0 1 4 17.4a10.6 10.6 0 0 0 5.8 1.7c7 0 10.8-5.8 10.8-10.8v-.5A7.6 7.6 0 0 0 22 5.8Z"/></svg>
              </span>
            </div>

            <button class="mt-10 inline-flex items-center gap-3 rounded-xl bg-[#c2191f] px-7 py-4 text-sm font-black uppercase tracking-[0.16em] text-white shadow-[0_16px_30px_rgba(194,25,31,0.26)] transition hover:brightness-105" type="button" @click="scrollTo('menu')">
              Explore
              <span aria-hidden="true">→</span>
            </button>
          </div>
        </div>
      </section>

      <section id="contact" class="py-20">
        <div class="mx-auto grid max-w-7xl gap-6 px-4 sm:px-6 lg:grid-cols-[1.3fr_0.9fr]">
          <div class="rounded-[1.125rem] border border-slate-200 bg-white/80 shadow-[0_18px_50px_rgba(15,23,42,0.08)]">
            <div class="card-inner">
              <h2 class="text-3xl font-black">Contact</h2>
              <p class="mt-3 max-w-xl text-sm text-slate-600">
                Ready to order? Message or call us and we’ll reply ASAP.
              </p>

              <div class="mt-6 flex flex-wrap gap-3">
                <a class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-5 py-3 text-sm font-semibold text-slate-950 transition hover:brightness-105 shadow-sm" :href="`tel:${phoneNumber}`">Call {{ phonePretty }}</a>
                <a class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" :href="smsLink">Text / SMS</a>
              </div>

              <div class="mt-6 grid gap-3 text-sm text-slate-600">
                <div class="flex items-center justify-between border-t border-slate-200 pt-3">
                  <span class="font-semibold text-slate-900">Facebook</span>
                  <span>Baked Sushi Ozamiz</span>
                </div>
                <div class="flex items-center justify-between border-t border-slate-200 pt-3">
                  <span class="font-semibold text-slate-900">Instagram</span>
                  <span>@bakedsushiozamiz</span>
                </div>
              </div>
            </div>
          </div>

          <div class="rounded-[1.125rem] border border-slate-200 bg-white/80 shadow-[0_18px_50px_rgba(15,23,42,0.08)]">
            <div class="card-inner">
              <div class="grid place-items-center gap-4 text-center">
                <img class="max-w-[260px] rounded-[1.125rem] border border-slate-200 bg-white/80 p-3" :src="logo" alt="Baked Sushi" />
                <div class="text-sm text-slate-600">
                  Replace this with your official QR (GCash / FB / IG) when ready.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer class="border-t border-slate-200 bg-gradient-to-b from-white to-slate-50 py-14">
        <div class="mx-auto grid max-w-7xl gap-6 px-4 sm:px-6 lg:grid-cols-[auto_1fr_auto] lg:items-center">
          <div class="flex items-center gap-3 text-slate-700" aria-label="Social links">
            <a class="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white/80 text-slate-700 transition hover:bg-slate-50" href="https://www.facebook.com/bakedsushiOzamiz" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
              <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M13.5 22v-8.3h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.7-1.6h1.7V4c-.3 0-1.5-.1-2.8-.1-2.8 0-4.7 1.7-4.7 4.8v1.8H6.5v3.2h2.9V22h4.1z"/></svg>
            </a>
            <a class="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white/80 text-slate-700 transition hover:bg-slate-50" href="#" aria-label="Instagram (update link)">
              <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M7.7 2h8.6A5.7 5.7 0 0 1 22 7.7v8.6A5.7 5.7 0 0 1 16.3 22H7.7A5.7 5.7 0 0 1 2 16.3V7.7A5.7 5.7 0 0 1 7.7 2Zm0 2A3.7 3.7 0 0 0 4 7.7v8.6A3.7 3.7 0 0 0 7.7 20h8.6A3.7 3.7 0 0 0 20 16.3V7.7A3.7 3.7 0 0 0 16.3 4H7.7Zm4.3 4.5a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7Zm0 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3ZM17.8 6.7a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8Z"/></svg>
            </a>
            <a class="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white/80 text-slate-700 transition hover:bg-slate-50" href="#" aria-label="TikTok (update link)">
              <svg viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5" aria-hidden="true"><path d="M16.6 3c.7 1.9 2 3.2 3.9 3.7v3.2c-1.7 0-3.2-.5-4.5-1.5v6.3c0 3.6-2.9 6.5-6.5 6.5S3 18.3 3 14.7s2.9-6.5 6.5-6.5c.5 0 1 .1 1.5.2v3.5c-.4-.2-.9-.3-1.5-.3-1.7 0-3.1 1.4-3.1 3.1S7.8 17.8 9.5 17.8s3.1-1.4 3.1-3.1V3h4z"/></svg>
            </a>
          </div>

          <div class="flex items-center gap-3">
            <img class="h-11 w-11 rounded-2xl border border-slate-200 bg-white/80 object-cover" :src="logo" alt="Baked Sushi" />
            <div>
              <div class="font-black leading-tight">Baked Sushi Ozamiz</div>
              <div class="text-sm text-slate-600">Scoop | Wrap | Munch | Repeat</div>
            </div>
          </div>

          <div class="grid gap-3 text-sm text-slate-600">
            <div>Built for Baked Sushi, Ozamiz.</div>
            <div class="flex flex-wrap items-center gap-2 text-slate-600">
              <a class="hover:text-slate-900" href="#top" @click.prevent="scrollTo('top')">Back to top</a>
              <span>•</span>
              <a class="hover:text-slate-900" href="#menu" @click.prevent="scrollTo('menu')">Menu</a>
              <span>•</span>
              <a class="hover:text-slate-900" href="#contact" @click.prevent="scrollTo('contact')">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </main>

    <div v-if="loginOpen" class="fixed inset-0 z-50 grid place-items-center p-6">
      <div class="absolute inset-0 bg-slate-950/50 backdrop-blur-sm" @click="loginOpen = false"></div>
      <div class="relative w-full max-w-5xl overflow-hidden rounded-[1.5rem] border border-white/70 bg-white/80 shadow-[0_40px_120px_rgba(15,23,42,0.15)]">
        <button
          class="absolute right-4 top-4 inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-xl text-slate-700"
          type="button"
          aria-label="Close"
          @click="loginOpen = false"
        >
          ×
        </button>
        <div class="grid min-h-[560px] grid-cols-1 gap-0 lg:grid-cols-[1.05fr_0.95fr]">
          <div class="p-8 sm:p-10">
            <div class="flex items-center gap-3">
              <img class="h-11 w-11 rounded-2xl border border-slate-200 bg-white/80 object-cover" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="font-black">Baked Sushi</div>
                <div class="text-xs text-slate-600">Scoop | Wrap | Munch | Repeat</div>
              </div>
            </div>

            <div class="mt-8 text-3xl font-black tracking-tight">Welcome back</div>
            <div class="mt-3 text-sm text-slate-600">Sign in to continue</div>

            <div class="mt-8 grid gap-3">
              <button class="inline-flex w-full items-center justify-center rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:brightness-110" type="button" @click="goDashboard">Continue with Google</button>
              <button class="inline-flex w-full items-center justify-center rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:brightness-110" type="button" @click="goDashboard">Continue with Microsoft</button>
            </div>

            <div class="mt-8 grid gap-3 text-center text-xs uppercase tracking-[0.25em] text-slate-500 sm:grid-cols-[1fr_auto_1fr] sm:items-center sm:text-left">
              <span class="hidden sm:block h-px bg-slate-200"></span>
              <span>or</span>
              <span class="hidden sm:block h-px bg-slate-200"></span>
            </div>

            <form class="mt-8 grid gap-4" @submit.prevent="goDashboard">
              <label class="grid gap-2 text-sm font-semibold text-slate-700">
                <span class="uppercase tracking-[0.12em] text-xs text-slate-600">Email</span>
                <input
                  v-model="loginEmail"
                  class="h-11 rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm outline-none transition focus:border-[#f27c86] focus:ring-2 focus:ring-[#f27c86]/20"
                  type="email"
                  autocomplete="email"
                  placeholder="you@example.com"
                />
              </label>

              <label class="grid gap-2 text-sm font-semibold text-slate-700">
                <span class="uppercase tracking-[0.12em] text-xs text-slate-600">Password</span>
                <div class="relative">
                  <input
                    v-model="loginPassword"
                    :type="showLoginPassword ? 'text' : 'password'"
                    class="h-11 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 pr-20 text-sm outline-none transition focus:border-[#f27c86] focus:ring-2 focus:ring-[#f27c86]/20"
                    autocomplete="current-password"
                    placeholder="••••••••"
                  />
                  <button
                    class="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-700"
                    type="button"
                    @click="showLoginPassword = !showLoginPassword"
                  >
                    {{ showLoginPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
              </label>

              <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <label class="inline-flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <input type="checkbox" v-model="loginRemember" class="h-4 w-4 rounded border-slate-300 text-[#f27c86] focus:ring-[#f27c86]" />
                  Remember me
                </label>
                <a class="text-sm font-semibold text-[#f27c86] hover:underline" href="#" @click.prevent="noop">Forgot password?</a>
              </div>

              <button class="inline-flex w-full items-center justify-center rounded-xl bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-5 py-3 text-sm font-semibold text-slate-950 shadow-sm transition hover:brightness-105" type="submit">Sign in</button>
            </form>
          </div>

          <div class="relative bg-gradient-to-br from-[#fa8072] to-[#d6a64a] text-white/95">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.16),transparent_42%),radial-gradient(circle_at_80%_40%,rgba(255,255,255,0.12),transparent_46%),radial-gradient(circle_at_65%_85%,rgba(255,255,255,0.1),transparent_48%)] opacity-90"></div>
            <div class="relative grid h-full place-items-center gap-4 p-10 text-center">
              <img class="max-w-[320px] object-contain drop-shadow-[0_18px_40px_rgba(15,23,42,0.35)]" :src="logo" alt="" />
              <div class="text-3xl font-black">Premium Baked Sushi</div>
              <div class="text-sm">Order gifts, trays, and party sets in minutes.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="cartOpen" class="fixed inset-0 z-50 grid place-items-center">
      <div class="absolute inset-0 bg-slate-950/50 backdrop-blur-sm" @click="cartOpen = false"></div>
      <div class="relative ml-auto flex h-full w-full max-w-[420px] flex-col bg-white/95 border-l border-slate-200 shadow-[0_40px_120px_rgba(15,23,42,0.12)]">
        <div class="flex items-center justify-between gap-4 border-b border-slate-200 bg-white/80 px-5 py-4">
          <div>
            <div class="text-lg font-black">Your cart</div>
            <div class="text-sm text-slate-600">{{ cartCount }} item(s)</div>
          </div>
          <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="cartOpen = false">Close</button>
        </div>

        <div v-if="!cart.length" class="p-5">
          <div class="card">
            <div class="card-inner space-y-3">
              <div class="text-lg font-black">Cart is empty</div>
              <div class="text-sm text-slate-600">Add items from the menu to start your order.</div>
              <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-5 py-3 text-sm font-semibold text-slate-950 transition hover:brightness-105 shadow-sm" type="button" @click="goMenu()">Browse menu</button>
            </div>
          </div>
        </div>

        <div v-else class="flex h-full flex-col overflow-hidden">
          <div class="flex-1 overflow-y-auto p-5 space-y-4">
            <div v-for="line in cart" :key="line.id" class="card">
              <div class="card-inner flex items-center justify-between gap-4">
                <div>
                  <div class="font-black">{{ line.name }}</div>
                  <div class="text-sm text-slate-600">{{ formatPeso(line.price) }} each</div>
                </div>
                <div class="flex items-center gap-2">
                  <button class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white/90 px-0 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="dec(line.id)">-</button>
                  <div class="min-w-[26px] text-center font-black">{{ line.qty }}</div>
                  <button class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white/90 px-0 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="inc(line.id)">+</button>
                </div>
              </div>
            </div>
          </div>

          <div class="border-t border-slate-200 bg-white/90 p-5">
            <div class="space-y-4">
              <div class="flex items-center justify-between text-sm font-semibold text-slate-700">
                <span>Subtotal</span>
                <span>{{ formatPeso(cartTotal) }}</span>
              </div>
              <div class="text-sm text-slate-600">Delivery and taxes calculated on message.</div>
              <div class="flex flex-wrap gap-3">
                <button class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white/90 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-300 hover:bg-white shadow-sm" type="button" @click="clearCart()">Clear</button>
                <a class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-gradient-to-r from-[#f27c86] to-[#d6a64a] px-5 py-3 text-sm font-semibold text-slate-950 transition hover:brightness-105 shadow-sm" :href="checkoutLink">Checkout</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.png?url'
import heroVideoUrl from '~/assets/digital_assets/mp_.mp4?url'

const logo = logoUrl
const heroVideo = heroVideoUrl
const router = useRouter()

type MenuItem = {
  id: string
  category: Category
  name: string
  description: string
  price: number
  sizeLabel: string
  image?: string
  isBestSeller?: boolean
}

type CartLine = {
  id: string
  name: string
  price: number
  qty: number
}

useHead({
  title: 'Baked Sushi - Ozamiz',
  meta: [
    {
      name: 'description',
      content: 'Baked Sushi Ozamiz - menu, prices, and easy ordering.'
    }
  ]
})

type Category = 'Large Portion Servings' | 'Rolls and Salad' | 'Rice Bowls'
type MenuFilter = 'All Products' | Category

const phoneNumber = '09551834288'
const phonePretty = '0955 183 4288'

const categoryOrder: Category[] = ['Large Portion Servings', 'Rolls and Salad', 'Rice Bowls']

const menu: MenuItem[] = [
  {
    id: 'spring-rolls-24',
    category: 'Rolls and Salad',
    name: 'Spring Rolls',
    description: 'Crisp, fresh, and crowd-pleasing.',
    price: 400,
    sizeLabel: '24 pcs'
  },
  {
    id: 'kimbap-bilao-50',
    category: 'Large Portion Servings',
    name: 'Kimbap Rolls Bilao',
    description: 'A festive tray of bite-sized goodness.',
    price: 600,
    sizeLabel: '50 pcs'
  },
  {
    id: 'baked-sushi-duo',
    category: 'Large Portion Servings',
    name: 'Baked Sushi Duo',
    description: 'Creamy, savory, and seriously addicting.',
    price: 550,
    sizeLabel: 'Large tray',
    isBestSeller: true
  },
  {
    id: 'fishcake',
    category: 'Rolls and Salad',
    name: 'Fishcake',
    description: 'Comforting bites with a tasty kick.',
    price: 0,
    sizeLabel: 'Ask for price'
  }
]

const bestSeller = computed(() => menu.find((m) => m.isBestSeller))
const selectedMenuFilter = ref<MenuFilter>('All Products')
const productShowcase = computed(() => [
  ...menu.map((item) => ({ ...item, trackKey: 'a' })),
  ...menu.map((item) => ({ ...item, trackKey: 'b' }))
])

const cartOpen = ref(false)
const loginOpen = ref(false)
const cart = ref<CartLine[]>([])

const loginEmail = ref('')
const loginPassword = ref('')
const loginRemember = ref(true)
const showLoginPassword = ref(false)

const cartCount = computed(() => cart.value.reduce((sum, line) => sum + line.qty, 0))
const cartTotal = computed(() => cart.value.reduce((sum, line) => sum + line.price * line.qty, 0))

const smsLink = computed(() => {
  const body = encodeURIComponent('Hi! I want to order Baked Sushi. Here are my details:')
  return `sms:${phoneNumber}?body=${body}`
})

function formatPeso(value: number) {
  if (!value) return '₱ —'
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value)
}

function slug(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
}

const menuByCategory = computed<Record<Category, MenuItem[]>>(() => {
  const grouped: Record<Category, MenuItem[]> = {
    'Large Portion Servings': [],
    'Rolls and Salad': [],
    'Rice Bowls': []
  }
  for (const item of menu) grouped[item.category].push(item)
  return grouped
})

const menuFilterOptions = computed(() => [
  { key: 'All Products' as const, label: 'All Products', count: menu.length },
  ...categoryOrder.map((category) => ({
    key: category,
    label: category,
    count: menuByCategory.value[category].length
  }))
])

const filteredMenu = computed(() => {
  if (selectedMenuFilter.value === 'All Products') return menu
  return menuByCategory.value[selectedMenuFilter.value]
})

const selectedMenuLabel = computed(() => selectedMenuFilter.value)

function scrollTo(id: string) {
  const el = document.getElementById(id)
  el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function noop() {}

function goDashboard() {
  loginOpen.value = false
  router.push('/dashboard')
}

function addToCart(item: MenuItem) {
  const existing = cart.value.find((l) => l.id === item.id)
  if (existing) {
    existing.qty += 1
    return
  }
  cart.value.push({ id: item.id, name: item.name, price: item.price, qty: 1 })
}

function inc(id: string) {
  const line = cart.value.find((l) => l.id === id)
  if (line) line.qty += 1
}

function dec(id: string) {
  const line = cart.value.find((l) => l.id === id)
  if (!line) return
  line.qty -= 1
  if (line.qty <= 0) cart.value = cart.value.filter((l) => l.id !== id)
}

function clearCart() {
  cart.value = []
}

function goMenu() {
  cartOpen.value = false
  scrollTo('menu')
}

function orderSingle(item: MenuItem) {
  addToCart(item)
  cartOpen.value = true
}

function buildOrderMessage(lines: CartLine[]) {
  const hasPricedItems = lines.some((l) => l.price > 0)
  const list = lines
    .map((l) => {
      const pricePart = l.price > 0 ? ` @ ${formatPeso(l.price)}` : ''
      return `- ${l.qty}x ${l.name}${pricePart}`
    })
    .join('\n')

  const totalLine = hasPricedItems ? `\n\nSubtotal: ${formatPeso(cartTotal.value)}` : ''
  return `Hi! I want to order:\n${list}${totalLine}\n\nName:\nPickup/Delivery time:\nAddress:`
}

const checkoutLink = computed(() => {
  const message = buildOrderMessage(cart.value)
  return `sms:${phoneNumber}?body=${encodeURIComponent(message)}`
})

function quickOrder() {
  cartOpen.value = true
}
</script>

<!-- Styles moved to `ui/app/assets/css/main.css` (centralized Tailwind component classes) -->
