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
        <template #footer>Tip: Products here are mock-only.</template>
      </AppSidebar>

      <div class="main">
        <AppTopbar>
          <template #left>
            <div class="brand">
              <img class="brand-logo" :src="logo" alt="Baked Sushi logo" />
              <div>
                <div class="brand-name">Products</div>
                <div class="brand-tag muted">Manage items you sell</div>
              </div>
            </div>
          </template>

          <template #right>
            <div class="top-actions">
              <button class="btn" type="button" @click="refreshMock">Refresh mock</button>
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
                    <div class="rows-label muted">Rows</div>
                    <select v-model.number="pageSize" class="rows-select" aria-label="Rows per page">
                      <option v-for="n in pageSizes" :key="n" :value="n">{{ n }}</option>
                    </select>
                  </div>
                  <div class="meta muted">{{ filtered.length }} item(s)</div>
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
                    placeholder="Search products..."
                    aria-label="Search products"
                  />
                </div>
              </div>

              <div class="table">
                <div class="t-head muted">
                  <div>Product</div>
                  <div class="right">Price</div>
                  <div class="center">Availability</div>
                </div>

                <div v-for="p in paged" :key="p.id" class="t-row">
                  <div class="prod">
                    <button class="thumb-btn" type="button" @click="openImage(p)">
                      <img class="thumb" :src="p.imageUrl || logo" :alt="p.name" />
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
                      <input v-model="p.available" type="checkbox" />
                      <span class="toggle-ui" aria-hidden="true" />
                      <span class="sr">{{ p.available ? 'Available' : 'Not available' }}</span>
                    </label>
                  </div>
                </div>
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
          <div class="muted">Frontend mock only</div>

          <form class="form" @submit.prevent="saveAdd">
            <label class="field">
              <span class="label">Product name</span>
              <input v-model.trim="form.name" class="input" type="text" placeholder="e.g., California Baked Sushi" />
            </label>

            <label class="field">
              <span class="label">Price</span>
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
              <span class="label">Picture</span>
              <div class="upload">
                <input class="file" type="file" accept="image/*" @change="onFile" />
                <div class="preview">
                  <img v-if="form.imagePreview" class="preview-img" :src="form.imagePreview" alt="Preview" />
                  <div v-else class="preview-empty muted">Upload a photo (optional)</div>
                </div>
              </div>
            </label>

            <label class="check">
              <input v-model="form.available" type="checkbox" />
              <span>Available</span>
            </label>

            <div class="actions">
              <button class="btn" type="button" @click="closeAdd">Cancel</button>
              <button class="btn primary" type="submit" :disabled="!form.name">Save</button>
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
import logoUrl from '~/assets/digital_assets/logo.png?url'

const logo = logoUrl

type Product = {
  id: string
  name: string
  price: number
  description: string
  available: boolean
  imageUrl?: string
}

const sidebarItems = [
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Orders', to: '/orders' },
  { label: 'Products', to: '/products' }
]

const query = ref('')
const products = ref<Product[]>(seedProducts())

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return products.value
  return products.value.filter((p) => (p.name + ' ' + p.description).toLowerCase().includes(q))
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
  file: null as File | null,
  imagePreview: '' as string
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

function onFile(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0] || null
  form.file = file
  if (form.imagePreview) URL.revokeObjectURL(form.imagePreview)
  form.imagePreview = file ? URL.createObjectURL(file) : ''
}

function saveAdd() {
  const id = String(Date.now())
  const imageUrl = form.imagePreview || undefined
  products.value = [
    {
      id,
      name: form.name,
      price: Math.max(0, Math.round(Number(form.price) || 0)),
      description: form.description,
      available: !!form.available,
      imageUrl
    },
    ...products.value
  ]
  addOpen.value = false
}

function openImage(p: Product) {
  viewerSrc.value = p.imageUrl || logo
  viewerCaption.value = p.name
  viewerOpen.value = true
}

function closeViewer() {
  viewerOpen.value = false
}

function refreshMock() {
  products.value = seedProducts()
  query.value = ''
  page.value = 1
}

