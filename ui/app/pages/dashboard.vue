<template>
  <div class="admin-page">
    <div class="shell">
      <AppSidebar class="side" variant="fixed" :items="sidebarItems">
        <template #brand>
          <div class="side-brand">
            <img class="side-logo" :src="logo" alt="Baked Sushi logo" />
            <div>
              <div class="side-name">Baked Sushi</div>
              <div class="muted" style="font-size: 12px">Admin</div>
            </div>
          </div>
        </template>
        <template #footer>Tip: Data here is mock-only.</template>
      </AppSidebar>

      <div class="main">
        <AppTopbar>
          <template #left>
            <div class="brand">
              <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="brand-name">Dashboard</div>
                <div class="brand-tag muted">Orders • Sales • Overview</div>
              </div>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <NuxtLink class="btn" to="/">Home</NuxtLink>
              <button class="btn primary" type="button" @click="refreshMock">Refresh mock</button>
            </div>
          </template>
        </AppTopbar>

        <main class="container content">
      <section class="grid kpis">
        <article class="card">
          <div class="card-inner">
            <div class="kpi-k">Completed orders</div>
            <div class="kpi-v">{{ completedCount }}</div>
            <div class="kpi-sub muted">Fulfilled today</div>
          </div>
        </article>

        <article class="card">
          <div class="card-inner">
            <div class="kpi-k">Not completed</div>
            <div class="kpi-v">{{ pendingCount }}</div>
            <div class="kpi-sub muted">Preparing / for pickup</div>
          </div>
        </article>

        <article class="card kpi-accent">
          <div class="card-inner">
            <div class="kpi-k">Sales ({{ salesPeriodLabel }})</div>
            <div class="kpi-v">{{ formatPeso(salesTotal) }}</div>
            <div class="kpi-sub">Mock data • updates on refresh</div>
          </div>
        </article>
      </section>

      <section id="sales" class="card sales-card">
        <div class="card-inner">
          <div class="sales-head">
            <div>
              <div class="section-title">Sales</div>
              <div class="muted">Day / Month / Quarter / Year</div>
            </div>
            <div class="seg" role="tablist" aria-label="Sales period">
              <button
                v-for="p in periods"
                :key="p.key"
                class="seg-btn"
                :class="{ active: salesPeriod === p.key }"
                type="button"
                role="tab"
                :aria-selected="salesPeriod === p.key"
                @click="salesPeriod = p.key"
              >
                {{ p.label }}
              </button>
            </div>
          </div>

          <div class="sales-grid">
            <div class="bars" aria-label="Sales chart">
              <div
                v-for="b in salesBars"
                :key="b.label"
                class="bar"
                :title="`${b.label}: ${formatPeso(b.value)}`"
              >
                <div class="bar-top">
                  <div class="bar-label">{{ b.label }}</div>
                  <div class="bar-val muted">{{ formatCompactPeso(b.value) }}</div>
                </div>
                <div class="bar-track">
                  <div class="bar-fill" :style="{ width: `${b.pct}%` }" />
                </div>
              </div>
            </div>

            <div class="sales-summary">
              <div class="mini">
                <div class="mini-k muted">Average per day</div>
                <div class="mini-v">{{ formatPeso(avgPerDay) }}</div>
              </div>
              <div class="mini">
                <div class="mini-k muted">Best day</div>
                <div class="mini-v">{{ bestDayLabel }}</div>
              </div>
              <div class="mini">
                <div class="mini-k muted">Best day sales</div>
                <div class="mini-v">{{ formatPeso(bestDayValue) }}</div>
              </div>

              <div class="note">
                <div class="note-title">Note</div>
                <div class="muted">
                  This is frontend-only. Later we’ll replace these numbers with real data from the backend.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-inner">
          <div class="section-title">Quick actions</div>
          <div class="muted">Frontend placeholders</div>

          <div class="actions">
            <NuxtLink class="btn" to="/orders">Go to orders</NuxtLink>
            <NuxtLink class="btn" to="/products">Manage products</NuxtLink>
            <button class="btn" type="button" @click="noop">Export report</button>
            <button class="btn primary" type="button" @click="noop">Open settings</button>
          </div>
        </div>
      </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.png?url'

const logo = logoUrl

type OrderStatus = 'completed' | 'pending'
type Order = {
  id: string
  status: OrderStatus
  customer: string
  total: number
  createdAt: string // ISO
}

type SalesPeriod = 'day' | 'month' | 'quarter' | 'year'

