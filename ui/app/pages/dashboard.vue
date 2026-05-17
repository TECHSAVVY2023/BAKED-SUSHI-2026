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
        <template #footer>Tip: Dashboard metrics here are mock-only.</template>
      </AppSidebar>

      <div class="main">
        <AppTopbar>
          <template #left>
            <div class="brand">
              <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="brand-name">Dashboard</div>
                <div class="brand-tag muted">Quick view of store activity</div>
              </div>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <button class="btn" type="button" @click="refreshMock">Refresh mock</button>
              <NuxtLink class="btn primary" to="/orders">View orders</NuxtLink>
            </div>
          </template>
        </AppTopbar>

        <main class="container content">
          <section class="grid kpis">
            <article class="card">
              <div class="card-inner">
                <div class="kpi-k">Completed orders</div>
                <div class="kpi-v">{{ completedCount }}</div>
                <div class="kpi-sub muted">Finished and ready for handoff</div>
              </div>
            </article>

            <article class="card">
              <div class="card-inner">
                <div class="kpi-k">Pending orders</div>
                <div class="kpi-v">{{ pendingCount }}</div>
                <div class="kpi-sub muted">Still being prepared</div>
              </div>
            </article>

            <article class="card kpi-accent">
              <div class="card-inner">
                <div class="kpi-k">{{ salesPeriodLabel }} sales</div>
                <div class="kpi-v">{{ formatCompactPeso(salesTotal) }}</div>
                <div class="kpi-sub">Based on mock sales history</div>
              </div>
            </article>
          </section>

          <section class="card sales-card">
            <div class="card-inner">
              <div class="sales-head">
                <div>
                  <div class="section-title">Sales overview</div>
                  <div class="muted">Monitor totals across different time ranges</div>
                </div>

                <div class="seg" role="tablist" aria-label="Sales period">
                  <button
                    v-for="period in periods"
                    :key="period.key"
                    class="seg-btn"
                    :class="{ active: salesPeriod === period.key }"
                    type="button"
                    @click="salesPeriod = period.key"
                  >
                    {{ period.label }}
                  </button>
                </div>
              </div>

              <div class="sales-grid">
                <div class="bars">
                  <div v-for="bar in salesBars" :key="bar.label" class="mini">
                    <div class="bar-top">
                      <div class="bar-label">{{ bar.label }}</div>
                      <div class="muted">{{ formatPeso(bar.value) }}</div>
                    </div>
                    <div class="bar-track">
                      <div class="bar-fill" :style="{ width: `${bar.pct}%` }" />
                    </div>
                  </div>
                </div>

                <div class="sales-summary">
                  <div class="mini">
                    <div class="muted">Total for {{ salesPeriodLabel.toLowerCase() }}</div>
                    <div class="mini-v">{{ formatPeso(salesTotal) }}</div>
                  </div>

                  <div class="mini">
                    <div class="muted">Average per day</div>
                    <div class="mini-v">{{ formatPeso(avgPerDay) }}</div>
                  </div>

                  <div class="mini">
                    <div class="muted">Best day</div>
                    <div class="mini-v">{{ formatPeso(bestDayValue) }}</div>
                    <div class="kpi-sub muted">{{ bestDayLabel }}</div>
                  </div>

                  <div class="note">
                    <div class="note-title">Quick insight</div>
                    <div class="muted">
                      Sales are strongest on <strong>{{ bestDayLabel }}</strong>, so that is a good time to spotlight promos or bundle offers.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="grid two">
            <article class="card">
              <div class="card-inner">
                <div class="section-title">Recent orders</div>
                <div class="table">
                  <div class="t-head muted">
                    <div>Order</div>
                    <div>Status</div>
                    <div>Customer</div>
                    <div class="right">Total</div>
                  </div>

                  <div v-for="order in orders.slice(0, 6)" :key="order.id" class="t-row">
                    <div class="mono">#{{ order.id }}</div>
                    <div>
                      <span class="pill" :class="order.status">{{ order.status }}</span>
                    </div>
                    <div>{{ order.customer }}</div>
                    <div class="right">{{ formatPeso(order.total) }}</div>
                  </div>
                </div>
              </div>
            </article>

            <article class="card">
              <div class="card-inner">
                <div class="section-title">Quick actions</div>
                <div class="muted">Jump straight to the areas you manage most.</div>

                <div class="actions">
                  <NuxtLink class="btn" to="/orders">Go to orders</NuxtLink>
                  <NuxtLink class="btn" to="/products">Manage products</NuxtLink>
                  <button class="btn" type="button" @click="noop">Export report</button>
                  <button class="btn primary" type="button" @click="noop">Open settings</button>
                </div>
              </div>
            </article>
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
  createdAt: string
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
const dailySales = ref<number[]>(seedDailySales())

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const completedCount = computed(() => orders.value.filter((order) => order.status === 'completed').length)
const pendingCount = computed(() => orders.value.filter((order) => order.status === 'pending').length)

