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
              <h1 class="page-title">Products</h1>
              <p class="page-subtitle">Manage items you sell</p>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <button class="btn" type="button" @click="fetchProducts">Refresh</button>
              <button class="btn primary" type="button" @click="openAdd">Add product</button>
            </div>
          </template>
        </AppTopbar>

        <main class="container content">
          <section class="card">
            <div class="card-inner">
              <div class="toolbar">
                <div class="toolbar-left">
                  <div class="rows">
                    <div class="rows-label muted text-xs font-medium">Rows</div>
                    <select v-model.number="pageSize" class="rows-select text-xs font-semibold rounded-lg border border-slate-200 px-2 py-1 bg-white" aria-label="Rows per page">
                      <option v-for="n in pageSizes" :key="n" :value="n">{{ n }}</option>
                    </select>
                  </div>
                  <div class="meta muted text-xs font-medium">{{ filtered.length }} item(s)</div>
                </div>

                <div class="search relative">
                  <span class="search-ico absolute left-3 top-2.5 text-slate-400 pointer-events-none" aria-hidden="true">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M10.5 3a7.5 7.5 0 1 0 4.6 13.4l4 4a1 1 0 0 0 1.4-1.4l-4-4A7.5 7.5 0 0 0 10.5 3Zm0 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11Z" />
                    </svg>
                  </span>
                  <input
                    v-model="query"
                    class="search-input"
                    type="search"
                    placeholder="Search products..."
                    aria-label="Search products"
                  />
                </div>
              </div>

              <div v-if="loading" class="text-slate-500 text-xs p-8 text-center">Loading products...</div>
              <div v-else-if="error" class="p-8 text-center bg-slate-50/50 border border-slate-100 rounded-xl my-4">
                <div class="w-10 h-10 mx-auto rounded-full bg-rose-50 text-rose-500 flex items-center justify-center mb-3">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div class="text-sm font-bold text-slate-800">Backend API Disconnected</div>
                <div class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">Make sure your Django server is running at <code>http://localhost:8000</code>.</div>
                <button class="btn text-xs mt-4" type="button" @click="fetchProducts">Retry Connection</button>
              </div>
              <div v-else class="table">
                <div class="t-head muted">
                  <div>Product</div>
                  <div class="right">Price</div>
                  <div class="center">Availability</div>
                </div>

                <div v-for="p in paged" :key="p.id" class="t-row">
                  <div class="prod">
                    <button class="thumb-btn" type="button" @click="openImage(p)">
                      <img class="thumb" :src="p.image_url || logo" :alt="p.name" />
                    </button>
                    <div class="prod-text">
                      <div class="prod-name">{{ p.name }}</div>
                      <div class="prod-desc muted">
                        {{ p.description || '—' }}
                      </div>
                    </div>
                  </div>

                  <div class="right price">{{ formatPeso(p.price) }}</div>

                  <div class="center">
                    <label class="toggle">
                      <input
                        :checked="p.available"
                        type="checkbox"
                        @change="toggleAvailability(p, ($event.target as HTMLInputElement).checked)"
                      />
                      <span class="toggle-ui" aria-hidden="true" />
                      <span class="sr">{{ p.available ? 'Available' : 'Not available' }}</span>
                    </label>
                  </div>
                </div>

                <div v-if="filtered.length === 0" class="muted p-4 text-center">No products found.</div>
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

    <!-- Add product modal -->
    <div v-if="addOpen" class="modal" role="dialog" aria-modal="true" aria-label="Add product">
      <div class="modal-backdrop" @click="closeAdd" />
      <div class="modal-panel">
        <button class="modal-close" type="button" aria-label="Close" @click="closeAdd">×</button>
        <div class="modal-inner">
          <div class="modal-title">Add product</div>

          <form class="form" @submit.prevent="saveAdd">
            <label class="field">
              <span class="label">Product name</span>
              <input v-model.trim="form.name" class="input" type="text" placeholder="e.g., California Baked Sushi" required />
            </label>

            <label class="field">
              <span class="label">Price (₱)</span>
              <input v-model.number="form.price" class="input" type="number" min="0" step="1" placeholder="0" />
            </label>

            <label class="field">
              <span class="label">Description</span>
              <textarea
                v-model.trim="form.description"
                class="textarea"
                rows="3"
                placeholder="Short description..."
              />
            </label>

            <label class="field">
              <span class="label">Image URL</span>
              <input v-model.trim="form.image_url" class="input" type="url" placeholder="https://example.com/image.jpg" />
            </label>

            <label class="check">
              <input v-model="form.available" type="checkbox" />
              <span>Available</span>
            </label>

            <div class="actions">
              <button class="btn" type="button" @click="closeAdd">Cancel</button>
              <button class="btn primary" type="submit" :disabled="!form.name || saving">
                {{ saving ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Image viewer modal -->
    <div v-if="viewerOpen" class="viewer" role="dialog" aria-modal="true" aria-label="Image viewer">
      <div class="viewer-backdrop" @click="closeViewer" />
      <div class="viewer-panel">
        <button class="viewer-close" type="button" aria-label="Close" @click="closeViewer">×</button>
        <img class="viewer-img" :src="viewerSrc" alt="" />
        <div class="viewer-caption">{{ viewerCaption }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import logoUrl from '~/assets/digital_assets/logo.jpg?url'

const logo = logoUrl
const config = useRuntimeConfig()

type Product = {
  id: number | string
  name: string
  price: number
  description: string
  available: boolean
  image_url?: string
}

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const query = ref('')
const products = ref<Product[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')

async function fetchProducts() {
  loading.value = true
  error.value = ''
  try {
    const data = await $fetch<Product[]>(`${config.public.apiBase}/api/bakedsushi/products/list/`)
    products.value = data
  } catch (err: any) {
    error.value = 'Failed to load products from API.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProducts()
})

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return products.value
  return products.value.filter((p) => (p.name + ' ' + (p.description || '')).toLowerCase().includes(q))
})

const pageSizes = [5, 10, 20, 50]
const pageSize = ref(10)
const page = ref(1)

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

const addOpen = ref(false)
const form = reactive({
  name: '',
  price: 0,
  description: '',
  available: true,
  image_url: ''
})

const viewerOpen = ref(false)
const viewerSrc = ref('')
const viewerCaption = ref('')

function openAdd() {
  resetForm()
  addOpen.value = true
}

function closeAdd() {
  addOpen.value = false
}

async function saveAdd() {
  if (!form.name) return
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/bakedsushi/products/list/`, {
      method: 'POST',
      body: {
        name: form.name,
        price: Math.max(0, Math.round(Number(form.price) || 0)),
        description: form.description,
        available: form.available,
        image_url: form.image_url
      }
    })
    addOpen.value = false
    await fetchProducts()
  } catch (err) {
    alert('Failed to save product.')
  } finally {
    saving.value = false
  }
}

async function toggleAvailability(p: Product, available: boolean) {
  p.available = available
  try {
    await $fetch(`${config.public.apiBase}/api/bakedsushi/products/${p.id}/`, {
      method: 'PUT',
      body: { available }
    })
  } catch (err) {
    p.available = !available
    alert('Failed to update availability.')
  }
}

function openImage(p: Product) {
  viewerSrc.value = p.image_url || logo
  viewerCaption.value = p.name
  viewerOpen.value = true
}

function closeViewer() {
  viewerOpen.value = false
}

function resetForm() {
  form.name = ''
  form.price = 0
  form.description = ''
  form.available = true
  form.image_url = ''
}

watch([query, pageSize], () => {
  page.value = 1
})

watch(totalPages, (tp) => {
  if (page.value > tp) page.value = tp
})

function formatPeso(value: number) {
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value || 0)
}
</script>


<!-- Styles migrated to `ui/app/assets/css/main.css` -->