const periods: Array<{ key: SalesPeriod; label: string }> = [
  { key: 'day', label: 'Day' },
  { key: 'month', label: 'Month' },
  { key: 'quarter', label: 'Quarter' },
  { key: 'year', label: 'Year' }
]

const salesPeriod = ref<SalesPeriod>('day')

const orders = ref<Order[]>(seedOrders())
const dailySales = ref<number[]>(seedDailySales()) // last 30 days

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const completedCount = computed(() => orders.value.filter((o) => o.status === 'completed').length)
const pendingCount = computed(() => orders.value.filter((o) => o.status === 'pending').length)

const salesPeriodLabel = computed(() => periods.find((p) => p.key === salesPeriod.value)?.label ?? 'Day')

const salesTotal = computed(() => {
  const days = periodDays(salesPeriod.value)
  return dailySales.value.slice(0, days).reduce((sum, v) => sum + v, 0)
})

const avgPerDay = computed(() => {
  const days = periodDays(salesPeriod.value)
  return Math.round(salesTotal.value / Math.max(1, days))
})

const bestDayValue = computed(() => Math.max(...dailySales.value))
const bestDayIndex = computed(() => dailySales.value.findIndex((v) => v === bestDayValue.value))
const bestDayLabel = computed(() => {
  const idx = bestDayIndex.value
  if (idx < 0) return '—'
  return idx === 0 ? 'Today' : `${idx}d ago`
})

const salesBars = computed(() => {
  const days = periodDays(salesPeriod.value)
  const values = dailySales.value.slice(0, days)
  const max = Math.max(1, ...values)

  // show up to 8 bars for readability
  const buckets = bucket(values, 8)
  const bucketMax = Math.max(1, ...buckets.map((b) => b.value))

  return buckets.map((b) => ({
    label: b.label,
    value: b.value,
    pct: Math.round((b.value / bucketMax) * 100)
  }))
})

function refreshMock() {
  orders.value = seedOrders()
  dailySales.value = seedDailySales()
}

function formatPeso(value: number) {
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value)
}

function formatCompactPeso(value: number) {
  const formatted = new Intl.NumberFormat('en-PH', { notation: 'compact', maximumFractionDigits: 1 }).format(value)
  return `₱ ${formatted}`
}

function periodDays(p: SalesPeriod) {
  if (p === 'day') return 1
  if (p === 'month') return 30
  if (p === 'quarter') return 90
  return 365
}

function bucket(values: number[], maxBars: number) {
  const take = Math.min(values.length, maxBars)
  if (values.length <= take) {
    return values.map((v, i) => ({ label: i === 0 ? 'Today' : `${i}d`, value: v }))
  }
  const size = Math.ceil(values.length / take)
  const out: Array<{ label: string; value: number }> = []
  for (let i = 0; i < values.length; i += size) {
    const chunk = values.slice(i, i + size)
    const sum = chunk.reduce((a, b) => a + b, 0)
    const label = i === 0 ? 'Now' : `${i}-${Math.min(values.length - 1, i + size - 1)}d`
    out.push({ label, value: sum })
  }
  return out.slice(0, take)
}

function seedOrders(): Order[] {
  const customers = ['Aira', 'Janelle', 'Mark', 'Pia', 'Kyle', 'Tina', 'Jomar', 'Rhea', 'CJ', 'Aly']
  const now = Date.now()
  const count = 14 + Math.floor(Math.random() * 10)

  const list: Order[] = []
  for (let i = 0; i < count; i++) {
    const status: OrderStatus = Math.random() > 0.45 ? 'completed' : 'pending'
    const total = Math.round(220 + Math.random() * 1500)
    list.push({
      id: String(1000 + i),
      status,
      customer: customers[Math.floor(Math.random() * customers.length)],
      total,
      createdAt: new Date(now - i * 1000 * 60 * 35).toISOString()
    })
  }
  return list
}

function seedDailySales(): number[] {
  // last 30 days (index 0 = today)
  const days = 30
  const out: number[] = []
  for (let i = 0; i < days; i++) {
    const weekendBoost = i % 7 === 0 || i % 7 === 1 ? 1.25 : 1
    const base = 1800 + Math.random() * 5200
    out.push(Math.round(base * weekendBoost))
  }
  return out
}

function noop() {}
</script>

<style scoped>

.shell {
  min-height: 100vh;
}

