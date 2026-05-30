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
        <template #footer>Tip: Orders here are mock-only.</template>
      </AppSidebar>

      <div class="main">
        <AppTopbar>
          <template #left>
            <div class="brand">
              <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="brand-name">Orders</div>
                <div class="brand-tag muted">Track completed and pending orders</div>
              </div>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <button class="btn" type="button" @click="refreshMock">Refresh mock</button>
              <button class="btn primary" type="button" @click="openCreate">Create order</button>
            </div>
          </template>
        </AppTopbar>

        <main class="container content">
          <section class="grid kpis">
            <article class="card">
              <div class="card-inner">
                <div class="kpi-k">Completed</div>
                <div class="kpi-v">{{ completedCount }}</div>
                <div class="kpi-sub muted">Marked as completed</div>
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
                <div class="kpi-k">Sales (all)</div>
                <div class="kpi-v">{{ formatPeso(totalSales) }}</div>
                <div class="kpi-sub">Mock totals</div>
              </div>
            </article>
          </section>

          <section class="card">
            <div class="card-inner">
              <div class="toolbar">
                <div class="toolbar-left">
                  <div class="rows">
                    <div class="rows-label muted">Rows</div>
                    <select v-model.number="pageSize" class="rows-select" aria-label="Rows per page">
                      <option v-for="n in pageSizes" :key="n" :value="n">{{ n }}</option>
                    </select>
                  </div>

                  <div class="filters">
                    <button
                      v-for="f in filters"
                      :key="f.key"
                      class="chip"
                      :class="{ active: statusFilter === f.key }"
                      type="button"
                      @click="statusFilter = f.key"
                    >
                      {{ f.label }}
                    </button>
                  </div>
                </div>

                <div class="search">
                  <span class="search-ico" aria-hidden="true">
                    <svg viewBox="0 0 24 24">
                      <path
                        d="M10.5 3a7.5 7.5 0 1 0 4.6 13.4l4 4a1 1 0 0 0 1.4-1.4l-4-4A7.5 7.5 0 0 0 10.5 3Zm0 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11Z"
                        fill="currentColor"
                      />
                    </svg>
                  </span>
                  <input
                    v-model="query"
                    class="search-input"
                    type="search"
                    placeholder="Search orders..."
                    aria-label="Search orders"
                  />
                </div>
              </div>

              <div class="table">
                <div class="t-head muted">
                  <div>Order</div>
                  <div>Customer</div>
                  <div class="right">Total</div>
                  <div class="center">Paid</div>
                  <div class="center">Completed</div>
                </div>

                <button
                  v-for="o in paged"
                  :key="o.id"
                  class="t-row"
                  type="button"
                  @click="openDetails(o)"
                >
                  <div class="cell">
                    <div class="id mono">#{{ o.id }}</div>
                    <div class="sub muted">{{ formatWhen(o.createdAt) }}</div>
                  </div>
                  <div class="cell">
                    <div class="strong">{{ o.customer }}</div>
                    <div class="sub muted">{{ o.items }} item(s)</div>
                  </div>
                  <div class="cell right strong">{{ formatPeso(o.total) }}</div>
                  <div class="cell center" @click.stop>
                    <label class="check">
                      <input v-model="o.paid" type="checkbox" />
                      <span class="sr">{{ o.paid ? 'Paid' : 'Not paid' }}</span>
                    </label>
                  </div>
                  <div class="cell center" @click.stop>
                    <label class="check">
                      <input v-model="o.completed" type="checkbox" />
                      <span class="sr">{{ o.completed ? 'Completed' : 'Not completed' }}</span>
                    </label>
                  </div>
                </button>
              </div>

              <div class="pager">
                <div class="showing muted">
                  Showing <span class="strong">{{ showingFrom }}</span>-<span class="strong">{{ showingTo }}</span> of
                  <span class="strong">{{ filtered.length }}</span>
                </div>

                <div class="page-actions" aria-label="Pagination">
                  <button class="page-btn" type="button" :disabled="page <= 1" @click="page = 1" aria-label="First page">
                    «
                  </button>
                  <button
                    class="page-btn"
                    type="button"
                    :disabled="page <= 1"
                    @click="page -= 1"
                    aria-label="Previous page"
                  >
                    ‹
                  </button>

                  <button
                    v-for="p in pageButtons"
                    :key="p.key"
                    class="page-num"
                    :class="{ active: p.type === 'page' && p.value === page, ellipsis: p.type === 'ellipsis' }"
                    type="button"
                    :disabled="p.type === 'ellipsis'"
                    @click="p.type === 'page' && (page = p.value)"
                  >
                    {{ p.label }}
                  </button>

                  <button class="page-btn" type="button" :disabled="page >= totalPages" @click="page += 1" aria-label="Next page">
                    ›
                  </button>
                  <button class="page-btn" type="button" :disabled="page >= totalPages" @click="page = totalPages" aria-label="Last page">
                    »
                  </button>
                </div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>

    <!-- Create order modal -->
    <div v-if="createOpen" class="modal" role="dialog" aria-modal="true" aria-label="Create order">
      <div class="modal-backdrop" @click="closeCreate" />
      <div class="modal-panel">
        <button class="modal-close" type="button" aria-label="Close" @click="closeCreate">×</button>
        <div class="modal-inner">
          <div class="modal-title">Create order</div>
          <div class="muted">Frontend mock only</div>

          <form class="form" @submit.prevent="saveCreate">
            <label class="field">
              <span class="label">Customer</span>
              <input v-model.trim="form.customer" class="input" type="text" placeholder="Customer name" />
            </label>
            <label class="field">
              <span class="label">Total</span>
              <input v-model.number="form.total" class="input" type="number" min="0" step="1" placeholder="0" />
            </label>
            <label class="field">
              <span class="label">Items count</span>
              <input v-model.number="form.items" class="input" type="number" min="1" step="1" placeholder="1" />
            </label>
            <label class="check-row">
              <input v-model="form.paid" type="checkbox" />
              <span>Mark as paid</span>
            </label>
            <label class="check-row">
              <input v-model="form.completed" type="checkbox" />
              <span>Mark as completed</span>
            </label>

            <div class="actions">
              <button class="btn" type="button" @click="closeCreate">Cancel</button>
              <button class="btn primary" type="submit" :disabled="!form.customer">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Details modal -->
    <div v-if="detailsOpen" class="modal" role="dialog" aria-modal="true" aria-label="Order details">
      <div class="modal-backdrop" @click="closeDetails" />
      <div class="modal-panel">
        <button class="modal-close" type="button" aria-label="Close" @click="closeDetails">×</button>
        <div class="modal-inner">
          <div class="modal-title">Order #{{ details.id }}</div>
          <div class="muted">{{ formatWhen(details.createdAt) }}</div>

          <div class="detail-grid">
            <div class="detail">
              <div class="label">Customer</div>
              <div class="val">{{ details.customer }}</div>
            </div>
            <div class="detail">
              <div class="label">Items</div>
              <div class="val">{{ details.items }}</div>
            </div>
            <div class="detail">
              <div class="label">Total</div>
              <div class="val">{{ formatPeso(details.total) }}</div>
            </div>
            <div class="detail">
              <div class="label">Paid</div>
              <div class="val">
                <label class="check">
                  <input v-model="details.paid" type="checkbox" />
                  <span class="sr">{{ details.paid ? 'Paid' : 'Not paid' }}</span>
                </label>
              </div>
            </div>
            <div class="detail">
              <div class="label">Completed</div>
              <div class="val">
                <label class="check">
                  <input v-model="details.completed" type="checkbox" />
                  <span class="sr">{{ details.completed ? 'Completed' : 'Not completed' }}</span>
                </label>
              </div>
            </div>
          </div>

          <div class="actions">
            <button class="btn" type="button" @click="closeDetails">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.png?url'

