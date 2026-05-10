<template>
  <div class="page">
    <AppTopbar>
      <template #left>
        <a class="brand" href="#top" @click.prevent="scrollTo('top')">
          <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
          <div class="brand-text">
            <div class="brand-name">Baked Sushi</div>
            <div class="brand-tag">Scoop | Wrap | Munch | Repeat</div>
          </div>
        </a>
      </template>

      <template #center>
        <nav class="nav">
          <a class="nav-link" href="#menu" @click.prevent="scrollTo('menu')">Menu</a>
          <a class="nav-link" href="#how" @click.prevent="scrollTo('how')">How to Order</a>
          <a class="nav-link" href="#contact" @click.prevent="scrollTo('contact')">Contact</a>
        </nav>
      </template>

      <template #right>
        <button class="btn login-btn" type="button" @click="loginOpen = true">Login</button>

        <button class="btn cart-btn" type="button" @click="cartOpen = true">
          <span class="dot" aria-hidden="true" />
          Cart
          <span v-if="cartCount" class="count" aria-label="Items in cart">{{ cartCount }}</span>
        </button>
      </template>
    </AppTopbar>

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

    <div v-if="loginOpen" class="auth" role="dialog" aria-modal="true" aria-label="Login">
      <div class="auth-backdrop" @click="loginOpen = false" />
      <div class="auth-modal">
        <button class="auth-close" type="button" aria-label="Close" @click="loginOpen = false">×</button>

        <div class="auth-inner">
          <div class="auth-left">
            <div class="auth-brand">
              <img class="auth-logo" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="auth-name">Baked Sushi</div>
                <div class="auth-tag muted">Scoop | Wrap | Munch | Repeat</div>
              </div>
            </div>

            <div class="auth-title">Welcome back</div>
            <div class="auth-sub muted">Sign in to continue</div>

            <div class="auth-social">
              <button class="btn auth-social-btn" type="button" @click="goDashboard">Continue with Google</button>
              <button class="btn auth-social-btn" type="button" @click="goDashboard">Continue with Microsoft</button>
            </div>

            <div class="auth-divider" role="separator">
              <span />
              <span class="auth-divider-text">or</span>
              <span />
            </div>

            <form class="auth-form" @submit.prevent="goDashboard">
              <label class="auth-field">
                <span class="auth-label">Email</span>
                <input v-model="loginEmail" class="auth-input" type="email" autocomplete="email" placeholder="you@example.com" />
              </label>

              <label class="auth-field">
                <span class="auth-label">Password</span>
                <div class="auth-input-wrap">
                  <input
                    v-model="loginPassword"
                    class="auth-input"
                    :type="showLoginPassword ? 'text' : 'password'"
                    autocomplete="current-password"
                    placeholder="••••••••"
                  />
                  <button class="auth-ghost" type="button" @click="showLoginPassword = !showLoginPassword">
                    {{ showLoginPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
              </label>

              <div class="auth-row">
                <label class="auth-check">
                  <input v-model="loginRemember" type="checkbox" />
                  <span>Remember me</span>
                </label>
                <a class="auth-link" href="#" @click.prevent="noop">Forgot password?</a>
              </div>

              <button class="btn primary auth-submit" type="submit">Sign in</button>
            </form>
          </div>

          <div class="auth-right">
            <div class="auth-right-inner">
              <img class="auth-right-logo" :src="logo" alt="" />
              <div class="auth-right-title">Premium Baked Sushi</div>
            </div>
          </div>
        </div>
      </div>
    </div>

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

<style scoped>
.page {
  min-height: 100vh;
  color: rgba(20, 12, 10, 0.92);
  background: radial-gradient(1200px 700px at 20% -10%, rgba(255, 224, 228, 0.9), rgba(255, 255, 255, 0)),
    linear-gradient(180deg, rgba(255, 243, 245, 1), rgba(255, 255, 255, 1));
}

.container {
  width: 100%;
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 18px;
}

.muted {
  color: rgba(20, 12, 10, 0.62);
}

.subtle {
  color: rgba(20, 12, 10, 0.72);
  font-size: 14px;
  line-height: 1.35;
}

.grid {
  display: grid;
  gap: 14px;
}

.card {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(20, 12, 10, 0.12);
  border-radius: 18px;
  box-shadow: 0 18px 50px rgba(20, 12, 10, 0.08);
  backdrop-filter: blur(10px);
}

.card-inner {
  padding: 14px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: 42px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid rgba(20, 12, 10, 0.16);
  background: rgba(255, 255, 255, 0.72);
  color: rgba(20, 12, 10, 0.92);
  font-weight: 750;
  letter-spacing: 0.01em;
  transition: transform 120ms ease, background 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
  text-decoration: none;
}

.btn:hover {
  border-color: rgba(20, 12, 10, 0.22);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 10px 24px rgba(20, 12, 10, 0.12);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0);
  box-shadow: none;
}

.btn.primary {
  border-color: rgba(242, 124, 134, 0.35);
  background: linear-gradient(135deg, rgba(242, 124, 134, 1), rgba(214, 166, 74, 1));
  color: rgba(20, 12, 10, 0.96);
}

.btn.primary:hover {
  border-color: rgba(242, 124, 134, 0.5);
  box-shadow: 0 16px 30px rgba(242, 124, 134, 0.22);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 220px;
  text-decoration: none;
  color: inherit;
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
  font-weight: 900;
  letter-spacing: 0.02em;
  line-height: 1.05;
}

.brand-tag {
  font-size: 12px;
  color: rgba(20, 12, 10, 0.65);
  margin-top: 2px;
}

.nav-link {
  padding: 10px 12px;
  border-radius: 999px;
  color: rgba(20, 12, 10, 0.72);
  border: 1px solid transparent;
  text-decoration: none;
}

.nav-link:hover {
  color: rgba(20, 12, 10, 0.92);
  border-color: rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.55);
}

