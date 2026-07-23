<template>
  <div class="admin-page">
    <div class="shell">
      <AppSidebar class="side" variant="fixed" :items="sidebarItems">
        <template #brand>
          <div class="side-brand">
            <img class="side-logo" :src="logo" alt="Baked Sushi logo" />
            <div>
              <div class="side-name">Baked Sushi</div>
              <div class="text-[11px] font-semibold text-slate-400">Admin Panel</div>
            </div>
          </div>
        </template>
        <template #footer>Connected to Backend API</template>
      </AppSidebar>

      <div class="main">
        <AppTopbar>
          <template #left>
            <div>
              <h1 class="page-title">Dashboard</h1>
              <p class="page-subtitle">Quick view of store activity</p>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <button class="btn" type="button" @click="fetchOrders">Refresh</button>
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
                <div class="kpi-sub">Total sales from real orders</div>
              </div>
            </article>
          </section>

          <section class="card sales-card">
            <div class="card-inner">
              <div class="sales-head">
                <div>
                  <div class="section-title text-sm font-extrabold text-slate-900">Sales overview</div>
                  <div class="muted text-xs">Monitor totals across different time ranges</div>
                </div>

                <div class="seg flex items-center gap-1 bg-slate-100 p-1 rounded-xl" role="tablist" aria-label="Sales period">
                  <button
                    v-for="period in periods"
                    :key="period.key"
                    class="seg-btn text-xs font-semibold px-3 py-1 rounded-lg transition"
                    :class="salesPeriod === period.key ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'"
                    type="button"
                    @click="salesPeriod = period.key"
                  >
                    {{ period.label }}
                  </button>
                </div>
              </div>

              <div v-if="loading" class="text-slate-500 text-xs p-8 text-center">Loading metrics...</div>
              <div v-else-if="error" class="p-8 text-center bg-slate-50/50 border border-slate-100 rounded-xl my-4">
                <div class="w-10 h-10 mx-auto rounded-full bg-rose-50 text-rose-500 flex items-center justify-center mb-3">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div class="text-sm font-bold text-slate-800">Backend API Disconnected</div>
                <div class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">Make sure your Django server is running at <code>http://localhost:8000</code>.</div>
                <button class="btn text-xs mt-4" type="button" @click="fetchOrders">Retry Connection</button>
              </div>
              <div v-else class="sales-grid">
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
                  <div v-if="salesBars.length === 0" class="muted p-4">No order data available for chart.</div>
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

                  <div v-for="order in recentOrders" :key="order.id" class="t-row">
                    <div class="mono">#{{ order.id }}</div>
                    <div>
                      <span class="pill" :class="order.status">{{ order.status }}</span>
                    </div>
                    <div>{{ order.customer }}</div>
                    <div class="right">{{ formatPeso(order.total) }}</div>
                  </div>

                  <div v-if="recentOrders.length === 0" class="muted p-4 text-center">No orders recorded yet.</div>
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
import logoUrl from '~/assets/digital_assets/logo.jpg?url'

const logo = logoUrl
const config = useRuntimeConfig()

type ApiOrder = {
  id: number
  customer: string
  total: number
  items: number
  paid: boolean
  completed: boolean
  created_at: string
}

type OrderStatus = 'completed' | 'pending'
type Order = {
  id: number | string
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
const apiOrders = ref<ApiOrder[]>([])
const loading = ref(false)
const error = ref('')

async function fetchOrders() {
  loading.value = true
  error.value = ''
  try {
    const data = await $fetch<ApiOrder[]>(`${config.public.apiBase}/api/bakedsushi/orders/list/`)
    apiOrders.value = data
  } catch (err: any) {
    error.value = 'Failed to load dashboard data from API.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const orders = computed<Order[]>(() =>
  apiOrders.value.map((o) => ({
    id: o.id,
    status: o.completed ? 'completed' : 'pending',
    customer: o.customer,
    total: o.total,
    createdAt: o.created_at
  }))
)

const recentOrders = computed(() =>
  [...orders.value]
    .sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))
    .slice(0, 6)
)

const completedCount = computed(() => orders.value.filter((order) => order.status === 'completed').length)
const pendingCount = computed(() => orders.value.filter((order) => order.status === 'pending').length)

const salesPeriodLabel = computed(() => periods.find((period) => period.key === salesPeriod.value)?.label ?? 'Day')

// Group orders into daily sales totals for up to 365 days
const dailySales = computed(() => {
  const now = new Date()
  const days = 365
  const result: number[] = new Array(days).fill(0)

  for (const o of apiOrders.value) {
    const d = new Date(o.created_at)
    const diffTime = Math.abs(now.getTime() - d.getTime())
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
    if (diffDays >= 0 && diffDays < days) {
      result[diffDays] += o.total || 0
    }
  }
  return result
})

const salesTotal = computed(() => {
  const days = periodDays(salesPeriod.value)
  return dailySales.value.slice(0, days).reduce((sum, value) => sum + value, 0)
})

const avgPerDay = computed(() => {
  const days = periodDays(salesPeriod.value)
  return Math.round(salesTotal.value / Math.max(1, days))
})

const bestDayValue = computed(() => (dailySales.value.length ? Math.max(...dailySales.value) : 0))
const bestDayIndex = computed(() => dailySales.value.findIndex((value) => value === bestDayValue.value))
const bestDayLabel = computed(() => {
  const index = bestDayIndex.value
  if (index < 0 || bestDayValue.value === 0) return '-'
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

function formatPeso(value: number) {
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value || 0)
}

function formatCompactPeso(value: number) {
  const formatted = new Intl.NumberFormat('en-PH', {
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(value || 0)

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

function noop() {}
</script>