const logo = logoUrl

type Order = {
  id: string
  customer: string
  total: number
  items: number
  paid: boolean
  completed: boolean
  createdAt: string // ISO
}

type FilterKey = 'all' | 'completed' | 'pending'

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const filters: Array<{ key: FilterKey; label: string }> = [
  { key: 'all', label: 'All' },
  { key: 'pending', label: 'Not completed' },
  { key: 'completed', label: 'Completed' }
]

const query = ref('')
const statusFilter = ref<FilterKey>('all')
const orders = ref<Order[]>(seedOrders())

const pageSizes = [5, 10, 20, 50]
const pageSize = ref(10)
const page = ref(1)

const completedCount = computed(() => orders.value.filter((o) => o.completed).length)
const pendingCount = computed(() => orders.value.filter((o) => !o.completed).length)
const totalSales = computed(() => orders.value.reduce((sum, o) => sum + (o.total || 0), 0))

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return orders.value
    .filter((o) => {
      if (statusFilter.value === 'completed') return o.completed
      if (statusFilter.value === 'pending') return !o.completed
      return true
    })
    .filter((o) => {
      if (!q) return true
      return (`${o.id} ${o.customer}`).toLowerCase().includes(q)
    })
    .sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1))
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize.value)))
const paged = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filtered.value.slice(start, start + pageSize.value)
})

