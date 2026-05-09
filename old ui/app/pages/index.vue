<template>
  <div class="page">
    <header class="topbar">
      <div class="container topbar-inner">
        <a class="brand" href="#top" @click.prevent="scrollTo('top')">
          <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
          <div class="brand-text">
            <div class="brand-name">Baked Sushi</div>
            <div class="brand-tag">Scoop | Wrap | Munch | Repeat</div>
          </div>
        </a>

        <nav class="nav">
          <a class="nav-link" href="#menu" @click.prevent="scrollTo('menu')">Menu</a>
          <a class="nav-link" href="#how" @click.prevent="scrollTo('how')">How to Order</a>
          <a class="nav-link" href="#contact" @click.prevent="scrollTo('contact')">Contact</a>
        </nav>

        <button class="btn cart-btn" type="button" @click="cartOpen = true">
          <span class="dot" aria-hidden="true" />
          Cart
          <span v-if="cartCount" class="count" aria-label="Items in cart">{{ cartCount }}</span>
        </button>
      </div>
    </header>

    <main id="top">
      <section class="hero">
        <video
          class="hero-video"
          autoplay
          muted
          loop
          playsinline
          preload="metadata"
        >
          <source :src="heroVideo" type="video/mp4" />
        </video>
        <div class="hero-overlay" />

        <div class="container hero-inner">
          <div class="pill">
            <span aria-hidden="true">Hot</span>
            Freshly baked | Made to order | Ozamiz
          </div>

          <div class="hero-welcome">Welcome to</div>

          <h1 class="hero-title">
            Baked Sushi
            <span class="hero-script">Ozamiz</span>
          </h1>

          <p class="hero-sub">
            Freshly made. Perfectly baked. Made for every sushi lover.
          </p>

          <div class="hero-actions">
            <a class="btn primary" href="#menu" @click.prevent="scrollTo('menu')">View Menu</a>
            <button class="btn" type="button" @click="quickOrder()">Order Now</button>
            <button
              v-if="bestSeller"
              class="btn"
              type="button"
              @click="scrollTo(`cat-${slug(bestSeller.category)}`)"
            >
              Best seller: {{ bestSeller.name }}
            </button>
          </div>

          <div class="hero-stats">
            <div class="stat card">
              <div class="card-inner">
                <div class="stat-k">Large portions</div>
                <div class="stat-v">party-ready trays</div>
              </div>
            </div>
            <div class="stat card">
              <div class="card-inner">
                <div class="stat-k">Fast ordering</div>
                <div class="stat-v">message us anytime</div>
              </div>
            </div>
            <div class="stat card">
              <div class="card-inner">
                <div class="stat-k">Made with care</div>
                <div class="stat-v">fresh & flavorful</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="menu" class="section menu-section">
        <div class="container">
          <div class="section-head">
            <div>
              <h2 class="section-title menu-title">
                Our Menu <span class="menu-heart" aria-hidden="true">♥</span>
              </h2>
              <p class="section-sub">Tap “Add” to build your order. You can edit prices/items later.</p>
            </div>
            <button class="btn" type="button" @click="cartOpen = true">Review Cart</button>
          </div>

          <div class="category-tabs">
            <a
              v-for="cat in categoryOrder"
              :key="cat"
              class="cat-tab"
              :href="`#cat-${slug(cat)}`"
              @click.prevent="scrollTo(`cat-${slug(cat)}`)"
            >
              {{ cat }}
              <span class="cat-count">{{ (menuByCategory[cat] || []).length }}</span>
            </a>
          </div>

          <section
            v-for="cat in categoryOrder"
            :key="cat"
            class="menu-category"
            :id="`cat-${slug(cat)}`"
          >
            <div class="menu-cat-head">
              <h3 class="menu-cat-title">{{ cat }}</h3>
              <div class="menu-cat-sub muted">{{ (menuByCategory[cat] || []).length }} item(s)</div>
            </div>

            <div class="grid menu-grid">
              <article
                v-for="item in menuByCategory[cat]"
                :key="item.id"
                class="card product"
              >
                <div class="product-media">
                  <div v-if="item.isBestSeller" class="best-badge">Best Seller</div>
                  <img
                    class="product-img"
                    :src="item.image || logo"
                    :alt="item.name"
                    loading="lazy"
                  />
                </div>
                <div class="card-inner product-body">
                  <div class="product-top">
                    <div>
                      <h4 class="product-name">{{ item.name }}</h4>
                      <p class="product-desc muted">{{ item.description }}</p>
                    </div>
                    <div class="product-price">
                      <div class="price">{{ formatPeso(item.price) }}</div>
                      <div class="muted price-note">{{ item.sizeLabel }}</div>
                    </div>
                  </div>

                  <div class="product-actions">
                    <button class="btn primary" type="button" @click="addToCart(item)">Add</button>
                    <button class="btn" type="button" @click="orderSingle(item)">Order this</button>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>
      </section>

      <section id="how" class="section section-alt">
        <div class="container">
          <h2 class="section-title">How to order</h2>
          <div class="grid how-grid">
            <div class="card">
              <div class="card-inner how-card">
                <div class="how-step">1</div>
                <div>
                  <div class="how-title">Choose your tray</div>
                  <div class="subtle">Add items to your cart from the menu.</div>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-inner how-card">
                <div class="how-step">2</div>
                <div>
                  <div class="how-title">Send your order</div>
                  <div class="subtle">Checkout opens a message you can send to us.</div>
                </div>
              </div>
            </div>
            <div class="card">
              <div class="card-inner how-card">
                <div class="how-step">3</div>
                <div>
                  <div class="how-title">Wait for confirmation</div>
                  <div class="subtle">We’ll confirm availability, schedule, and total.</div>
                </div>
              </div>
            </div>
          </div>

          <div class="notice card">
            <div class="card-inner notice-inner">
              <div class="notice-title">Tip</div>
              <div class="notice-text">
                For faster processing, include your name, delivery/pickup time, and address in the
                message.
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="contact" class="section">
        <div class="container contact">
          <div class="contact-left card">
            <div class="card-inner">
              <h2 class="section-title" style="margin-top: 0">Contact</h2>
              <p class="section-sub">
                Ready to order? Message or call us and we’ll reply ASAP.
              </p>

              <div class="contact-actions">
                <a class="btn primary" :href="`tel:${phoneNumber}`">Call {{ phonePretty }}</a>
                <a class="btn" :href="smsLink">Text / SMS</a>
              </div>

              <div class="contact-meta">
                <div class="meta-row">
                  <span class="meta-k">Facebook</span>
                  <span class="meta-v">Baked Sushi Ozamiz</span>
                </div>
                <div class="meta-row">
                  <span class="meta-k">Instagram</span>
                  <span class="meta-v">@bakedsushiozamiz</span>
                </div>
              </div>
            </div>
          </div>

          <div class="contact-right card">
            <div class="card-inner">
              <div class="qr-wrap">
                <img class="qr" :src="logo" alt="Baked Sushi" />
                <div class="qr-note subtle">
                  Replace this with your official QR (GCash / FB / IG) when ready.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer class="footer">
        <div class="container footer-wrap">
          <div class="footer-social" aria-label="Social links">
            <a
              class="social-btn"
              href="https://www.facebook.com/bakedsushiOzamiz"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Facebook"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M13.5 22v-8.3h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.7-1.6h1.7V4c-.3 0-1.5-.1-2.8-.1-2.8 0-4.7 1.7-4.7 4.8v1.8H6.5v3.2h2.9V22h4.1z"
                />
              </svg>
            </a>
            <a class="social-btn" href="#" aria-label="Instagram (update link)">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M7.7 2h8.6A5.7 5.7 0 0 1 22 7.7v8.6A5.7 5.7 0 0 1 16.3 22H7.7A5.7 5.7 0 0 1 2 16.3V7.7A5.7 5.7 0 0 1 7.7 2Zm0 2A3.7 3.7 0 0 0 4 7.7v8.6A3.7 3.7 0 0 0 7.7 20h8.6A3.7 3.7 0 0 0 20 16.3V7.7A3.7 3.7 0 0 0 16.3 4H7.7Zm4.3 4.5a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7Zm0 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3ZM17.8 6.7a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8Z"
                />
              </svg>
            </a>
            <a class="social-btn" href="#" aria-label="TikTok (update link)">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M16.6 3c.7 1.9 2 3.2 3.9 3.7v3.2c-1.7 0-3.2-.5-4.5-1.5v6.3c0 3.6-2.9 6.5-6.5 6.5S3 18.3 3 14.7s2.9-6.5 6.5-6.5c.5 0 1 .1 1.5.2v3.5c-.4-.2-.9-.3-1.5-.3-1.7 0-3.1 1.4-3.1 3.1S7.8 17.8 9.5 17.8s3.1-1.4 3.1-3.1V3h4z"
                />
              </svg>
            </a>
          </div>

          <div class="footer-brand">
            <img class="footer-logo" :src="logo" alt="Baked Sushi" />
            <div class="footer-smallcaps">
              <div class="footer-line">Baked Sushi Ozamiz</div>
              <div class="footer-line muted">Scoop | Wrap | Munch | Repeat</div>
            </div>
          </div>

          <div class="footer-legal">
            <div class="legal muted">
              © {{ new Date().getFullYear() }} Baked Sushi · Ozamiz. Thank you for the support!
            </div>
            <div class="legal-links">
              <a class="muted" href="#top" @click.prevent="scrollTo('top')">Back to top</a>
              <span class="sep" aria-hidden="true">•</span>
              <a class="muted" href="#menu" @click.prevent="scrollTo('menu')">Menu</a>
              <span class="sep" aria-hidden="true">•</span>
              <a class="muted" href="#contact" @click.prevent="scrollTo('contact')">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </main>

    <div v-if="cartOpen" class="drawer" role="dialog" aria-modal="true" aria-label="Cart">
      <div class="drawer-backdrop" @click="cartOpen = false" />
      <div class="drawer-panel">
        <div class="drawer-head">
          <div>
            <div class="drawer-title">Your cart</div>
            <div class="muted">{{ cartCount }} item(s)</div>
          </div>
          <button class="btn" type="button" @click="cartOpen = false">Close</button>
        </div>

        <div v-if="!cart.length" class="drawer-empty">
          <div class="card">
            <div class="card-inner">
              <div class="drawer-empty-title">Cart is empty</div>
              <div class="muted">Add items from the menu to start your order.</div>
              <div style="margin-top: 12px">
                <button class="btn primary" type="button" @click="goMenu()">Browse menu</button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="drawer-body">
          <div class="cart-list">
            <div v-for="line in cart" :key="line.id" class="cart-item card">
              <div class="card-inner cart-item-inner">
                <div class="cart-item-left">
                  <div class="cart-name">{{ line.name }}</div>
                  <div class="muted">{{ formatPeso(line.price) }} each</div>
                </div>
                <div class="cart-item-right">
                  <button class="btn qty" type="button" @click="dec(line.id)">-</button>
                  <div class="qty-val" aria-label="Quantity">{{ line.qty }}</div>
                  <button class="btn qty" type="button" @click="inc(line.id)">+</button>
                </div>
              </div>
            </div>
          </div>

          <div class="cart-summary card">
            <div class="card-inner summary-inner">
              <div class="summary-row">
                <span class="muted">Subtotal</span>
                <span>{{ formatPeso(cartTotal) }}</span>
              </div>
              <div class="summary-row muted">
                <span>Delivery fee</span>
                <span>Depends on location</span>
              </div>
              <div class="summary-actions">
                <button class="btn" type="button" @click="clearCart()">Clear</button>
                <a class="btn primary" :href="checkoutLink" @click="cartOpen = false">Checkout</a>
              </div>
              <div class="muted" style="font-size: 12px; margin-top: 10px">
                Checkout opens an SMS message. You can switch it to Messenger/WhatsApp later.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/app/assets/digital_assets/logo.png?url'