.cart-btn {
  padding-inline: 14px;
}

.login-btn {
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
  font-weight: 850;
}

.hero {
  position: relative;
  min-height: min(92vh, 780px);
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
  transform: scale(1.03);
  filter: saturate(1.1) contrast(1.08);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(900px 520px at 16% 24%, rgba(255, 255, 255, 0.14), rgba(255, 210, 215, 0.64)),
    linear-gradient(180deg, rgba(255, 227, 230, 0.22), rgba(255, 210, 215, 0.88));
}

.hero-inner {
  position: relative;
  z-index: 2;
  padding: 34px 0 42px;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(20, 12, 10, 0.12);
  font-weight: 750;
  width: fit-content;
}

.pill span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 22px;
  padding: 0 10px;
  border-radius: 999px;
  background: rgba(20, 12, 10, 0.9);
  color: rgba(255, 255, 255, 0.95);
  font-weight: 900;
  font-size: 12px;
  letter-spacing: 0.04em;
}

.hero-welcome {
  margin-top: 16px;
  font-weight: 800;
  color: rgba(20, 12, 10, 0.74);
  letter-spacing: 0.01em;
}

.hero-title {
  margin-top: 6px;
  font-size: clamp(40px, 6vw, 64px);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-weight: 950;
}

.hero-script {
  display: inline-block;
  margin-left: 10px;
  font-weight: 900;
  font-style: italic;
  letter-spacing: 0.01em;
  color: rgba(242, 124, 134, 0.95);
  text-shadow: 0 14px 40px rgba(242, 124, 134, 0.25);
}

.hero-sub {
  margin-top: 10px;
  max-width: 52ch;
  font-size: 16px;
  color: rgba(20, 12, 10, 0.72);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
}

.hero-stats {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin-top: 18px;
  max-width: 720px;
}

.stat-k {
  font-weight: 900;
}

.stat-v {
  margin-top: 2px;
  color: rgba(20, 12, 10, 0.68);
  font-size: 13px;
}

.section {
  padding: 44px 0;
}

.section-alt {
  background: linear-gradient(180deg, rgba(255, 239, 242, 1), rgba(255, 255, 255, 1));
}

.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.section-title {
  font-size: 28px;
  line-height: 1.1;
  font-weight: 950;
  letter-spacing: -0.02em;
}

.section-sub {
  margin-top: 6px;
  color: rgba(20, 12, 10, 0.62);
}

.menu-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.menu-heart {
  color: rgba(242, 124, 134, 1);
}

.category-tabs {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 8px 2px 12px;
  margin-bottom: 12px;
  scroll-snap-type: x mandatory;
}

.cat-tab {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 999px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.72);
  text-decoration: none;
  color: inherit;
  white-space: nowrap;
  scroll-snap-align: start;
}