const showingFrom = computed(() => (filtered.value.length ? (page.value - 1) * pageSize.value + 1 : 0))
const showingTo = computed(() =>
  Math.min(filtered.value.length, (page.value - 1) * pageSize.value + paged.value.length)
)

const pageButtons = computed(() => {
  const max = totalPages.value
  const current = Math.min(max, Math.max(1, page.value))
  const windowSize = 5

  if (max <= 7) {
    return Array.from({ length: max }, (_, i) => ({
      type: 'page' as const,
      key: `p-${i + 1}`,
      value: i + 1,
      label: String(i + 1)
    }))
  }

  const start = Math.max(2, current - Math.floor(windowSize / 2))
  const end = Math.min(max - 1, start + windowSize - 1)
  const realStart = Math.max(2, end - windowSize + 1)

  const out: Array<
    | { type: 'page'; key: string; value: number; label: string }
    | { type: 'ellipsis'; key: string; label: string }
  > = [{ type: 'page', key: 'p-1', value: 1, label: '1' }]

  if (realStart > 2) out.push({ type: 'ellipsis', key: 'e-1', label: '…' })

  for (let i = realStart; i <= end; i++) out.push({ type: 'page', key: `p-${i}`, value: i, label: String(i) })

  if (end < max - 1) out.push({ type: 'ellipsis', key: 'e-2', label: '…' })
  out.push({ type: 'page', key: `p-${max}`, value: max, label: String(max) })
  return out
})

const createOpen = ref(false)
const form = reactive({
  customer: '',
  total: 0,
  items: 1,
  paid: false,
  completed: false
})

const detailsOpen = ref(false)
const details = reactive<Order>({
  id: '',
  customer: '',
  total: 0,
  items: 0,
  paid: false,
  completed: false,
  createdAt: new Date().toISOString()
})

function openCreate() {
  form.customer = ''
  form.total = 0
  form.items = 1
  form.paid = false
  form.completed = false
  createOpen.value = true
}

function closeCreate() {
  createOpen.value = false
}

function saveCreate() {
  const id = String(1000 + Math.floor(Math.random() * 9000))
  orders.value = [
    {
      id,
      customer: form.customer,
      total: Math.max(0, Math.round(Number(form.total) || 0)),
      items: Math.max(1, Math.round(Number(form.items) || 1)),
      paid: !!form.paid,
      completed: !!form.completed,
      createdAt: new Date().toISOString()
    },
    ...orders.value
  ]
  createOpen.value = false
}

function openDetails(o: Order) {
  details.id = o.id
  details.customer = o.customer
  details.total = o.total
  details.items = o.items
  details.paid = o.paid
  details.completed = o.completed
  details.createdAt = o.createdAt
  detailsOpen.value = true
}

function closeDetails() {
  // sync changes back (since `details` is a copy)
  const idx = orders.value.findIndex((o) => o.id === details.id)
  if (idx >= 0) {
    orders.value[idx].paid = details.paid
    orders.value[idx].completed = details.completed
  }
  detailsOpen.value = false
}