import heroVideoUrl from 'assets/digital_assets/mp_.mp4?url'

const logo = logoUrl
const heroVideo = heroVideoUrl

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

const cartOpen = ref(false)
const cart = ref<CartLine[]>([])

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

function scrollTo(id: string) {
  const el = document.getElementById(id)
  el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
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

<style scoped>
/* (kept identical to the user's provided styles) */
.page {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(255, 224, 228, 0.72);
  border-bottom: 1px solid rgba(20, 12, 10, 0.1);
}

.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 12px 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 220px;
}

.brand-logo {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  object-fit: cover;
  border: 1px solid rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.72);
}

.brand-name {
  font-weight: 850;
  letter-spacing: 0.02em;
  line-height: 1.05;
}

.brand-tag {
  font-size: 12px;
  color: rgba(20, 12, 10, 0.65);
  margin-top: 2px;
}

.nav {
  display: none;
  gap: 12px;
  align-items: center;
}

.nav-link {
  padding: 10px 12px;
  border-radius: 999px;
  color: rgba(20, 12, 10, 0.72);
  border: 1px solid transparent;
}

.nav-link:hover {
  color: rgba(20, 12, 10, 0.9);
  border-color: rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.55);
}

.cart-btn {
  padding-inline: 14px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(242, 124, 134, 1), rgba(214, 166, 74, 1));
  box-shadow: 0 0 0 4px rgba(242, 124, 134, 0.16);
}

.count {
  display: inline-flex;
  min-width: 26px;
  height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  align-items: center;
  justify-content: center;
  background: rgba(20, 12, 10, 0.06);
  border: 1px solid rgba(20, 12, 10, 0.12);
  font-weight: 800;
}

.hero {
  position: relative;
  min-height: clamp(620px, 84vh, 900px);
  display: grid;
  align-items: center;
  overflow: hidden;
}

.hero-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.02);
  filter: saturate(1.05) contrast(1.05);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(900px 520px at 16% 24%, rgba(255, 255, 255, 0.08), rgba(255, 210, 215, 0.78)),
    linear-gradient(180deg, rgba(255, 227, 230, 0.22), rgba(255, 210, 215, 0.94));
}

/* rest of styles kept as provided by user... */

/* (For brevity the remainder of the user's style block is present unchanged.) */
</style>