function resetForm() {
  form.name = ''
  form.price = 0
  form.description = ''
  form.available = true
  form.file = null
  if (form.imagePreview) URL.revokeObjectURL(form.imagePreview)
  form.imagePreview = ''
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

function seedProducts(): Product[] {
  return [
    {
      id: 'p-1',
      name: 'Baked Sushi (Classic)',
      price: 250,
      description: 'Creamy, savory, and freshly baked.',
      available: true
    },
    {
      id: 'p-2',
      name: 'Baked Sushi Duo Tray',
      price: 550,
      description: 'Best for sharing. Made to order.',
      available: true
    },
    {
      id: 'p-3',
      name: 'Kimbap Rolls (Bilao)',
      price: 600,
      description: 'A festive tray of bite-sized goodness.',
      available: false
    }
  ]
}
</script>

<style scoped>

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

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(20, 12, 10, 0.08);
  flex-wrap: wrap;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.table {
  margin-top: 14px;
  display: grid;
  gap: 10px;
}

.rows {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(20, 12, 10, 0.04);
  border: 1px solid rgba(20, 12, 10, 0.08);
}

.rows-label {
  font-weight: 950;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.rows-select {
  height: 32px;
  border-radius: 999px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.86);
  padding: 0 10px;
  font-weight: 950;
  color: rgba(20, 12, 10, 0.86);
  outline: none;
}

.pager {
  margin-top: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 12px;
  border-top: 1px solid rgba(20, 12, 10, 0.08);
}

.page-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.page-btn,
.page-num {
  height: 38px;
  min-width: 38px;
  padding: 0 12px;
  border-radius: 12px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 255, 255, 0.72);
  font-weight: 950;
  color: rgba(20, 12, 10, 0.82);
  cursor: pointer;
}

.page-num {
  padding: 0 14px;
}

.page-btn:disabled,
.page-num:disabled {
  opacity: 0.45;
  cursor: default;
}

.page-num.active {
  background: rgba(242, 124, 134, 0.14);
  border-color: rgba(242, 124, 134, 0.28);
  color: rgba(20, 12, 10, 0.92);
}

.page-num.ellipsis {
  background: transparent;
  border-color: transparent;
  min-width: 24px;
  padding: 0 6px;
  cursor: default;
}

.strong {
  font-weight: 950;
}

.t-head,
.t-row {
  display: grid;
  grid-template-columns: 1.6fr 0.6fr 0.7fr;
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
  padding: 12px;
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.08);
  background: rgba(255, 255, 255, 0.74);
}

.prod {
  display: flex;
  gap: 12px;
  align-items: center;
  min-width: 0;
}

.thumb-btn {
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.thumb {
  width: 46px;
  height: 46px;
  border-radius: 16px;
  object-fit: cover;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 245, 247, 0.9);
}

.prod-text {
  min-width: 0;
}

.prod-name {
  font-weight: 950;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.prod-desc {
  margin-top: 2px;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.price {
  font-weight: 950;
}

.toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.toggle input {
  width: 18px;
  height: 18px;
  accent-color: rgb(242, 124, 134);
}

.toggle-ui {
  display: none;
}

.upload {
  display: grid;
  gap: 10px;
}

.file {
  width: 100%;
}

.preview {
  border-radius: 18px;
  border: 1px dashed rgba(20, 12, 10, 0.18);
  background: rgba(255, 245, 247, 0.8);
  padding: 12px;
  display: grid;
  place-items: center;
}

.preview-img {
  width: 100%;
  max-height: 220px;
  object-fit: cover;
  border-radius: 16px;
  border: 1px solid rgba(20, 12, 10, 0.12);
}

.preview-empty {
  font-weight: 850;
  font-size: 13px;
}

.check {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  color: rgba(20, 12, 10, 0.72);
}

.check input {
  width: 16px;
  height: 16px;
  accent-color: rgb(242, 124, 134);
}

/* Viewer */
.viewer-panel {
  position: relative;
  z-index: 2;
  width: min(920px, 96vw);
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.45);
  box-shadow: 0 40px 120px rgba(20, 12, 10, 0.45);
  background: rgba(255, 255, 255, 0.9);
  padding: 14px;
  display: grid;
  gap: 10px;
}

.viewer-close {
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

.viewer-img {
  width: 100%;
  max-height: min(70vh, 720px);
  object-fit: contain;
  border-radius: 18px;
  border: 1px solid rgba(20, 12, 10, 0.12);
  background: rgba(255, 245, 247, 0.7);
}

.viewer-caption {
  text-align: center;
  font-weight: 950;
  color: rgba(20, 12, 10, 0.78);
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

</style>