.cat-count {
  display: inline-flex;
  min-width: 22px;
  height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  align-items: center;
  justify-content: center;
  background: rgba(20, 12, 10, 0.06);
  border: 1px solid rgba(20, 12, 10, 0.12);
  font-size: 12px;
  font-weight: 850;
}

.menu-category {
  margin-top: 20px;
}

.menu-cat-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}

.menu-cat-title {
  font-size: 18px;
  font-weight: 950;
}

.menu-grid {
  grid-template-columns: 1fr;
}

.product {
  overflow: hidden;
}

.product-media {
  position: relative;
  background: rgba(255, 255, 255, 0.4);
  border-bottom: 1px solid rgba(20, 12, 10, 0.1);
  aspect-ratio: 16 / 10;
}

.best-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2;
  padding: 8px 10px;
  border-radius: 999px;
  background: rgba(20, 12, 10, 0.88);
  color: rgba(255, 255, 255, 0.96);
  font-weight: 900;
  font-size: 12px;
}

.product-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(1.02) contrast(1.02);
}

.product-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.product-name {
  font-weight: 950;
  font-size: 16px;
  line-height: 1.2;
}

.product-desc {
  margin-top: 6px;
  font-size: 13px;
  line-height: 1.35;
}

.product-price {
  text-align: right;
  min-width: 120px;
}

.price {
  font-weight: 950;
}

.price-note {
  margin-top: 2px;
  font-size: 12px;
}

.product-actions {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.how-grid {
  grid-template-columns: 1fr;
  margin-top: 14px;
}

.how-card {
  display: flex;
  gap: 14px;
  align-items: center;
}

.how-step {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 950;
  background: linear-gradient(135deg, rgba(242, 124, 134, 1), rgba(214, 166, 74, 1));
}

.how-title {
  font-weight: 950;
}

.notice {
  margin-top: 14px;
}

.notice-inner {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.notice-title {
  font-weight: 950;
}

.contact {
  display: grid;
  gap: 14px;
}

.contact-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.contact-meta {
  margin-top: 16px;
  display: grid;
  gap: 10px;
}

.meta-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
  border-top: 1px dashed rgba(20, 12, 10, 0.16);
  padding-top: 10px;
}

.meta-k {
  font-weight: 850;
}

.qr-wrap {
  display: grid;
  place-items: center;
  text-align: center;
  gap: 10px;
}

.qr {
  width: min(260px, 100%);
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
}

.footer {
  padding: 26px 0 40px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 1), rgba(255, 239, 242, 1));
  border-top: 1px solid rgba(20, 12, 10, 0.08);
}

.footer-wrap {
  display: grid;
  gap: 14px;
  align-items: center;
}

.footer-social {
  display: flex;
  gap: 10px;
}

.social-btn {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.76);
  color: rgba(20, 12, 10, 0.82);
}

.social-btn svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer-logo {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.12);
}

.footer-line {
  font-weight: 900;
  line-height: 1.1;
}

.footer-legal {
  display: grid;
  gap: 10px;
}

.legal-links {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.sep {
  opacity: 0.5;
}

.drawer {
  position: fixed;
  inset: 0;
  z-index: 70;
}

.drawer-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(20, 12, 10, 0.36);
  backdrop-filter: blur(6px);
}

.drawer-panel {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: min(420px, 92vw);
  background: rgba(255, 245, 247, 0.92);
  border-left: 1px solid rgba(20, 12, 10, 0.12);
  display: grid;
  grid-template-rows: auto 1fr;
}

.auth {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: grid;
  place-items: center;
  padding: 18px;
}

.auth-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(20, 12, 10, 0.36);
  backdrop-filter: blur(10px);
}

.auth-modal {
  position: relative;
  width: min(980px, 96vw);
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.45);
  box-shadow: 0 40px 120px rgba(20, 12, 10, 0.45);
  background: rgba(255, 255, 255, 0.78);
  z-index: 2;
}

.auth-close {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.86);
  color: rgba(20, 12, 10, 0.82);
  font-size: 22px;
  line-height: 1;
}

.auth-inner {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  min-height: 560px;
}

.auth-left {
  padding: 34px 34px 28px;
  background: rgba(255, 255, 255, 0.94);
}

.auth-right {
  position: relative;
  background: linear-gradient(135deg, rgba(250, 128, 114, 1), rgba(214, 166, 74, 0.92));
  color: rgba(255, 255, 255, 0.95);
}