const salesPeriodLabel = computed(() => periods.find((period) => period.key === salesPeriod.value)?.label ?? 'Day')

const salesTotal = computed(() => {
  const days = periodDays(salesPeriod.value)
  return dailySales.value.slice(0, days).reduce((sum, value) => sum + value, 0)
})

const avgPerDay = computed(() => {
  const days = periodDays(salesPeriod.value)
  return Math.round(salesTotal.value / Math.max(1, days))
})

const bestDayValue = computed(() => Math.max(...dailySales.value))
const bestDayIndex = computed(() => dailySales.value.findIndex((value) => value === bestDayValue.value))
const bestDayLabel = computed(() => {
  const index = bestDayIndex.value
  if (index < 0) return '-'
  return index === 0 ? 'Today' : `${index}d ago`
})

const salesBars = computed(() => {
  const days = periodDays(salesPeriod.value)
  const values = dailySales.value.slice(0, days)
  const buckets = bucket(values, 8)
  const bucketMax = Math.max(1, ...buckets.map((entry) => entry.value))

  return buckets.map((entry) => ({
    label: entry.label,
    value: entry.value,
    pct: Math.round((entry.value / bucketMax) * 100)
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
  const formatted = new Intl.NumberFormat('en-PH', {
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(value)

  return `PHP ${formatted}`
}

function periodDays(period: SalesPeriod) {
  if (period === 'day') return 1
  if (period === 'month') return 30
  if (period === 'quarter') return 90
  return 365
}

function bucket(values: number[], maxBars: number) {
  const take = Math.min(values.length, maxBars)

  if (values.length <= take) {
    return values.map((value, index) => ({ label: index === 0 ? 'Today' : `${index}d`, value }))
  }

  const size = Math.ceil(values.length / take)
  const out: Array<{ label: string; value: number }> = []

  for (let index = 0; index < values.length; index += size) {
    const chunk = values.slice(index, index + size)
    const sum = chunk.reduce((left, right) => left + right, 0)
    const label = index === 0 ? 'Now' : `${index}-${Math.min(values.length - 1, index + size - 1)}d`
    out.push({ label, value: sum })
  }

  return out.slice(0, take)
}

function seedOrders(): Order[] {
  const customers = ['Aira', 'Janelle', 'Mark', 'Pia', 'Kyle', 'Tina', 'Jomar', 'Rhea', 'CJ', 'Aly']
  const now = Date.now()
  const count = 14 + Math.floor(Math.random() * 10)

  const list: Order[] = []

  for (let index = 0; index < count; index++) {
    const status: OrderStatus = Math.random() > 0.45 ? 'completed' : 'pending'
    const total = Math.round(220 + Math.random() * 1500)

    list.push({
      id: String(1000 + index),
      status,
      customer: customers[Math.floor(Math.random() * customers.length)],
      total,
      createdAt: new Date(now - index * 1000 * 60 * 35).toISOString()
    })
  }

  return list
}

function seedDailySales(): number[] {
  const days = 30
  const out: number[] = []

  for (let index = 0; index < days; index++) {
    const weekendBoost = index % 7 === 0 || index % 7 === 1 ? 1.25 : 1
    const base = 1800 + Math.random() * 5200
    out.push(Math.round(base * weekendBoost))
  }

  return out
}

function noop() {}
</script>