.main {
  min-height: 100vh;
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
  font-weight: 950;
  letter-spacing: 0.02em;
  line-height: 1.05;
}

.brand-tag {
  font-size: 12px;
  margin-top: 2px;
}

.top-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.content {
  padding: 18px 0 40px;
  display: grid;
  gap: 14px;
}

.side {
  display: none;
}

.side-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.side-logo {
  width: 38px;
  height: 38px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 245, 247, 0.9);
}

.side-name {
  font-weight: 950;
  line-height: 1.05;
}

.grid {
  display: grid;
  gap: 14px;
}

.kpis {
  grid-template-columns: repeat(3, 1fr);
}

.two {
  grid-template-columns: 1.25fr 0.75fr;
}

.kpi-k {
  font-weight: 950;
  letter-spacing: -0.01em;
}

.kpi-v {
  margin-top: 8px;
  font-size: 34px;
  font-weight: 950;
  letter-spacing: -0.03em;
}

.kpi-sub {
  margin-top: 6px;
  font-size: 13px;
}

.kpi-accent {
  background: radial-gradient(900px 350px at 20% 10%, rgba(242, 124, 134, 0.22), transparent 55%),
    radial-gradient(700px 320px at 85% 70%, rgba(214, 166, 74, 0.18), transparent 60%),
    rgba(255, 255, 255, 0.78);
}

.sales-card .card-inner {
  padding: 18px;
}

.sales-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.section-title {
  font-weight: 950;
  font-size: 16px;
  letter-spacing: -0.01em;
}

.seg {
  display: inline-flex;
  padding: 5px;
  border-radius: 999px;
  background: rgba(20, 12, 10, 0.05);
  border: 1px solid rgba(20, 12, 10, 0.08);
  gap: 6px;
}

.seg-btn {
  height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid transparent;
  background: transparent;
  font-weight: 950;
  color: rgba(20, 12, 10, 0.7);
  cursor: pointer;
}

.seg-btn.active {
  background: rgba(255, 255, 255, 0.86);
  border-color: rgba(20, 12, 10, 0.12);
  color: rgba(20, 12, 10, 0.92);
}

.sales-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: 1.35fr 0.65fr;
  gap: 14px;
  align-items: start;
}

.bars {
  display: grid;
  gap: 10px;
}

.bar-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}

.bar-label {
  font-weight: 950;
  font-size: 13px;
}

.bar-track {
  margin-top: 8px;
  height: 12px;
  border-radius: 999px;
  background: rgba(20, 12, 10, 0.08);
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(242, 124, 134, 1), rgba(214, 166, 74, 1));
  box-shadow: 0 8px 20px rgba(242, 124, 134, 0.14);
}

.sales-summary {
  display: grid;
  gap: 10px;
}

.mini {
  padding: 12px;
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.1);
  background: rgba(255, 255, 255, 0.74);
}

.mini-v {
  margin-top: 6px;
  font-weight: 950;
  font-size: 18px;
}

.note {
  margin-top: 4px;
  padding: 12px;
  border-radius: 18px;
  background: rgba(242, 124, 134, 0.08);
  border: 1px solid rgba(214, 166, 74, 0.18);
}

.note-title {
  font-weight: 950;
  margin-bottom: 4px;
}

.table {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}

.t-head,
.t-row {
  display: grid;
  grid-template-columns: 0.7fr 0.9fr 1.4fr 0.9fr;
  gap: 10px;
  align-items: center;
}

.t-head {
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 950;
}

.t-row {
  padding: 10px 12px;
  border-radius: 16px;
  border: 1px solid rgba(20, 12, 10, 0.08);
  background: rgba(255, 255, 255, 0.74);
}

.right {
  text-align: right;
}

.pill {
  display: inline-flex;
  align-items: center;
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  font-weight: 950;
  font-size: 12px;
  border: 1px solid rgba(20, 12, 10, 0.12);
}

.pill.completed {
  background: rgba(214, 166, 74, 0.18);
  border-color: rgba(214, 166, 74, 0.35);
}

.pill.pending {
  background: rgba(242, 124, 134, 0.14);
  border-color: rgba(242, 124, 134, 0.32);
}

.actions {
  margin-top: 12px;
  display: grid;
  gap: 10px;
}

@media (max-width: 980px) {
  .kpis {
    grid-template-columns: 1fr;
  }

  .sales-grid {
    grid-template-columns: 1fr;
  }

  .two {
    grid-template-columns: 1fr;
  }
}

</style>