function refreshMock() {
  orders.value = seedOrders()
  query.value = ''
  statusFilter.value = 'all'
  page.value = 1
}

function formatPeso(value: number) {
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value || 0)
}

function formatWhen(iso: string) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return new Intl.DateTimeFormat('en-PH', {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(d)
}

function seedOrders(): Order[] {
  const customers = ['Aira', 'Janelle', 'Mark', 'Pia', 'Kyle', 'Tina', 'Jomar', 'Rhea', 'CJ', 'Aly']
  const now = Date.now()
  const count = 18 + Math.floor(Math.random() * 12)

  const list: Order[] = []
  for (let i = 0; i < count; i++) {
    const paid = Math.random() > 0.25
    const completed = Math.random() > 0.45
    const total = Math.round(220 + Math.random() * 1800)
    const items = 1 + Math.floor(Math.random() * 6)
    list.push({
      id: String(1000 + i),
      paid,
      completed,
      customer: customers[Math.floor(Math.random() * customers.length)],
      total,
      items,
      createdAt: new Date(now - i * 1000 * 60 * 32).toISOString()
    })
  }
  return list
}

watch([query, statusFilter, pageSize], () => {
  page.value = 1
})

watch(totalPages, (tp) => {
  if (page.value > tp) page.value = tp
})
</script>

<!-- Styles migrated to `ui/app/assets/css/main.css` -->
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

.grid {
  display: grid;
  gap: 14px;
}

.kpis {
  grid-template-columns: repeat(3, 1fr);
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
.t-head,
.t-row {
  display: grid;
  grid-template-columns: 1fr 1.1fr 0.7fr 0.55fr 0.55fr;
  gap: 12px;
  align-items: center;
}

.t-head {
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 950;
}

.t-row {
  text-align: left;
  width: 100%;
  padding: 12px;
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.08);
  background: rgba(255, 255, 255, 0.74);
  cursor: pointer;
}

.t-row:hover {
  background: rgba(255, 255, 255, 0.88);
}

.cell {
  min-width: 0;
}

.id {
  font-weight: 950;
}

.strong {
  font-weight: 950;
}

.sub {
  margin-top: 2px;
  font-size: 12px;
}

.center {
  display: grid;
  justify-items: center;
}

.check input {
  width: 16px;
  height: 16px;
  accent-color: rgb(242, 124, 134);
}

/* Modal */
.modal {
  position: fixed;
  inset: 0;
  z-index: 90;
  display: grid;
  place-items: center;
  padding: 18px;
}

.modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(20, 12, 10, 0.36);
  backdrop-filter: blur(10px);
}

.modal-panel {
  position: relative;
  z-index: 2;
  width: min(560px, 96vw);
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.45);
  box-shadow: 0 40px 120px rgba(20, 12, 10, 0.45);
  background: rgba(255, 255, 255, 0.92);
}

.modal-close {
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

.modal-inner {
  padding: 18px;
}

.modal-title {
  font-weight: 950;
  font-size: 18px;
  letter-spacing: -0.01em;
}

.form {
  margin-top: 14px;
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 8px;
}

.label {
  font-size: 12px;
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border-radius: 14px;
  border: 1px solid rgba(20, 12, 10, 0.14);
  background: rgba(255, 255, 255, 0.92);
  color: rgba(20, 12, 10, 0.9);
  outline: none;
}

.check-row {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 950;
  color: rgba(20, 12, 10, 0.74);
}

.check-row input {
  width: 16px;
  height: 16px;
  accent-color: rgb(242, 124, 134);
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 4px;
  flex-wrap: wrap;
}

.detail-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail {
  padding: 12px;
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.1);
  background: rgba(255, 255, 255, 0.74);
}

.val {
  margin-top: 6px;
  font-weight: 950;
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

@media (max-width: 980px) {
  .kpis {
    grid-template-columns: 1fr;
  }

  .t-head,
  .t-row {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .right {
    text-align: left;
  }

  .center {
    justify-items: start;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 980px) {
  .side {
    display: block;
  }

  .main {
    margin-left: 280px;
  }
}