.auth-right::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.16), transparent 42%),
    radial-gradient(circle at 80% 40%, rgba(255, 255, 255, 0.12), transparent 46%),
    radial-gradient(circle at 65% 85%, rgba(255, 255, 255, 0.1), transparent 48%);
  opacity: 0.9;
}

.auth-right-inner {
  position: relative;
  height: 100%;
  padding: 34px;
  display: grid;
  align-content: center;
  justify-items: center;
  text-align: center;
  gap: 14px;
}

.auth-right-logo {
  width: min(320px, 72%);
  aspect-ratio: 1 / 1;
  object-fit: contain;
  filter: drop-shadow(0 18px 40px rgba(20, 12, 10, 0.35));
}

.auth-right-title {
  font-weight: 950;
  letter-spacing: -0.02em;
  font-size: 22px;
}

.auth-right-sub {
  opacity: 0.92;
  font-size: 14px;
}

.auth-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.auth-logo {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 245, 247, 0.9);
}

.auth-name {
  font-weight: 950;
  line-height: 1.05;
}

.auth-title {
  margin-top: 20px;
  font-size: 28px;
  letter-spacing: -0.02em;
  font-weight: 950;
}

.auth-sub {
  margin-top: 6px;
  font-size: 14px;
}

.auth-social {
  margin-top: 18px;
  display: grid;
  gap: 10px;
}

.auth-social-btn {
  justify-content: center;
}

.auth-divider {
  margin: 18px 0 12px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 12px;
}

.auth-divider span {
  height: 1px;
  background: rgba(20, 12, 10, 0.12);
}

.auth-divider-text {
  font-size: 12px;
  font-weight: 850;
  color: rgba(20, 12, 10, 0.58);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.auth-form {
  display: grid;
  gap: 12px;
}

.auth-field {
  display: grid;
  gap: 8px;
}

.auth-label {
  font-size: 12px;
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.auth-input-wrap {
  position: relative;
}

.auth-input {
  width: 100%;
  height: 44px;
  padding: 0 14px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.92);
  color: rgba(20, 12, 10, 0.9);
  outline: none;
  transition: box-shadow 0.12s ease, border-color 0.12s ease;
}

.auth-input:focus {
  border-color: rgba(242, 124, 134, 0.9);
  box-shadow: 0 0 0 4px rgba(242, 124, 134, 0.18);
}

.auth-ghost {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  height: 30px;
  padding: 0 10px;
  border-radius: 12px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.7);
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
  cursor: pointer;
}

.auth-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.auth-check {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  color: rgba(20, 12, 10, 0.7);
  font-size: 13px;
}

.auth-check input {
  width: 16px;
  height: 16px;
  accent-color: rgb(242, 124, 134);
}

.auth-link {
  font-size: 13px;
  font-weight: 900;
  color: rgba(242, 124, 134, 0.98);
  text-decoration: none;
}

.auth-link:hover {
  text-decoration: underline;
}

.auth-submit {
  margin-top: 2px;
}

@media (max-width: 860px) {
  .auth-inner {
    grid-template-columns: 1fr;
  }

  .auth-right {
    min-height: 220px;
  }

  .auth-left {
    padding: 26px 20px 22px;
  }

  .auth-right-inner {
    padding: 26px 20px;
  }
}

.drawer-head {
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.6);
}

.drawer-title {
  font-weight: 950;
  font-size: 16px;
}

.drawer-body {
  padding: 14px;
  overflow: auto;
  display: grid;
  gap: 14px;
  align-content: start;
}

.drawer-empty {
  padding: 14px;
}

.drawer-empty-title {
  font-weight: 950;
  font-size: 16px;
}

.cart-item-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.cart-name {
  font-weight: 950;
}

.qty {
  width: 40px;
  padding: 0;
}

.qty-val {
  width: 26px;
  text-align: center;
  font-weight: 950;
}

.cart-item-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-inner {
  display: grid;
  gap: 10px;
}

.summary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-weight: 850;
}

.summary-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 6px;
}

@media (min-width: 860px) {
  .hero-stats {
    grid-template-columns: repeat(3, 1fr);
  }

  .menu-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .how-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .contact {
    grid-template-columns: 1.3fr 0.9fr;
    align-items: start;
  }

  .footer-wrap {
    grid-template-columns: auto 1fr auto;
    justify-content: space-between;
  }
}
</style>
